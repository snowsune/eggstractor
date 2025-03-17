from flask import request, jsonify, send_from_directory
from . import app, celery
from .tasks import download_media
from .config import config
import os


@app.route("/extract", methods=["POST"])
def extract_media():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    task = celery.send_task("app.tasks.download_media", args=[url])
    return jsonify({"task_id": task.id}), 202


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({"status": task.state, "result": task.result})


@app.route("/result/<filename>", methods=["GET"])
def get_result(filename):
    return send_from_directory(config.DOWNLOAD_DIR, filename)
