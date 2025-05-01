![ultrapass2025-05-01 13-36-28](https://github.com/user-attachments/assets/81be8bdf-b585-47ff-be03-8fd676f3efde)

# 🔐 ULTRAPASS - Cyberpunk Edition

**ULTRAPASS** is a futuristic, stylish password generator built with PyQt5. It offers a glowing, cyberpunk-style GUI for generating secure passwords with real-time strength evaluation and customizable character options.

## 🚀 Features

- Cyberpunk-styled PyQt5 interface
- Password strength indicator based on entropy
- Three security presets: Low, Medium, High
- Custom character selection: uppercase, lowercase, numbers, symbols
- Password length customization (4–64 characters)
- Copy to clipboard with one click
- Save password to file (.txt)
- Animated "Powered By Roy Merlo V.2025" label

## 🖼️ Preview

*Coming soon – add screenshots here if you want*

## 🛠️ Requirements

- Python 3.x
- PyQt5
- pyperclip

Install dependencies via pip:

```bash
pip install pyqt5 pyperclip
📦 Usage
Run the app with:

bash
Copy
Edit
python NEWPASS.PY
📁 Options Explained
Security Level: Sets character complexity and length:

Low: Lowercase only, 8 characters

Medium: Mixed case and numbers, 12 characters

High: Full charset, 16 characters

Password Options: Choose which character types to include manually

Buttons:

Generate Password: Creates a password with selected options

Copy to Clipboard: Copies the generated password

Save to File: Saves the password and options to a .txt file

Reset: Resets the form to default (Medium security)

🔒 Password Strength
Strength is calculated using entropy and classified as:

🔴 Weak (entropy < 40)

🟡 Medium (entropy 40–80)

🟢 Strong (entropy > 80)

✨ Author
Developed by Roy Merlo
Version: 2025

