# utils/sftp.py
import os, paramiko

def sftp_upload(local_path, remote_path):
    host = os.environ["SFTP_HOST"]       # your GoDaddy/cPanel SFTP host
    port = int(os.environ.get("SFTP_PORT","22"))
    user = os.environ["SFTP_USER"]
    pwd  = os.environ["SFTP_PASS"]

    t = paramiko.Transport((host, port))
    t.connect(username=user, password=pwd)
    s = paramiko.SFTPClient.from_transport(t)
    s.put(local_path, remote_path)       # e.g., /home/USER/public_html/sitemap.xml
    s.close(); t.close()
