import os
import secrets
import subprocess
import sys
from pathlib import Path

from flask import Flask, render_template, request, send_file, abort
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
STORAGE_DIR = BASE_DIR / "storage"
KEY_DIR = BASE_DIR / "keys"

for folder in (UPLOAD_DIR, STORAGE_DIR, KEY_DIR):
    folder.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
app.secret_key = secrets.token_hex(32)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/encrypt")
def encrypt_file():
    uploaded = request.files.get("file")

    if not uploaded or not uploaded.filename:
        return "Please choose a file first.", 400

    original_name = secure_filename(uploaded.filename)
    if not original_name:
        return "Invalid filename.", 400

    job_id = secrets.token_hex(12)
    input_path = UPLOAD_DIR / f"{job_id}_{original_name}"
    output_dir = STORAGE_DIR / job_id
    key_path = KEY_DIR / f"{job_id}.key"

    uploaded.save(input_path)

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(BASE_DIR / "secure_storage.py"),
                "encrypt",
                str(input_path),
                "--out",
                str(output_dir),
                "--key",
                str(key_path),
            ],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        if result.returncode != 0:
            app.logger.error("Encryption failed: %s", result.stderr)
            return "Encryption failed. Check the Flask terminal for details.", 500

        block_count = len(list(output_dir.glob("block_*.bin")))

        return render_template(
            "result.html",
            filename=original_name,
            job_id=job_id,
            block_count=block_count,
            message="Encryption completed successfully.",
        )
    finally:
        input_path.unlink(missing_ok=True)


@app.get("/download/<job_id>")
def download_encrypted(job_id):
    if not job_id.isalnum():
        abort(404)

    output_dir = STORAGE_DIR / job_id
    key_path = KEY_DIR / f"{job_id}.key"

    if not output_dir.is_dir() or not key_path.is_file():
        abort(404)

    archive_path = BASE_DIR / f"{job_id}_encrypted.zip"

    import zipfile

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in output_dir.iterdir():
            if item.is_file():
                archive.write(item, arcname=item.name)

    return send_file(
        archive_path,
        as_attachment=True,
        download_name="encrypted_blocks.zip",
    )


@app.errorhandler(413)
def file_too_large(_error):
    return "File too large. Maximum upload size is 20 MB.", 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
