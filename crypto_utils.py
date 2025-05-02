# === crypto_utils.py ===
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import json
import base64

# Security constants
AES_KEY_SIZE = 32  # 256 bits
AES_NONCE_SIZE = 12  # 96 bits for GCM mode

# RSA key generation (2048 bits for better performance)
def generate_rsa_keys():
    """Generate a new RSA key pair (2048 bits for better performance)"""
    try:
        key = RSA.generate(2048)  # Changed from 3072 to 2048 for faster generation
        return key, key.publickey()
    except Exception as e:
        raise Exception(f"Key generation failed: {e}")

# Hash and sign data with RSA private key
def hash_and_sign(data, private_key):
    """Create SHA-256 hash of data and sign it with private key"""
    try:
        h = SHA256.new(data)
        signature = pkcs1_15.new(private_key).sign(h)
        return signature, h.hexdigest()
    except Exception as e:
        raise Exception(f"Hashing or signing failed: {e}")

# Verify signature using public key
def verify_signature(data, signature, public_key):
    """Verify that signature matches data using public key"""
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
    """Encrypt data using AES-GCM with random key and nonce"""
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
    """Decrypt data using AES-GCM with authentication tag verification"""
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(encrypted, tag)
    except Exception as e:
        raise Exception(f"AES-GCM decryption failed: {e}")

# Encrypt AES key with RSA
def encrypt_aes_key(aes_key, rsa_pub):
    """Encrypt symmetric AES key with asymmetric RSA public key"""
    try:
        cipher = PKCS1_OAEP.new(rsa_pub)
        return cipher.encrypt(aes_key)
    except Exception as e:
        raise Exception(f"Encrypting AES key with RSA failed: {e}")

# Decrypt AES key with RSA
def decrypt_aes_key(encrypted_key, rsa_priv):
    """Decrypt symmetric AES key with asymmetric RSA private key"""
    try:
        cipher = PKCS1_OAEP.new(rsa_priv)
        return cipher.decrypt(encrypted_key)
    except Exception as e:
        raise Exception(f"Decrypting AES key with RSA failed: {e}")

# Encode secure package with metadata
def build_encrypted_package(ciphertext, encrypted_key, nonce, tag, extension):
    """Create a JSON package containing all encrypted components and metadata"""
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
    """Parse JSON package and decode all encrypted components"""
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
