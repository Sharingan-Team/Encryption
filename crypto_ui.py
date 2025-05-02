# === crypto_ui.py ===
import os
import json
import webbrowser
import mimetypes
import time
import threading
from tkinter import filedialog, messagebox, scrolledtext, Tk, Button, Frame, Label, END
from tkinter import ttk
import tkinter as tk
from crypto_utils import *

class CryptoApp:
    def __init__(self, root):
        """Initialize the Crypto Application UI"""
        self.root = root
        self.root.title("Secure Hybrid Encryption & Signature")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # For Windows systems, try to use colored buttons
        self.root.tk_setPalette(background='#f5f5f5')
        
        # Set modern theme and style
        self.setup_styles()
        
        # Create main frames
        self.create_header_frame()
        self.create_main_frame()
        self.create_footer_frame()
        
        # Initialize instance variables to store keys
        self.receiver_priv = None
        self.sender_pub = None

    def setup_styles(self):
        """Configure UI styles for a modern look and feel"""
        self.style = ttk.Style()
        
        # Configure colors
        bg_color = "#f5f5f5"
        accent_color = "#3498db"
        
        # Button colors as requested
        encrypt_color = "#3498db"  # Blue for encryption
        decrypt_color = "#2ecc71"  # Green for decryption
        clear_color = "#e74c3c"    # Red for clear log
        
        self.root.configure(bg=bg_color)
        
        # Configure ttk styles with Inter font
        self.style.configure("TFrame", background=bg_color)
        
        # Make buttons have full-color backgrounds instead of just borders
        if 'vista' in self.style.theme_names():
            self.style.theme_use('vista')
        
        # Custom button styles with different colors
        self.style.configure("Encrypt.TButton", 
                             background=encrypt_color,
                             foreground="white", 
                             font=("Inter", 10, "bold"),
                             padding=10)
        
        self.style.map("Encrypt.TButton",
                      background=[('active', '#2980b9'), ('pressed', '#2980b9')])
                             
        self.style.configure("Decrypt.TButton", 
                             background=decrypt_color,
                             foreground="white",
                             font=("Inter", 10, "bold"),
                             padding=10)
        
        self.style.map("Decrypt.TButton",
                      background=[('active', '#27ae60'), ('pressed', '#27ae60')])
                             
        self.style.configure("Clear.TButton", 
                             background=clear_color,
                             foreground="white",
                             font=("Inter", 10, "bold"), 
                             padding=10)
        
        self.style.map("Clear.TButton",
                      background=[('active', '#c0392b'), ('pressed', '#c0392b')])
                             
        self.style.configure("TLabel", 
                             background=bg_color, 
                             font=("Inter", 10))
                             
        self.style.configure("Header.TLabel", 
                             background=accent_color, 
                             foreground="white",
                             font=("Inter", 16, "bold"),
                             padding=10)

    def create_header_frame(self):
        """Create the header with application title"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(0, 10))
        
        header_label = ttk.Label(header_frame, 
                                text="Secure File Encryption System", 
                                style="Header.TLabel")
        header_label.pack(fill="x")

    def create_main_frame(self):
        """Create the main application area with log and buttons"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create log area for operation status
        log_label = ttk.Label(main_frame, text="Operation Log:")
        log_label.pack(anchor="w", pady=(0, 5))
        
        # Create scrolled text area with modern styling using Inter font
        self.log = scrolledtext.ScrolledText(main_frame, 
                                            width=80, 
                                            height=25,
                                            font=("Inter", 10),
                                            background="#ffffff",
                                            borderwidth=1,
                                            relief="solid")
        self.log.pack(fill="both", expand=True, pady=(0, 10))

    def create_footer_frame(self):
        """Create footer with action buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create action buttons with fully colored backgrounds
        # Use regular tkinter buttons instead of ttk for more consistent coloring across platforms
        encrypt_btn = Button(button_frame, 
                            text="Encrypt File", 
                            command=self.encrypt_flow,
                            bg="#3498db",
                            fg="white",
                            font=("Inter", 10, "bold"),
                            padx=15,
                            pady=8,
                            relief="flat",
                            activebackground="#2980b9",
                            activeforeground="white",
                            borderwidth=0)
        encrypt_btn.pack(side="left", padx=(0, 10))
        
        decrypt_btn = Button(button_frame, 
                            text="Decrypt File", 
                            command=self.decrypt_flow,
                            bg="#2ecc71",
                            fg="white",
                            font=("Inter", 10, "bold"),
                            padx=15,
                            pady=8,
                            relief="flat",
                            activebackground="#27ae60",
                            activeforeground="white",
                            borderwidth=0)
        decrypt_btn.pack(side="left")
        
        # Add clear log button (red)
        clear_btn = Button(button_frame, 
                          text="Clear Log", 
                          command=self.clear_log,
                          bg="#e74c3c",
                          fg="white",
                          font=("Inter", 10, "bold"),
                          padx=15,
                          pady=8,
                          relief="flat",
                          activebackground="#c0392b",
                          activeforeground="white",
                          borderwidth=0)
        clear_btn.pack(side="right")
    
    def clear_log(self):
        """Clear the log area"""
        self.log.delete(1.0, END)
        
    def log_step(self, title, content):
        """Log operation steps to the UI"""
        self.log.insert(END, f"\n--- {title} ---\n{content}\n")
        self.log.see(END)  # Auto-scroll to latest entry

    def is_text_file(self, path):
        """Check if a file is a text file based on MIME type"""
        mime, _ = mimetypes.guess_type(path)
        return mime and mime.startswith("text")

    def encrypt_flow(self):
        """Handle complete file encryption workflow"""
        # Select file to encrypt
        path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not path:
            return
            
        try:
            # Read selected file
            file_name = os.path.basename(path)
            with open(path, 'rb') as f:
                data = f.read()
            self.log_step("Selected File", f"File: {file_name}\nSize: {len(data)} bytes")
            
            # File type validation
            ext = os.path.splitext(path)[1]
            if ext.lower() in ['.exe', '.bat', '.dll']:
                self.log_step("Security Check", f"Files with extension {ext} are not allowed.")
                messagebox.showwarning("Security Check", f"The file type {ext} is not supported for encryption.")
                return
        except Exception as e:
            self.log_step("Error Reading File", str(e))
            messagebox.showerror("Error", f"Failed to read file: {e}")
            return

        # Use threading to prevent UI freezing during encryption
        def encryption_task():
            try:
                # Step 1: Generate RSA key pairs
                self.log_step("Generating Keys", "Creating RSA key pairs...")
                sender_priv, sender_pub = generate_rsa_keys()
                receiver_priv, receiver_pub = generate_rsa_keys()
                self.log_step("Key Generation", "RSA keys created successfully")
                
                # Step 2: Create digital signature
                self.log_step("Creating Signature", "Generating SHA-256 hash and RSA signature...")
                signature, hash_hex = hash_and_sign(data, sender_priv)
                self.log_step("File Hash", f"SHA-256: {hash_hex}")
                
                # Step 3: Combine data with signature
                combined = data + b"::SIGNATURE::" + signature
                
                # Step 4: Encrypt with AES-GCM
                self.log_step("Encrypting", "Encrypting with AES-256-GCM...")
                ciphertext, aes_key, nonce, tag = aes_encrypt(combined)
                encrypted_key = encrypt_aes_key(aes_key, receiver_pub)
                package = build_encrypted_package(ciphertext, encrypted_key, nonce, tag, ext)
                self.log_step("Encryption Complete", f"Original size: {len(data)} bytes\nEncrypted size: {len(package)} bytes")
                
                # Step 5: Save encrypted package
                self.root.after(0, lambda: self.finish_encryption(package, receiver_priv, sender_pub))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_step("Encryption Error", str(e)))
        
        # Start encryption in a separate thread
        threading.Thread(target=encryption_task, daemon=True).start()
    
    def finish_encryption(self, package, receiver_priv, sender_pub):
        """Complete the encryption process by saving the package file"""
        out_path = filedialog.asksaveasfilename(
            title="Save Encrypted File",
            defaultextension=".encpkg",
            filetypes=[("Encrypted Package", "*.encpkg")]
        )
        if not out_path:
            return

        try:
            with open(out_path, 'w') as f:
                f.write(package)
            self.log_step("File Saved", f"Encrypted file saved: {os.path.basename(out_path)}")
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            self.log_step("Write Error", str(e))

        # Store keys for decryption
        self.receiver_priv = receiver_priv
        self.sender_pub = sender_pub

    def decrypt_flow(self):
        """Handle complete file decryption workflow"""
        # Check if keys are available
        if not hasattr(self, 'receiver_priv') or not hasattr(self, 'sender_pub'):
            self.log_step("Key Error", "Decryption keys not available. Please encrypt a file first.")
            messagebox.showwarning("Keys Unavailable", "Please encrypt a file first to generate keys.")
            return
            
        # Select encrypted file
        path = filedialog.askopenfilename(
            title="Select File to Decrypt",
            filetypes=[("Encrypted Package", "*.encpkg"), ("All Files", "*.*")]
        )
        if not path:
            return

        # Step 1: Read and parse encrypted package
        try:
            self.log_step("Reading Package", f"Opening: {os.path.basename(path)}")
            with open(path, 'r') as f:
                package = f.read()
            parsed = parse_encrypted_package(package)
            self.log_step("Package Parsed", f"Extension: {parsed['extension']}")
        except Exception as e:
            self.log_step("Parse Error", str(e))
            messagebox.showerror("Parse Error", f"Invalid encrypted package: {e}")
            return

        # Use threading to prevent UI freezing during decryption
        def decryption_task():
            try:
                # Step 2: Decrypt AES key and content
                self.log_step("Decrypting", "Decrypting AES key with RSA private key...")
                aes_key = decrypt_aes_key(parsed['encrypted_key'], self.receiver_priv)
                self.log_step("Decrypting", "Decrypting content with AES-GCM...")
                plaintext = aes_decrypt(parsed['ciphertext'], aes_key, parsed['nonce'], parsed['tag'])
                
                # Step 3: Verify signature
                self.log_step("Verifying", "Checking digital signature...")
                content, signature = plaintext.split(b"::SIGNATURE::")
                verified = verify_signature(content, signature, self.sender_pub)
                
                if verified:
                    self.log_step("Signature Valid", "Digital signature verification successful!")
                    # Call finish_decryption on the main thread
                    ext = parsed['extension']
                    self.root.after(0, lambda: self.finish_decryption(content, ext))
                else:
                    self.root.after(0, lambda: self.log_step("Signature Invalid", "WARNING: Digital signature verification FAILED!"))
                    self.root.after(0, lambda: messagebox.showwarning("Security Warning", "Digital signature verification failed!"))
            except Exception as e:
                self.root.after(0, lambda: self.log_step("Decryption Error", str(e)))
                self.root.after(0, lambda: messagebox.showerror("Decryption Failed", str(e)))
                
        # Start decryption in a separate thread
        threading.Thread(target=decryption_task, daemon=True).start()
    
    def finish_decryption(self, content, ext):
        """Complete the decryption process by saving the decrypted file"""
        if ext.lower().startswith("."):
            ext = ext[1:]
            
        out_path = filedialog.asksaveasfilename(
            title="Save Decrypted File",
            defaultextension=f".{ext}",
            filetypes=[(f"{ext.upper()} File", f"*.{ext}"), ("All Files", "*.*")]
        )
        if not out_path:
            return

        try:
            with open(out_path, 'wb') as f:
                f.write(content)
            self.log_step("File Saved", f"Decrypted file saved: {os.path.basename(out_path)}")
            messagebox.showinfo("Success", "File decrypted and signature verified successfully!")
            
            # Open file with default application
            webbrowser.open(out_path)
        except Exception as e:
            self.log_step("Save Error", str(e))
            messagebox.showerror("Save Error", f"Failed to save decrypted file: {e}")
