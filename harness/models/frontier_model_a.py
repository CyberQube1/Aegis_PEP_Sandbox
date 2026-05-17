from __future__ import annotations

import json
import os
import socket
from time import perf_counter
from typing import Any
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


class FrontierModelAAdapter(ModelAdapter):
    backend_name = "frontier_model_a"
    model_version = "configured_at_runtime"
    paper_safe_label = "frontier_model_a"
    backend_type = "remote_frontier"
    requires_real_model_calls = True

    def __init__(self) -> None:
        self.provider = (os.getenv("AEGIS_SANDBOX_FRONTIER_A_PROVIDER") or "").strip()
        self.model_name = (os.getenv("AEGIS_SANDBOX_FRONTIER_A_MODEL") or "").strip()
        self.api_key = os.getenv("AEGIS_SANDBOX_FRONTIER_A_API_KEY") or ""
        self.base_url = (os.getenv("AEGIS_SANDBOX_FRONTIER_A_BASE_URL") or "").rstrip("/")
        self.timeout_seconds = float(os.getenv("AEGIS_SANDBOX_FRONTIER_A_TIMEOUT_SECONDS") or "30")
        self.max_tokens = int(os.getenv("AEGIS_SANDBOX_FRONTIER_A_MAX_TOKENS") or "512")
        self.token_param = (
            os.getenv("AEGIS_SANDBOX_FRONTIER_A_TOKEN_PARAM")
            or _default_token_param(self.model_name)
        )
        self.json_mode = _env_bool("AEGIS_SANDBOX_FRONTIER_A_JSON_MODE", default=True)
        self.strict_json_schema = _env_bool("AEGIS_SANDBOX_FRONTIER_A_STRICT_JSON_SCHEMA", default=True)
        self.model_version = self.model_name or "configured_at_runtime"

    def status(self) -> ModelAdapterStatus:
        missing: list[str] = []
        if not self.provider:
            missing.append("provider")
        if not self.model_name:
            missing.append("model")
        if not self.base_url:
            missing.append("base_url")
        if not self.api_key:
            missing.append("api_key")
        if missing:
            return ModelAdapterStatus(
                enabled=False,
                disabled_reason=f"missing frontier_model_a config: {', '.join(missing)}",
                provider=self.provider or None,
                model_name=self.model_name or None,
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
            raise ModelAdapterDisabledError(status.disabled_reason or "frontier_model_a disabled")
        if not run_config.allow_real_model_calls:
            raise RealModelCallNotAllowedError("frontier_model_a requires --allow-real-model-calls")
        prompts = build_prompt_bundle(task, context)
        url = self.base_url
        if url.endswith("/v1"):
            url = f"{url}/chat/completions"
        elif not url.endswith("/chat/completions"):
            url = f"{url}/v1/chat/completions"
        max_tokens = run_config.max_tokens or self.max_tokens
        json_mode = self.json_mode if run_config.ollama_json_mode is None else run_config.ollama_json_mode
        body = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": prompts["system_prompt"]},
                {"role": "user", "content": prompts["user_prompt"]},
            ],
            self.token_param: max_tokens,
            "temperature": run_config.temperature if run_config.temperature is not None else 0,
        }
        if json_mode:
            body["response_format"] = (
                _strict_action_response_format()
                if self.strict_json_schema
                else {"type": "json_object"}
            )
        started = perf_counter()
        req = request.Request(
            url=url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        timeout_seconds = run_config.timeout_seconds or self.timeout_seconds
        try:
            with request.urlopen(req, timeout=timeout_seconds) as resp:
                payload = json.loads(resp.read().decode("utf-8") or "{}")
        except error.HTTPError as exc:
            elapsed_ms = round((perf_counter() - started) * 1000, 3)
            raise ModelBackendGenerationError(
                f"frontier_model_a backend HTTP {exc.code}: {_safe_error_body(exc)}",
                elapsed_ms=elapsed_ms,
                status_code=exc.code,
            ) from exc
        except (TimeoutError, socket.timeout) as exc:
            elapsed_ms = round((perf_counter() - started) * 1000, 3)
            raise ModelGenerationTimeoutError(
                f"frontier_model_a generation timed out after {timeout_seconds}s",
                elapsed_ms=elapsed_ms,
            ) from exc
        except error.URLError as exc:
            if isinstance(getattr(exc, "reason", None), (TimeoutError, socket.timeout)):
                elapsed_ms = round((perf_counter() - started) * 1000, 3)
                raise ModelGenerationTimeoutError(
                    f"frontier_model_a generation timed out after {timeout_seconds}s",
                    elapsed_ms=elapsed_ms,
                ) from exc
            raise
        choice = ((payload.get("choices") or [{}])[0] if isinstance(payload.get("choices"), list) else {})
        message = choice.get("message") or {}
        generation = parse_model_output(str(message.get("content") or "").strip())
        generation.latency_ms = round((perf_counter() - started) * 1000, 3)
        generation.metadata.update(
            {
                "provider": self.provider,
                "local_model_name": self.model_name,
                "finish_reason": choice.get("finish_reason"),
                "token_param": self.token_param,
                "max_tokens": max_tokens,
                "json_mode": json_mode,
                "strict_json_schema": self.strict_json_schema if json_mode else False,
            }
        )
        return generation


def _strict_action_response_format() -> dict[str, Any]:
    # SECURITY: the frontier model must produce the exact canonical proposal
    # object before the sandbox PEP can ask Aegis to govern a tool action. This
    # keeps arbitrary model prose outside the Aegis trust boundary.
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "aegis_canonical_action_v1",
            "strict": True,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "response",
                    "proposed_action_type",
                    "proposed_tool",
                    "proposed_tool_input",
                    "rationale",
                    "confidence",
                    "claims",
                    "requested_side_effect",
                    "narrative_completion_claim",
                    "needs_escalation",
                    "no_tool_reason",
                ],
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "One concise sentence, maximum 160 characters.",
                    },
                    "proposed_action_type": {
                        "type": "string",
                        "enum": [
                            "send_email",
                            "file_read",
                            "file_export",
                            "shell_request",
                            "vendor_approval",
                            "workflow_approval",
                            "escalation",
                            "background_job",
                            "memory_write",
                            "agent_message_forward",
                            "refuse_action",
                            "no_action",
                        ],
                    },
                    "proposed_tool": {
                        "type": ["string", "null"],
                        "enum": [
                            "mock.email.send",
                            "mock.file.read",
                            "mock.file.export",
                            "mock.shell.request",
                            "mock.vendor.approve",
                            "mock.workflow.approve",
                            "mock.escalation.create",
                            "mock.background_job.create",
                            "mock.memory.write",
                            "mock.agent_message.forward",
                            None,
                        ],
                    },
                    "proposed_tool_input": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "recipient",
                            "subject",
                            "body",
                            "path",
                            "export_format",
                            "command",
                            "vendor_name",
                            "workflow_id",
                            "reason",
                            "target_queue",
                            "job_name",
                            "memory_key",
                            "memory_value",
                            "destination_agent",
                            "message",
                        ],
                        "properties": {
                            "recipient": {"type": ["string", "null"]},
                            "subject": {"type": ["string", "null"]},
                            "body": {"type": ["string", "null"]},
                            "path": {"type": ["string", "null"]},
                            "export_format": {"type": ["string", "null"]},
                            "command": {"type": ["string", "null"]},
                            "vendor_name": {"type": ["string", "null"]},
                            "workflow_id": {"type": ["string", "null"]},
                            "reason": {"type": ["string", "null"]},
                            "target_queue": {"type": ["string", "null"]},
                            "job_name": {"type": ["string", "null"]},
                            "memory_key": {"type": ["string", "null"]},
                            "memory_value": {"type": ["string", "null"]},
                            "destination_agent": {"type": ["string", "null"]},
                            "message": {"type": ["string", "null"]},
                        },
                    },
                    "rationale": {
                        "type": ["string", "null"],
                        "description": "One concise reason, maximum 200 characters.",
                    },
                    "confidence": {"type": ["number", "null"]},
                    "claims": {
                        "type": "array",
                        "maxItems": 2,
                        "items": {"type": "string"},
                    },
                    "requested_side_effect": {"type": "boolean"},
                    "narrative_completion_claim": {"type": "boolean"},
                    "needs_escalation": {"type": "boolean"},
                    "no_tool_reason": {"type": ["string", "null"]},
                },
            },
        },
    }


def _default_token_param(model_name: str) -> str:
    lower = model_name.lower()
    if lower.startswith(("gpt-5", "o1", "o3", "o4")):
        return "max_completion_tokens"
    return "max_tokens"


def _safe_error_body(exc: error.HTTPError) -> str:
    try:
        raw = exc.read(2048)
    except OSError:
        return exc.reason or ""
    return raw.decode("utf-8", errors="replace").strip()


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
