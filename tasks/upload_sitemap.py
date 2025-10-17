# tasks/upload_sitemap.py
from pathlib import Path
import os, sys

# Ensure repo root is on sys.path so "utils" can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Try to import the helper; if not found, fall back to a tiny inline uploader
try:
    from utils.sftp import sftp_upload  # expects paramiko installed
except ModuleNotFoundError:
    import paramiko
    def sftp_upload(local_path, remote_path):
        host = os.environ["SFTP_HOST"]
        port = int(os.environ.get("SFTP_PORT", "22"))
        user = os.environ["SFTP_USER"]
        pwd  = os.environ["SFTP_PASS"]
        t = paramiko.Transport((host, port))
        t.connect(username=user, password=pwd)
        s = paramiko.SFTPClient.from_transport(t)
        s.put(local_path, remote_path)
        s.close(); t.close()

LOCAL  = "reports/sitemap.xml"
REMOTE = os.environ.get("REMOTE_SITEMAP_PATH", "/home/z09esrwccxu0/public_html/sitemap.xml")  # replace USER via workflow env

if all(os.getenv(k) for k in ("SFTP_HOST","SFTP_USER","SFTP_PASS")):
    print(f"Uploading {LOCAL} -> {REMOTE}")
    sftp_upload(LOCAL, REMOTE)
    print("Sitemap uploaded.")
else:
    print("SFTP secrets not set; skipping upload.")
