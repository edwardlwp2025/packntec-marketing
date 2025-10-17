# tasks/upload_sitemap.py  (no utils import)
import os, paramiko

LOCAL  = "reports/sitemap.xml"
REMOTE = os.environ.get("REMOTE_SITEMAP_PATH", "/home/z09esrwccxu0/public_html/sitemap.xml")  # overridden in workflow

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

if all(os.getenv(k) for k in ("SFTP_HOST","SFTP_USER","SFTP_PASS")):
    print(f"Uploading {LOCAL} -> {REMOTE}")
    sftp_upload(LOCAL, REMOTE)
    print("Sitemap uploaded.")
else:
    print("SFTP secrets not set; skipping upload.")
