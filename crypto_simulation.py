# === crypto_simulation.py ===
# Hybrid encryption + digital signature simulator with AES-GCM + RSA-3072
# UI: Tkinter | Crypto: PyCryptodome | Modular & commented | Secure metadata

from crypto_ui import CryptoApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()