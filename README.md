# 🔐 Secure Cloud Storage

A secure file storage mini project built with **Python, Flask, and AES-256-GCM encryption** as part of a Cloud Computing project. The application demonstrates how files can be divided into smaller blocks, encrypted before storage, and decrypted when needed.

The project focuses on file confidentiality, authenticated encryption, and secure file handling through a simple web interface.

## ✨ Features

- **File Upload:** Upload files through a Flask-based web interface.
- **Block-Based Processing:** Split files into smaller blocks before encryption.
- **AES-256-GCM Encryption:** Encrypt file blocks using authenticated encryption.
- **Data Integrity Verification:** AES-GCM authentication detects unauthorized modification of encrypted data.
- **File Decryption:** Decrypt encrypted blocks and reconstruct the original file.
- **Local Web Interface:** Run the application locally using Flask.
- **Encryption Testing:** Compare the original file with the recovered file to verify correctness.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application and file upload interface |
| AES-256-GCM | Authenticated file encryption |
| Cryptography library | Cryptographic operations |
| HTML/CSS | Web interface |
| Git & GitHub | Version control and source code hosting |

## 🏗️ How It Works

The project follows a simple file encryption and recovery workflow.

```text
             User
              |
              v
      Flask Web Interface
              |
              v
        File Processing
              |
              v
        Split into Blocks
              |
              v
      AES-256-GCM Encryption
              |
              v
      Encrypted File Blocks
              |
              v
       Local Storage
```

For file recovery, the encrypted blocks are decrypted using the correct key and authentication data, then reconstructed into the original file.

### Encryption Workflow

1. The user selects a file for processing.
2. The file is divided into smaller blocks.
3. Each block is encrypted using AES-256-GCM.
4. The encrypted blocks are saved to the output directory.
5. The encryption key is stored separately from the encrypted data.

### Decryption Workflow

1. The application reads the encrypted blocks.
2. It uses the supplied encryption key to decrypt each block.
3. AES-GCM verifies the authenticity of each encrypted block.
4. The decrypted blocks are combined to reconstruct the original file.

## 📋 Prerequisites

Make sure the following are installed:

- Python 3
- pip
- Git

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ganesh-12-spec/secure-cloud-storage.git
cd secure-cloud-storage
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Linux / macOS / WSL**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Web Application

Start the Flask application:

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

The application will be available locally while the Flask development server is running.

## 🧪 Test File Encryption and Decryption

You can test the encryption workflow using a sample file containing non-sensitive data.

### 1. Create a sample file

```bash
echo "This is a secure storage test file." > sample.txt
```

### 2. Encrypt the file

```bash
python secure_storage.py encrypt sample.txt --out encrypted_blocks --key secret.key
```

This command encrypts the sample file and writes the encrypted output to `encrypted_blocks`, using the key file `secret.key`.

### 3. Decrypt the file

```bash
python secure_storage.py decrypt --in-dir encrypted_blocks --key secret.key --out recovered.txt
```

The decrypted output will be saved as `recovered.txt`.

### 4. Verify the recovered file

**Linux / macOS / WSL**

```bash
cmp sample.txt recovered.txt
```

If the command produces no output and exits successfully, the original and recovered files are identical.

**Windows PowerShell**

```powershell
(Get-FileHash sample.txt).Hash -eq (Get-FileHash recovered.txt).Hash
```

A result of `True` indicates that both files have matching SHA-256 hashes.

> Run these commands from the project directory with the virtual environment activated. The commands assume the CLI options shown above are supported by the current implementation.

## 🔒 Security Considerations

- **Key protection:** Never commit encryption keys, passwords, credentials, or sensitive files to GitHub.
- **Key separation:** Store encryption keys separately from encrypted file data.
- **Authenticated encryption:** AES-256-GCM provides confidentiality and integrity/authenticity verification when implemented correctly.
- **Nonce management:** Never reuse a nonce with the same AES-GCM key.
- **Authentication failures:** Reject encrypted blocks when their authentication tags cannot be verified.
- **Safe testing:** Use sample files without sensitive or personal information.
- **Production limitations:** This project is an educational prototype and has not been presented as a production-ready cloud storage service.

## ☁️ Cloud Deployment

The current project focuses on local file encryption and the Flask web interface.

Deployment to AWS S3, CloudFront, or other cloud services is a separate step and requires additional configuration. Cloud hosting, remote storage integration, and production security controls should not be considered implemented unless they have been configured and tested.

## 🎯 Project Objectives

- Understand the fundamentals of cloud storage security.
- Implement file encryption and decryption using Python.
- Explore block-based file processing.
- Demonstrate authenticated encryption using AES-GCM.
- Build a web interface for file operations.
- Verify file recovery by comparing original and decrypted data.

## 🔮 Future Improvements

- Integrate AWS S3 for encrypted object storage.
- Add secure user authentication and access control.
- Implement managed encryption-key storage.
- Add file integrity and recovery status reporting.
- Support larger files through streaming or bounded-memory processing.
- Add automated tests for encryption, decryption, and tamper detection.
- Deploy the application with HTTPS and production-grade server configuration.

## 👨‍💻 Author

**Ganesh Mhetre**

Computer Engineering Student | Python | Flask | Cloud Computing | Backend Development

GitHub: [Ganesh-12-spec](https://github.com/Ganesh-12-spec)

## 📄 License

No license has been specified yet. Add a `LICENSE` file if you intend to publish this project under an open-source license.
