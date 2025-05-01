import sys
import random
import string
import pyperclip
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QCheckBox, QSpinBox, QLineEdit,
    QVBoxLayout, QHBoxLayout, QGroupBox, QFileDialog, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class UltraPass(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ULTRAPASS - Cyberpunk Edition")
        self.setFixedSize(520, 620)
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f0f1a, stop:1 #1e1e2f);
                color: white;
                font-family: 'Courier New', monospace;
            }
            QGroupBox {
                border: 2px solid #7289da;
                border-radius: 8px;
                padding: 10px;
                color: #7289da;
            }
            QSpinBox, QComboBox, QLineEdit {
                background-color: #2a2a3d;
                border: 1px solid #5865f2;
                border-radius: 5px;
                padding: 5px;
                color: #ffffff;
            }
            QCheckBox::indicator {
                border: 2px solid #e74c3c;
                background: #2a2a3d;
                width: 16px;
                height: 16px;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8, fx:0.5, fy:0.5, stop:0 #e74c3c, stop:1 #2a2a3d);
            }
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Titolo con effetto glow
        self.title = QLabel("ULTRAPASS")
        self.title.setFont(QFont("Courier New", 28, QFont.Bold))
        self.title.setStyleSheet("color: #00ffff; text-shadow: 0 0 10px #00ffff;")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # Powered By con effetto pulsante
        self.powered_label = QLabel("Powered By Roy Merlo V.2025")
        self.powered_label.setFont(QFont("Arial", 12))
        self.powered_label.setStyleSheet("color: rgba(255, 0, 127, 200); text-shadow: 0 0 5px #ff007f;")
        self.powered_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.powered_label)

        # Effetto pulsazione per il powered label
        self.pulse_animation()
        
        # Livello di Sicurezza
        level_group = QGroupBox("Livello di Sicurezza")
        level_layout = QHBoxLayout()
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Basso", "Medio", "Alto"])
        self.level_combo.currentIndexChanged.connect(self.update_from_level)
        level_layout.addWidget(self.level_combo)
        level_group.setLayout(level_layout)
        main_layout.addWidget(level_group)

        # Opzioni Password
        options_group = QGroupBox("Opzioni Password")
        options_layout = QVBoxLayout()

        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 64)
        self.length_spin.setValue(12)
        self.length_spin.setPrefix("Lunghezza: ")
        options_layout.addWidget(self.length_spin)

        self.upper_check = QCheckBox("Maiuscole (A-Z)")
        self.upper_check.setChecked(True)
        options_layout.addWidget(self.upper_check)

        self.lower_check = QCheckBox("Minuscole (a-z)")
        self.lower_check.setChecked(True)
        options_layout.addWidget(self.lower_check)

        self.digits_check = QCheckBox("Numeri (0-9)")
        self.digits_check.setChecked(True)
        options_layout.addWidget(self.digits_check)

        self.symbols_check = QCheckBox("Simboli (!@#$%^&*)")
        self.symbols_check.setChecked(True)
        options_layout.addWidget(self.symbols_check)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # Campo password con glow
        self.password_line = QLineEdit()
        self.password_line.setReadOnly(True)
        self.password_line.setStyleSheet("""
            font-size: 18px;
            padding: 8px;
            border: 2px solid #5865f2;
            border-radius: 8px;
            background-color: #1e1e2f;
            color: #00ffff;
            text-align: center;
            box-shadow: 0 0 10px #5865f2;
        """)
        main_layout.addWidget(self.password_line)

        # Indicatore di sicurezza
        self.strength_label = QLabel("Sicurezza: -")
        self.strength_label.setStyleSheet("font-size: 14px; text-shadow: 0 0 5px #00ffff;")
        main_layout.addWidget(self.strength_label)

        # Pulsanti con effetti interattivi
        btn_layout = QHBoxLayout()
        for text, color, hover_color in [
            ("Genera Password", "#7289da", "#99b3ff"),
            ("Copia Appunti", "#5865f2", "#7d8bff"),
            ("Salva su File", "#f1c40f", "#ffdd57"),
            ("Reset", "#e74c3c", "#ff6b54")
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                    box-shadow: 0 0 8px {color};
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                    box-shadow: 0 0 12px {hover_color};
                }}
            """)
            if text == "Genera Password":
                btn.clicked.connect(self.generate_password)
            elif text == "Copia Appunti":
                btn.clicked.connect(self.copy_to_clipboard)
            elif text == "Salva su File":
                btn.clicked.connect(self.save_to_file)
            elif text == "Reset":
                btn.clicked.connect(self.reset_form)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.update_from_level()

    def pulse_animation(self):
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.toggle_powered_glow)
        self.pulse_timer.start(800)
        self.glow_on = False

    def toggle_powered_glow(self):
        if self.glow_on:
            self.powered_label.setStyleSheet("color: rgba(255, 0, 127, 200); text-shadow: 0 0 5px #ff007f;")
        else:
            self.powered_label.setStyleSheet("color: rgba(255, 0, 127, 255); text-shadow: 0 0 8px #ff007f;")
        self.glow_on = not self.glow_on

    def update_from_level(self):
        level = self.level_combo.currentText()
        if level == "Basso":
            self.length_spin.setValue(8)
            self.upper_check.setChecked(False)
            self.lower_check.setChecked(True)
            self.digits_check.setChecked(False)
            self.symbols_check.setChecked(False)
        elif level == "Medio":
            self.length_spin.setValue(12)
            self.upper_check.setChecked(True)
            self.lower_check.setChecked(True)
            self.digits_check.setChecked(True)
            self.symbols_check.setChecked(False)
        else:
            self.length_spin.setValue(16)
            self.upper_check.setChecked(True)
            self.lower_check.setChecked(True)
            self.digits_check.setChecked(True)
            self.symbols_check.setChecked(True)

    def generate_password(self):
        pools = []
        if self.upper_check.isChecked():
            pools.append(string.ascii_uppercase)
        if self.lower_check.isChecked():
            pools.append(string.ascii_lowercase)
        if self.digits_check.isChecked():
            pools.append(string.digits)
        if self.symbols_check.isChecked():
            pools.append("!@#$%^&*()_+-=[]{}|;:,.<>?")

        if not pools:
            QMessageBox.warning(self, "Errore", "Seleziona almeno un tipo di carattere!")
            return

        length = self.length_spin.value()
        required = len(pools)

        if length < required:
            self.length_spin.setValue(required)
            length = required

        password = [random.choice(pool) for pool in pools]
        while len(password) < length:
            password.append(random.choice(random.choice(pools)))
        random.shuffle(password)
        final_password = ''.join(password)

        self.password_line.setText(final_password)
        self.check_strength(final_password, pools)

    def check_strength(self, password, pools):
        charset_size = len(''.join(set(''.join(pools))))
        entropy = len(password) * math.log2(charset_size)
        if entropy < 40:
            strength = "Debole 🔴"
            color = "#e74c3c"
        elif entropy < 80:
            strength = "Medio 🟡"
            color = "#f1c40f"
        else:
            strength = "Forte 🟢"
            color = "#2ecc71"
        self.strength_label.setText(f"Sicurezza: {strength}")
        self.strength_label.setStyleSheet(f"color: {color}; font-size: 14px;")

    def copy_to_clipboard(self):
        if self.password_line.text():
            pyperclip.copy(self.password_line.text())
            QMessageBox.information(self, "Copiato", "Password copiata negli appunti!")

    def save_to_file(self):
        if not self.password_line.text():
            return
        path, _ = QFileDialog.getSaveFileName(self, "Salva Password", "", "Testo (*.txt);;Tutti i file (*)")
        if path:
            with open(path, 'w') as f:
                f.write(f"Password: {self.password_line.text()}\n")
                f.write(f"Lunghezza: {self.length_spin.value()}\n")
                f.write(f"Caratteri: {'Maiuscole' if self.upper_check.isChecked() else ''}, "
                        f"{'Minuscole' if self.lower_check.isChecked() else ''}, "
                        f"{'Numeri' if self.digits_check.isChecked() else ''}, "
                        f"{'Simboli' if self.symbols_check.isChecked() else ''}")
            QMessageBox.information(self, "Salvato", "Password salvata correttamente!")

    def reset_form(self):
        self.length_spin.setValue(12)
        self.upper_check.setChecked(True)
        self.lower_check.setChecked(True)
        self.digits_check.setChecked(True)
        self.symbols_check.setChecked(True)
        self.password_line.clear()
        self.strength_label.setText("Sicurezza: -")
        self.level_combo.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UltraPass()
    window.show()
    sys.exit(app.exec_())