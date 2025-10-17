# tasks/upload_sitemap_ftps.py
import os
from ftplib import FTP_TLS
from pathlib import Path

LOCAL = "reports/sitemap.xml"
# For FTP on GoDaddy, the web root is usually just /public_html
REMOTE = os.environ.get("REMOTE_SITEMAP_PATH", "/public_html/sitemap.xml")

host = os.environ["FTP_HOST"]
port = int(os.environ.get("FTP_PORT", "21"))
user = os.environ["FTP_USER"]
pwd  = os.environ["FTP_PASS"]

assert Path(LOCAL).exists(), f"Local file not found: {LOCAL}"

print(f"Connecting FTPS to {host}:{port} as {user}")
ftps = FTP_TLS()
ftps.connect(host, port, timeout=30)
ftps.auth()      # explicit TLS
ftps.prot_p()    # secure data channel
ftps.login(user, pwd)
ftps.set_pasv(True)

rem_dir, rem_file = os.path.split(REMOTE)
if rem_dir:
    ftps.cwd(rem_dir)

with open(LOCAL, "rb") as f:
    ftps.storbinary(f"STOR {rem_file}", f)

ftps.quit()
print("FTPS upload complete.")
