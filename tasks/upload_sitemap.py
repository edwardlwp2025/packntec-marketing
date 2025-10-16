# tasks/upload_sitemap.py
import os
from utils.sftp import sftp_upload

LOCAL = "reports/sitemap.xml"
REMOTE = os.environ.get("REMOTE_SITEMAP_PATH", "/home/USER/public_html/sitemap.xml")  # <-- change USER in the workflow env

host = os.getenv("SFTP_HOST")
user = os.getenv("SFTP_USER")
pwd  = os.getenv("SFTP_PASS")

if host and user and pwd:
    print(f"Uploading {LOCAL} -> {REMOTE}")
    sftp_upload(LOCAL, REMOTE)
    print("Sitemap uploaded.")
else:
    print("SFTP secrets not set; skipping upload.")
