import os
from ftplib import FTP_TLS
from pathlib import Path
import sys

LOCAL = "reports/sitemap.xml"
REMOTE = os.environ.get("REMOTE_SITEMAP_PATH", "/public_html/sitemap.xml")

host = os.environ.get("FTP_HOST", "").strip()
user = os.environ.get("FTP_USER", "").strip()
pwd  = os.environ.get("FTP_PASS", "")
port = os.environ.get("FTP_PORT", "21").strip()
port = int(port) if port.isdigit() else 21

missing = [k for k,v in {"FTP_HOST":host,"FTP_USER":user,"FTP_PASS":pwd}.items() if not v]
if missing:
    print(f"Missing required env(s): {', '.join(missing)}")
    sys.exit(1)

assert Path(LOCAL).exists(), f"Local file not found: {LOCAL}"
print(f"Connecting FTPS to {host}:{port} as {user}")

ftps = FTP_TLS()
ftps.connect(host, port, timeout=30)
ftps.auth(); ftps.prot_p()
ftps.login(user, pwd)
ftps.set_pasv(True)

rem_dir, rem_file = os.path.split(REMOTE)
if rem_dir: ftps.cwd(rem_dir)

with open(LOCAL, "rb") as f:
    ftps.storbinary(f"STOR {rem_file}", f)
ftps.quit()
print("FTPS upload complete.")
