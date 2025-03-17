import os
import subprocess
import logging
import threading
import time
from queue import Queue
from .config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Queue and storage for tracking downloads
download_queue = Queue()
active_downloads = {}

# Files expire after this time
EXPIRATION_TIME = 600

# File where cookies live
cookie_file = "/app/cookies.txt" if not os.getenv("DEBUG", False) else "cookies.txt"


class DownloadTask:
    def __init__(self, url):
        self.url = url
        self.filename = None
        self.timestamp = time.time()


def worker():
    """Worker thread that processes downloads one at a time."""
    while True:
        task = download_queue.get()
        if task is None:
            break  # Stop worker

        logger.info(f"Processing URL: {task.url}")

        # Run yt-dlp
        output_template = os.path.join(config.DOWNLOAD_DIR, "%(title)s.%(ext)s")
        command = [
            "yt-dlp",
            task.url,
            "-o",
            output_template,
            "-f",
            "mp4",  # Force MP4 format
            "--merge-output-format",
            "mp4",
            "--remux-video",
            "mp4",  # Convert incompatible formats to MP4
            "--cookies",
            cookie_file,
        ]

        try:
            logger.info(f"Running command: {' '.join(command)}")
            subprocess.run(command, check=True)

            # Find the downloaded file
            files = os.listdir(config.DOWNLOAD_DIR)
            if not files:
                logger.error("No media files found.")
                continue

            task.filename = files[0]
            active_downloads[task.url] = task  # Track active download
            logger.info(f"Download complete: {task.filename}")

            # Cleanup expired files
            cleanup_old_files()

        except subprocess.CalledProcessError as e:
            logger.error(f"yt-dlp failed: {e}")


def cleanup_old_files():
    """Remove expired files from disk and tracking."""
    now = time.time()
    to_delete = [
        url
        for url, task in active_downloads.items()
        if now - task.timestamp > EXPIRATION_TIME
    ]

    for url in to_delete:
        task = active_downloads.pop(url, None)
        if task and task.filename:
            file_path = os.path.join(config.DOWNLOAD_DIR, task.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted expired file: {task.filename}")


# Start worker thread
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()
