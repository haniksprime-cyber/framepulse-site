"""Verify the release asset and make a GitHub Pages directory."""
from pathlib import Path
import hashlib, json, re, shutil, sys

root = Path(__file__).resolve().parent
conf = json.loads((root/'release.json').read_text(encoding='utf-8'))
repo, installer = sys.argv[1], Path(sys.argv[2])
version = conf['version']
assert re.fullmatch(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+', repo)
assert re.fullmatch(r'\d+\.\d+\.\d+', version)
assert installer.name == f'FramePulse-{version}-Setup-x64.exe'
with installer.open('rb') as f:
    assert f.read(2) == b'MZ', 'Expected Windows installer (EXE)'
    f.seek(0)
    assert hashlib.file_digest(f, 'sha256').hexdigest() == conf['installer_sha256'], 'The release installer has the wrong SHA-256'
out = root/'public-pages'
if out.exists():
    shutil.rmtree(out)
shutil.copytree(root/'site', out)
index = out/'index.html'
html = index.read_text(encoding='utf-8')
assert html.count(f'downloads/{installer.name}') == 2
html = html.replace(f'downloads/{installer.name}', f'https://github.com/{repo}/releases/download/v{version}/{installer.name}')
index.write_text(html, encoding='utf-8')
(out/'.nojekyll').touch()
print(f'Site prepared for https://{repo.split("/")[0]}.github.io/{repo.split("/")[1]}/')
