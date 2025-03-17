import os
import subprocess
from celery import shared_task
from .config import config


@shared_task(bind=True)
def download_media(self, url):
    output_template = os.path.join(config.DOWNLOAD_DIR, "%(title)s.%(ext)s")

    command = ["yt-dlp", url, "-o", output_template]

    try:
        subprocess.run(command, check=True)

        # Find the downloaded file
        files = os.listdir(config.DOWNLOAD_DIR)
        if not files:
            return {"status": "error", "message": "No media found"}

        return {"status": "done", "file": files[0]}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
