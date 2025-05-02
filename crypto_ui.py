# === crypto_ui.py ===
import os
import json
import webbrowser
import mimetypes
from tkinter import filedialog, messagebox, scrolledtext, Tk, Button, END
from crypto_utils import *

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Hybrid Encryption & Signature")

        self.log = scrolledtext.ScrolledText(root, width=90, height=35)
        self.log.pack(padx=10, pady=10)

        Button(root, text="Select File to Encrypt", command=self.encrypt_flow).pack(pady=5)
        Button(root, text="Select File to Decrypt", command=self.decrypt_flow).pack(pady=5)

    def log_step(self, title, content):
        self.log.insert(END, f"\n--- {title} ---\n{content}\n")
        self.log.see(END)

    def is_text_file(self, path):
        mime, _ = mimetypes.guess_type(path)
        return mime and mime.startswith("text")

    def encrypt_flow(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            with open(path, 'rb') as f:
                data = f.read()
            if self.is_text_file(path):
                self.log_step("Original File Content", data.decode(errors='ignore'))
            else:
                self.log_step("Notice", "Binary file detected. Content preview skipped.")
        except Exception as e:
            self.log_step("Error Reading File", str(e))
            messagebox.showerror("Error", f"Failed to read file: {e}")
            return

        ext = os.path.splitext(path)[1]
        if ext.lower() in ['.exe', '.bat', '.dll']:
            self.log_step("Blocked", f"Files with extension {ext} are not allowed.")
            messagebox.showwarning("Blocked", f"The file type {ext} is not supported for encryption.")
            return

        try:
            sender_priv, sender_pub = generate_rsa_keys()
            receiver_priv, receiver_pub = generate_rsa_keys()
        except Exception as e:
            self.log_step("Key Generation Error", str(e))
            return

        try:
            signature, hash_hex = hash_and_sign(data, sender_priv)
            self.log_step("SHA-256 Hash", hash_hex)
        except Exception as e:
            self.log_step("Hashing Error", str(e))
            return

        combined = data + b"::SIGNATURE::" + signature

        try:
            ciphertext, aes_key, nonce, tag = aes_encrypt(combined)
            encrypted_key = encrypt_aes_key(aes_key, receiver_pub)
            package = build_encrypted_package(ciphertext, encrypted_key, nonce, tag, ext)
        except Exception as e:
            self.log_step("Encryption Error", str(e))
            return

        out_path = filedialog.asksaveasfilename(defaultextension=".encpkg")
        if not out_path:
            return

        try:
            with open(out_path, 'w') as f:
                f.write(package)
            self.log_step("Output", f"Encrypted file saved: {out_path}")
        except Exception as e:
            self.log_step("Write Error", str(e))

        self.receiver_priv = receiver_priv
        self.sender_pub = sender_pub

    def decrypt_flow(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            with open(path, 'r') as f:
                package = f.read()
            parsed = parse_encrypted_package(package)
        except Exception as e:
            self.log_step("Parse Error", str(e))
            return

        try:
            aes_key = decrypt_aes_key(parsed['encrypted_key'], self.receiver_priv)
            plaintext = aes_decrypt(parsed['ciphertext'], aes_key, parsed['nonce'], parsed['tag'])
        except Exception as e:
            self.log_step("Decryption Error", str(e))
            return

        try:
            content, signature = plaintext.split(b"::SIGNATURE::")
            verified = verify_signature(content, signature, self.sender_pub)
        except Exception as e:
            self.log_step("Signature Verification Error", str(e))
            return

        ext = parsed['extension']
        if ext.lower().startswith("."):
            ext = ext[1:]

        out_path = filedialog.asksaveasfilename(defaultextension=f".{ext}")
        if not out_path:
            return

        try:
            with open(out_path, 'wb') as f:
                f.write(content)
            self.log_step("File Saved", f"Decrypted file saved: {out_path}")
            if self.is_text_file(out_path):
                self.log_step("Decrypted Content", content.decode(errors='ignore'))
            else:
                self.log_step("Notice", "Binary file preview skipped.")
            webbrowser.open(out_path)
        except Exception as e:
            self.log_step("Save Error", str(e))
