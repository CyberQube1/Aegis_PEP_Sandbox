from __future__ import annotations

import json
import os
import socket
from time import perf_counter
from urllib import error, request

from harness.adapters.model_adapter import (
    ModelAdapter,
    ModelBackendGenerationError,
    ModelAdapterDisabledError,
    ModelAdapterStatus,
    ModelGenerationTimeoutError,
    ModelGeneration,
    ModelRunConfig,
    RealModelCallNotAllowedError,
    build_prompt_bundle,
    parse_model_output,
)


class GemmaLocalAdapter(ModelAdapter):
    backend_name = "gemma_local"
    model_version = "configured_at_runtime"
    paper_safe_label = "open_model_a"
    backend_type = "local_open"
    requires_real_model_calls = True

    def __init__(self) -> None:
        self.provider = (
            os.getenv("AEGIS_SANDBOX_GEMMA_PROVIDER")
            or os.getenv("AEGIS_SANDBOX_OPEN_MODEL_A_PROVIDER")
            or "ollama"
        ).strip()
        self.model_name = (
            os.getenv("AEGIS_SANDBOX_GEMMA_MODEL")
            or os.getenv("AEGIS_SANDBOX_OPEN_MODEL_A_MODEL")
            or "gemma4:e2b-it-q8_0"
        ).strip()
        self.base_url = (
            os.getenv("AEGIS_SANDBOX_GEMMA_BASE_URL")
            or os.getenv("AEGIS_SANDBOX_OPEN_MODEL_A_BASE_URL")
            or "http://127.0.0.1:11434"
        ).rstrip("/")
        self.timeout_seconds = float(
            os.getenv("AEGIS_SANDBOX_GEMMA_TIMEOUT_SECONDS")
            or os.getenv("AEGIS_SANDBOX_OPEN_MODEL_A_TIMEOUT_SECONDS")
            or "600"
        )
        self.max_tokens = int(
            os.getenv("AEGIS_SANDBOX_GEMMA_MAX_TOKENS")
            or os.getenv("AEGIS_SANDBOX_OPEN_MODEL_A_MAX_TOKENS")
            or "512"
        )
        self.temperature = float(os.getenv("AEGIS_SANDBOX_GEMMA_TEMPERATURE") or "0")
        self.top_p = float(os.getenv("AEGIS_SANDBOX_GEMMA_TOP_P") or "0.9")
        self.ollama_json_mode = _env_bool("AEGIS_SANDBOX_GEMMA_JSON_MODE", default=True)
        self.keep_alive = os.getenv("AEGIS_SANDBOX_GEMMA_KEEP_ALIVE") or "0"
        self.model_version = self.model_name

    def status(self) -> ModelAdapterStatus:
        if self.provider.lower() != "ollama":
            return ModelAdapterStatus(
                enabled=False,
                disabled_reason=f"unsupported gemma_local provider: {self.provider}",
                provider=self.provider,
                model_name=self.model_name,
                backend_type=self.backend_type,
            )
        if not self.base_url or not self.model_name:
            return ModelAdapterStatus(
                enabled=False,
                disabled_reason="missing Ollama base URL or model name",
                provider=self.provider,
                model_name=self.model_name or None,
                backend_type=self.backend_type,
            )
        try:
            with request.urlopen(f"{self.base_url}/api/tags", timeout=min(self.timeout_seconds, 5.0)) as resp:
                payload = json.loads(resp.read().decode("utf-8") or "{}")
        except (OSError, error.URLError, json.JSONDecodeError) as exc:
            return ModelAdapterStatus(
                enabled=False,
                disabled_reason=f"Ollama unreachable at {self.base_url}: {exc}",
                provider=self.provider,
                model_name=self.model_name,
                backend_type=self.backend_type,
            )
        installed = {str(item.get("model") or "").strip() for item in payload.get("models", []) if isinstance(item, dict)}
        if self.model_name not in installed:
            return ModelAdapterStatus(
                enabled=False,
                disabled_reason=f"Ollama reachable but model not installed: {self.model_name}",
                provider=self.provider,
                model_name=self.model_name,
                backend_type=self.backend_type,
            )
        return ModelAdapterStatus(
            enabled=True,
            provider=self.provider,
            model_name=self.model_name,
            backend_type=self.backend_type,
        )

    def generate(
        self,
        task: dict[str, Any],
        context: dict[str, Any],
        run_config: ModelRunConfig,
    ) -> ModelGeneration:
        status = self.status()
        if not status.enabled:
            raise ModelAdapterDisabledError(status.disabled_reason or "gemma_local disabled")
        if not run_config.allow_real_model_calls:
            raise RealModelCallNotAllowedError("gemma_local requires --allow-real-model-calls")
        prompts = build_prompt_bundle(task, context)
        timeout_seconds = run_config.timeout_seconds if run_config.timeout_seconds is not None else self.timeout_seconds
        max_tokens = run_config.max_tokens if run_config.max_tokens is not None else self.max_tokens
        temperature = run_config.temperature if run_config.temperature is not None else self.temperature
        top_p = run_config.top_p if run_config.top_p is not None else self.top_p
        json_mode = self.ollama_json_mode if run_config.ollama_json_mode is None else run_config.ollama_json_mode
        keep_alive = run_config.keep_alive if run_config.keep_alive is not None else self.keep_alive
        body = {
            "model": self.model_name,
            "prompt": f"{prompts['system_prompt']}\n\n{prompts['user_prompt']}",
            "stream": False,
            "keep_alive": keep_alive,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
        }
        if json_mode:
            # Ollama JSON mode asks the backend to constrain decoding to a JSON
            # object. The prompt still carries the schema because not every
            # model obeys format mode perfectly under CPU-only pressure.
            body["format"] = "json"
        started = perf_counter()
        req = request.Request(
            url=f"{self.base_url}/api/generate",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=timeout_seconds) as resp:
                payload = json.loads(resp.read().decode("utf-8") or "{}")
        except error.HTTPError as exc:
            elapsed_ms = round((perf_counter() - started) * 1000, 3)
            body_text = _safe_error_body(exc)
            if run_config.cleanup_on_timeout:
                self._best_effort_unload()
            raise ModelBackendGenerationError(
                f"gemma_local backend HTTP {exc.code}: {body_text or exc.reason}",
                elapsed_ms=elapsed_ms,
                status_code=exc.code,
            ) from exc
        except (TimeoutError, socket.timeout) as exc:
            elapsed_ms = round((perf_counter() - started) * 1000, 3)
            if run_config.cleanup_on_timeout:
                self._best_effort_unload()
            raise ModelGenerationTimeoutError(
                f"gemma_local generation timed out after {timeout_seconds}s",
                elapsed_ms=elapsed_ms,
            ) from exc
        except error.URLError as exc:
            if isinstance(getattr(exc, "reason", None), (TimeoutError, socket.timeout)):
                elapsed_ms = round((perf_counter() - started) * 1000, 3)
                if run_config.cleanup_on_timeout:
                    self._best_effort_unload()
                raise ModelGenerationTimeoutError(
                    f"gemma_local generation timed out after {timeout_seconds}s",
                    elapsed_ms=elapsed_ms,
                ) from exc
            raise
        generation = parse_model_output(str(payload.get("response") or "").strip())
        generation.latency_ms = round((perf_counter() - started) * 1000, 3)
        generation.metadata.update(
            {
                "provider": self.provider,
                "local_model_name": self.model_name,
                "base_url": self.base_url,
                "done_reason": payload.get("done_reason"),
                "timeout_seconds": timeout_seconds,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "ollama_json_mode": json_mode,
                "keep_alive": keep_alive,
            }
        )
        return generation

    def _best_effort_unload(self) -> None:
        body = {
            "model": self.model_name,
            "prompt": "",
            "stream": False,
            "keep_alive": 0,
        }
        req = request.Request(
            url=f"{self.base_url}/api/generate",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=5.0) as resp:
                resp.read()
        except OSError:
            # Cleanup is advisory: the fail-closed row is already produced by
            # the caller. Operators can still use `ollama stop` if the backend
            # keeps a CPU-bound generation alive after the HTTP timeout.
            return


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _safe_error_body(exc: error.HTTPError) -> str:
    try:
        raw = exc.read(2048)
    except OSError:
        return ""
    return raw.decode("utf-8", errors="replace").strip()
