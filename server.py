from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, mimetypes
BASE=Path(__file__).parent
def calculate(subtotal):
    discount = subtotal*0.10 if subtotal >= 10000 else 0
    tax = (subtotal-discount)*0.18
    return {"subtotal":subtotal,"discount":discount,"tax":tax,"total":subtotal-discount+tax}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=="/api/calculate":
            s=float(parse_qs(u.query).get("subtotal",["0"])[0])
            self.send_json(calculate(s)); return
        p=BASE/("index.html" if u.path=="/" else u.path.lstrip("/"))
        if p.exists() and p.is_file():
            data=p.read_bytes(); self.send_response(200); self.send_header("Content-Type",mimetypes.guess_type(p)[0] or "text/plain"); self.end_headers(); self.wfile.write(data)
        else: self.send_error(404)
    def send_json(self,obj):
        data=json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(data)
HTTPServer(("127.0.0.1",5000),Handler).serve_forever()
