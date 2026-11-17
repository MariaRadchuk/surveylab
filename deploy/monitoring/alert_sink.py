"""Умовний отримувач сповіщень: друкує коротке зведення кожного webhook-запиту Alertmanager."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        for alert in body.get("alerts", []):
            print(
                f"[{alert['status'].upper()}] {alert['labels'].get('alertname')} "
                f"severity={alert['labels'].get('severity')} "
                f"- {alert['annotations'].get('summary')}",
                flush=True,
            )
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
