import argparse
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BLOCK_SIZE = 1024 * 1024  # 1 MiB per block
MAGIC = b"SECUREBLOCK1"


def encrypt_file(input_path, output_dir, key_path):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    key_path = Path(key_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if key_path.exists():
        raise FileExistsError(
            f"Key already exists: {key_path}. Choose a new key path."
        )
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    key_path.parent.mkdir(parents=True, exist_ok=True)

    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    metadata = {
        "format": "SECUREBLOCK1",
        "original_name": input_path.name,
        "block_size": BLOCK_SIZE,
        "blocks": [],
    }

    try:
        with input_path.open("rb") as source:
            index = 0
            while True:
                plaintext = source.read(BLOCK_SIZE)
                if not plaintext:
                    break

                nonce = os.urandom(12)
                aad = f"block:{index}".encode()
                ciphertext = aes.encrypt(nonce, plaintext, aad)

                block_name = f"block_{index:05d}.bin"
                block_path = output_dir / block_name
                block_path.write_bytes(MAGIC + nonce + ciphertext)

                metadata["blocks"].append({
                    "file": block_name,
                    "index": index,
                })
                index += 1

        if not metadata["blocks"]:
            nonce = os.urandom(12)
            ciphertext = aes.encrypt(nonce, b"", b"block:0")
            block_path = output_dir / "block_00000.bin"
            block_path.write_bytes(MAGIC + nonce + ciphertext)
            metadata["blocks"].append({
                "file": block_path.name,
                "index": 0,
            })

        key_path.write_bytes(key)
        try:
            key_path.chmod(0o600)
        except OSError:
            pass

        (output_dir / "manifest.json").write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

    except Exception:
        # Do not leave a partially generated key or block set behind.
        if key_path.exists():
            key_path.unlink()
        raise

    print(f"Encryption successful: {input_path.name}")
    print(f"Encrypted blocks: {len(metadata['blocks'])}")
    print(f"Encrypted data directory: {output_dir}")
    print(f"Key saved separately to: {key_path}")
    print("Keep the key private and backed up securely.")


def decrypt_file(input_dir, key_path, output_path):
    input_dir = Path(input_dir)
    key_path = Path(key_path)
    output_path = Path(output_path)

    manifest_path = input_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    if not key_path.is_file():
        raise FileNotFoundError(f"Key not found: {key_path}")
    if output_path.exists():
        raise FileExistsError(
            f"Output already exists: {output_path}. Choose another path."
        )

    metadata = json.loads(manifest_path.read_text(encoding="utf-8"))
    if metadata.get("format") != "SECUREBLOCK1":
        raise ValueError("Unsupported file format")

    key = key_path.read_bytes()
    if len(key) != 32:
        raise ValueError("Invalid AES-256 key length")

    aes = AESGCM(key)
    blocks = metadata.get("blocks", [])
    if not blocks:
        raise ValueError("Manifest contains no blocks")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(output_path.name + ".partial")

    try:
        with temporary_path.open("xb") as destination:
            for expected_index, item in enumerate(blocks):
                if item.get("index") != expected_index:
                    raise ValueError("Invalid block order in manifest")

                block_path = input_dir / item["file"]
                raw = block_path.read_bytes()

                if not raw.startswith(MAGIC) or len(raw) < len(MAGIC) + 12 + 16:
                    raise ValueError(f"Invalid encrypted block: {block_path.name}")

                offset = len(MAGIC)
                nonce = raw[offset:offset + 12]
                ciphertext = raw[offset + 12:]
                aad = f"block:{expected_index}".encode()

                # AES-GCM verifies integrity before returning plaintext.
                plaintext = aes.decrypt(nonce, ciphertext, aad)
                destination.write(plaintext)

        temporary_path.replace(output_path)

    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        raise

    print(f"Decryption successful: {output_path}")
    print(f"Blocks restored: {len(blocks)}")


def main():
    parser = argparse.ArgumentParser(
        description="Split files into blocks and encrypt them with AES-256-GCM."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    enc = commands.add_parser("encrypt", help="Encrypt and segment a file")
    enc.add_argument("input", help="File to encrypt")
    enc.add_argument("--out", default="encrypted_blocks", help="Output directory")
    enc.add_argument("--key", default="secret.key", help="Path for encryption key")

    dec = commands.add_parser("decrypt", help="Decrypt and reassemble a file")
    dec.add_argument("--in-dir", default="encrypted_blocks", help="Encrypted data directory")
    dec.add_argument("--key", default="secret.key", help="Path to encryption key")
    dec.add_argument("--out", required=True, help="Path for restored file")

    args = parser.parse_args()

    try:
        if args.command == "encrypt":
            encrypt_file(args.input, args.out, args.key)
        else:
            decrypt_file(args.in_dir, args.key, args.out)
    except Exception as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
