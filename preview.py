"""Serve only the public site and known installer; not used on GitHub Pages."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json, os
root = Path(__file__).resolve().parent
config = json.loads((root/'release.json').read_text())
filename = f"FramePulse-{config['version']}-Setup-x64.exe"
release_path = (root.parent/filename).resolve()
class Preview(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, directory=root/'site', **kwargs)
    def translate_path(self, path):
        if urlsplit(path).path == f'/downloads/{filename}':
            return str(release_path)
        return super().translate_path(path)
    def list_directory(self, path):
        self.send_error(404)
        return None
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        if urlsplit(self.path).path == f'/downloads/{filename}':
            self.send_header('Content-Disposition',f'attachment; filename="{filename}"')
        super().end_headers()
ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT','4188'))), Preview).serve_forever()
