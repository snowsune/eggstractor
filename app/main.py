import os
import logging

from flask import request, jsonify, send_from_directory
from . import app
from .tasks import download_queue, active_downloads, DownloadTask, config


@app.route("/extract", methods=["POST"])
def extract_media():
    data = request.json
    url = data.get("url")

    if not url:
        return (
            jsonify(
                {
                    "error": "Missing URL",
                    "version": os.getenv("BUILD_HASH", ""),
                }
            ),
            400,
        )

    # Check if already in progress
    if url in active_downloads:
        return jsonify(
            {
                "status": "IN_PROGRESS",
                "version": os.getenv("BUILD_HASH", ""),
            }
        )

    # Add to queue
    task = DownloadTask(url)
    download_queue.put(task)

    return jsonify(
        {
            "status": "QUEUED",
            "version": os.getenv("BUILD_HASH", ""),
        }
    )


@app.route("/status", methods=["GET"])
def check_status():
    url = request.args.get("url")

    if url in active_downloads:
        task = active_downloads[url]
        return jsonify(
            {
                "status": "DONE",
                "file": task.filename,
                "version": os.getenv("BUILD_HASH", ""),
            }
        )

    return jsonify({"status": "PENDING"})
