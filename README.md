# Secure Cloud Storage

A Cloud Computing mini project demonstrating secure file storage using
Python, Flask, and AES-256-GCM encryption.

## Features

- Upload files through a Flask web interface.
- Split files into blocks before encryption.
- Encrypt each block using AES-256-GCM.
-
## Installation

Clone the repository and enter the project directory:

    git clone https://github.com/Ganesh-12-spec/secure-cloud-storage.git
    cd secure-cloud-storage

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

## Run the Website

Start the Flask application:

    python app.py

Open this address in your browser:

    http://127.0.0.1:5000

## Test File Encryption

Create a sample file containing non-sensitive test data.

Encrypt it:

    python secure_storage.py encrypt sample.txt --out encrypted_blocks --key secret.key

Decrypt it:

    python secure_storage.py decrypt --in-dir encrypted_blocks --key secret.key --out recovered.txt

Compare the original and recovered files:

    cmp sample.txt recovered.txt

No output from cmp means the files match.

## Security Notes

- Never commit encryption keys, credentials, or private files.
- Keep encryption keys separate from encrypted data.
- AES-GCM detects unauthorized changes to encrypted blocks.
- This project is an educational prototype, not a production-ready
  cloud storage service.
- AWS S3 and CloudFront deployment must be configured separately
  if cloud hosting is required.

## Project Status

Local encryption and the Flask web interface have been developed.
Cloud deployment is a separate step.
## Project Status

Local encryption and the Flask web interface have been developed.
Cloud deployment is a separate step.
