# -*- coding: utf-8 -*-
"""Zero-dependency HTTP server (http.server) with Bearer token auth."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from ..types import Action, Decision
from ..models.clm_model import CLMModel
from ..engine.decision_engine import DecisionEngine
from ..engine.router import Router
from .schemas import decision_request, decision_response


class _Handler(BaseHTTPRequestHandler):
    router: Optional[Router] = None
    token: str = ""

    def _send(self, code: int, obj) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        if not self.token:
            return True
        auth = self.headers.get("Authorization", "")
        return auth == f"Bearer {self.token}"

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "service": "clmforge"})
            return
        if self.path == "/stats":
            if not self._authorized():
                self._send(401, {"error": "unauthorized"})
                return
            self._send(200, {"router": self.router.stats,
                             "cache": self.router.engine.model.action_cache.stats()})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/decide":
            if not self._authorized():
                self._send(401, {"error": "unauthorized"})
                return
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            actions = [Action(key=k, name=k) for k in data.get("keys", [])]
            decision = Decision(state=data["state"], actions=actions)
            result = self.router.route(decision)
            self._send(200, decision_response(result))
            return
        self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def create_server(router: Router, host: str = "127.0.0.1", port: int = 8765,
                  token: str = "") -> ThreadingHTTPServer:
    _Handler.router = router
    _Handler.token = token
    return ThreadingHTTPServer((host, port), _Handler)


def run_server(router: Router, host: str = "127.0.0.1", port: int = 8765,
               token: str = "") -> None:
    srv = create_server(router, host, port, token)
    print(f"clmforge server listening on http://{host}:{port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
