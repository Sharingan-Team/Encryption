# Secure Hybrid Encryption & Digital Signature

This project is an end-to-end cryptography application that combines hybrid encryption (AES-GCM + RSA-3072) and digital signatures to ensure data confidentiality and integrity. The user interface is built with Tkinter, and cryptographic operations are handled using the PyCryptodome library.

## Features

- **Hybrid Encryption**: Uses AES-GCM for data encryption and RSA-3072 for encrypting AES keys.
- **Digital Signature**: Generates and verifies digital signatures to ensure data integrity.
- **Intuitive User Interface**: Select files to encrypt or decrypt through a graphical interface.
- **Metadata Management**: Encrypted files include metadata to preserve the original file extension.

## Prerequisites

- Python 3.8 or higher
- PyCryptodome library

## Installation

1. Clone this repository:
    ```bash
    git clone <REPOSITORY_URL>
    cd <REPOSITORY_NAME>
    ```

2. Install the required dependencies:
    ```bash
    pip install pycryptodome
    ```

## Usage

1. Run the application:
    ```bash
    python crypto_simulation.py
    ```

2. A graphical interface will open with the following options:
    - **Select File to Encrypt**: Choose a file to encrypt.
    - **Select File to Decrypt**: Choose an encrypted file to decrypt.

3. Follow the on-screen instructions to encrypt or decrypt your files.

## Project Structure

- `crypto_simulation.py`: Main entry point of the application.
- `crypto_ui.py`: User interface built with Tkinter.
- `crypto_utils.py`: Utility functions for encryption and digital signatures.
- `README.md`: Project documentation.

## Security

- RSA keys are dynamically generated for each session.
- Encrypted files include a digital signature to ensure their integrity.
- Metadata is securely encoded to preserve file extensions.

## Contributions

Contributions are welcome! Please submit a pull request or open an issue to report bugs or suggest improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
