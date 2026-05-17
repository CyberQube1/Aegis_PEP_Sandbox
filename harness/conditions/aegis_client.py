from __future__ import annotations

import http.client
import json
import socket
import ssl
import string
from typing import Any
from urllib.parse import urljoin, urlparse


class AegisClientError(ValueError):
    def __init__(
        self,
        message: str,
        *,
        classification: str = "transport_failure",
        status_code: int | None = None,
        response_snippet: str | None = None,
        response_payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.classification = classification
        self.status_code = status_code
        self.response_snippet = response_snippet
        self.response_payload = response_payload


class _ServerNameOverrideHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, server_name_override: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._server_name_override = server_name_override

    def connect(self) -> None:  # pragma: no cover - exercised through integration tests
        sock = socket.create_connection((self.host, self.port), self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        self.sock = self._context.wrap_socket(
            sock,
            server_hostname=self._server_name_override or self.host,
        )


class AegisDecisionClient:
    def __init__(
        self,
        *,
        endpoint_url: str,
        decision_path: str,
        ca_cert_file: str,
        client_cert_file: str,
        client_key_file: str,
        server_name_override: str | None = None,
        host_header: str | None = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.decision_path = decision_path if decision_path.startswith("/") else f"/{decision_path}"
        self.ca_cert_file = ca_cert_file
        self.client_cert_file = client_cert_file
        self.client_key_file = client_key_file
        self.server_name_override = server_name_override
        self.host_header = host_header
        self.timeout_seconds = timeout_seconds

    def _ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(cafile=self.ca_cert_file)
        context.load_cert_chain(certfile=self.client_cert_file, keyfile=self.client_key_file)
        if self.server_name_override:
            context.check_hostname = True
        return context

    def decide(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = urljoin(f"{self.endpoint_url}/", self.decision_path.lstrip("/"))
        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            raise AegisClientError(f"invalid Aegis endpoint URL: {url}")
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Content-Length": str(len(body)),
        }
        headers.update(self._correlation_headers(payload))
        # Caddy may require a public Host header that differs from the socket
        # address used inside Docker. Keep Host and TLS SNI independently
        # configurable so the mesh client can use a routed address without
        # weakening certificate verification.
        expected_host = self.host_header or self.server_name_override
        if expected_host:
            headers["Host"] = expected_host
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"
        conn: http.client.HTTPConnection = _ServerNameOverrideHTTPSConnection(
            host,
            parsed.port or 443,
            timeout=self.timeout_seconds,
            context=self._ssl_context(),
            server_name_override=self.server_name_override,
        )
        try:
            conn.request("POST", path, body=body, headers=headers)
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8")
            parsed: dict[str, Any] | None = None
            if raw:
                try:
                    candidate = json.loads(raw)
                    if isinstance(candidate, dict):
                        parsed = candidate
                except json.JSONDecodeError:
                    parsed = None
            if resp.status >= 400:
                raise AegisClientError(
                    f"HTTP {resp.status}: {raw or resp.reason}",
                    classification=self._classify_http_failure(resp.status, raw),
                    status_code=resp.status,
                    response_snippet=raw[:512],
                    response_payload=parsed,
                )
            return parsed if parsed is not None else json.loads(raw or "{}")
        except Exception as exc:  # pragma: no cover - transport failures are normalized by caller
            if isinstance(exc, AegisClientError):
                raise
            raise AegisClientError(str(exc)) from exc
        finally:
            conn.close()

    @classmethod
    def _correlation_headers(cls, payload: dict[str, Any]) -> dict[str, str]:
        attributes = payload.get("attributes") if isinstance(payload.get("attributes"), dict) else {}
        candidates = {
            "X-Aegis-Correlation-Id": payload.get("correlation_id"),
            "X-Aegis-Request-Id": payload.get("request_id"),
            "X-Sandbox-Run-Id": payload.get("run_id"),
            "X-Sandbox-Task-Id": attributes.get("task_id"),
        }
        return {
            name: value
            for name, raw in candidates.items()
            if (value := cls._safe_header_value(raw))
        }

    @staticmethod
    def _safe_header_value(raw: Any) -> str | None:
        if raw is None:
            return None
        value = str(raw).strip()
        if not value:
            return None
        # These IDs are reflected into proxy access logs for timing joins.
        # Reject control characters so a task/run identifier cannot forge log
        # lines or smuggle additional headers through the mesh route.
        if any(ch not in string.printable or ch in "\r\n\t" for ch in value):
            return None
        return value[:256]

    @staticmethod
    def _classify_http_failure(status_code: int, response_body: str) -> str:
        body = (response_body or "").lower()
        if "governance bundle verification failed" in body or "signature verification failed" in body:
            return "governance_bundle_verification_failed"
        if 500 <= status_code <= 599:
            return "aegis_upstream_failure"
        return "aegis_http_failure"
