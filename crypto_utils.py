# === crypto_utils.py ===
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import json
import base64

AES_KEY_SIZE = 32
AES_NONCE_SIZE = 12

# RSA key generation (3072 bits)
def generate_rsa_keys():
    try:
        key = RSA.generate(3072)
        return key, key.publickey()
    except Exception as e:
        raise Exception(f"Key generation failed: {e}")

# Hash + sign file
def hash_and_sign(data, private_key):
    try:
        h = SHA256.new(data)
        signature = pkcs1_15.new(private_key).sign(h)
        return signature, h.hexdigest()
    except Exception as e:
        raise Exception(f"Hashing or signing failed: {e}")

# Verify signature
def verify_signature(data, signature, public_key):
    try:
        h = SHA256.new(data)
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
    except Exception as e:
        raise Exception(f"Verification failed: {e}")

# AES-GCM encrypt file content
def aes_encrypt(data):
    try:
        key = get_random_bytes(AES_KEY_SIZE)
        nonce = get_random_bytes(AES_NONCE_SIZE)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, key, nonce, tag
    except Exception as e:
        raise Exception(f"AES-GCM encryption failed: {e}")

# AES-GCM decrypt file content
def aes_decrypt(encrypted, key, nonce, tag):
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(encrypted, tag)
    except Exception as e:
        raise Exception(f"AES-GCM decryption failed: {e}")

# Encrypt AES key with RSA
def encrypt_aes_key(aes_key, rsa_pub):
    try:
        cipher = PKCS1_OAEP.new(rsa_pub)
        return cipher.encrypt(aes_key)
    except Exception as e:
        raise Exception(f"Encrypting AES key with RSA failed: {e}")

# Decrypt AES key with RSA
def decrypt_aes_key(encrypted_key, rsa_priv):
    try:
        cipher = PKCS1_OAEP.new(rsa_priv)
        return cipher.decrypt(encrypted_key)
    except Exception as e:
        raise Exception(f"Decrypting AES key with RSA failed: {e}")

# Encode secure package with metadata
def build_encrypted_package(ciphertext, encrypted_key, nonce, tag, extension):
    metadata = json.dumps({"ext": extension}).encode()
    metadata_encoded = base64.b64encode(metadata).decode()
    return json.dumps({
        "key": base64.b64encode(encrypted_key).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
        "data": base64.b64encode(ciphertext).decode(),
        "metadata": metadata_encoded
    })

# Decode secure package
def parse_encrypted_package(pkg):
    try:
        obj = json.loads(pkg)
        ext = ".txt"
        if "metadata" in obj:
            meta = json.loads(base64.b64decode(obj["metadata"]).decode())
            ext = meta.get("ext", ".txt")
        return {
            "encrypted_key": base64.b64decode(obj["key"]),
            "nonce": base64.b64decode(obj["nonce"]),
            "tag": base64.b64decode(obj["tag"]),
            "ciphertext": base64.b64decode(obj["data"]),
            "extension": ext
        }
    except Exception as e:
        raise Exception(f"Failed to parse encrypted package: {e}")

