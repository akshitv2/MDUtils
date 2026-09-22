import argparse
import base64
import hashlib
import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16) -> tuple[bytes, bytes]:
    """Derive Key and IV matching OpenSSL EVP_BytesToKey used by CryptoJS."""
    derived = b""
    block = b""
    while len(derived) < (key_len + iv_len):
        block = hashlib.md5(block + password + salt).digest()
        derived += block
    return derived[:key_len], derived[key_len : key_len + iv_len]


def encrypt_data(data: bytes, key_str: str) -> str:
    """Encrypt raw bytes into a CryptoJS-compatible OpenSSL Base64 string."""
    salt = os.urandom(8)
    key, iv = bytes_to_key(key_str.encode("utf-8"), salt)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size, style="pkcs7")
    ciphertext = cipher.encrypt(padded_data)

    payload = b"Salted__" + salt + ciphertext
    return base64.b64encode(payload).decode("utf-8")


def process_folder(input_dir: str, output_dir: str, secret_key: str) -> None:
    in_path = Path(input_dir).resolve()
    out_path = Path(output_dir).resolve()

    if not in_path.exists() or not in_path.is_dir():
        raise ValueError(f"Input directory does not exist or is not a folder: {in_path}")

    for file_path in in_path.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(in_path)
            target_file = out_path / rel_path

            target_file.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "rb") as f:
                raw_bytes = f.read()

            encrypted_str = encrypt_data(raw_bytes, secret_key)

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(encrypted_str)

            print(f"Encrypted: {rel_path} -> {target_file}")


if __name__ == ".__main__":
    parser = argparse.ArgumentParser(description="Recursively encrypt folder assets for CryptoJS HTML viewer.")
    parser.add_argument("-i", "--input", required=True, help="Path to input directory")
    parser.add_argument("-o", "--output", required=True, help="Path to output directory")
    parser.add_argument("-k", "--key", required=True, help="Encryption secret key")

    args = parser.parse_args()
    process_folder(args.input, args.output, args.key)

if __name__ == "__main__":
    process_folder("F:\Git\MDUtils\sample_mds", "F:\Git\MDUtils\sample_encrypted_mds", "")