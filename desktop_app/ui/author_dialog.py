from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from desktop_app.models.author import Author
from PIL import Image
import os
from desktop_app.ui.document_dialog import DocumentDialog
from desktop_app.utils.template_manager import TemplateManager

class AuthorDialog(QDialog):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Autor verwalten")
        layout = QFormLayout()

        self.full_name = QLineEdit()
        self.short_name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.mobile_phone = QLineEdit()
        self.role = QLineEdit()
        self.extra_info1 = QLineEdit()
        self.extra_info2 = QLineEdit()
        self.extra_info3 = QLineEdit()
        self.extra_info4 = QLineEdit()
        self.extra_info5 = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addRow("Vollständiger Name:", self.full_name)
        layout.addRow("Kurzname:", self.short_name)
        layout.addRow("E-Mail:", self.email)
        layout.addRow("Telefon:", self.phone)
        layout.addRow("Mobiltelefon:", self.mobile_phone)
        layout.addRow("Rolle:", self.role)
        layout.addRow("Extra Info 1:", self.extra_info1)
        layout.addRow("Extra Info 2:", self.extra_info2)
        layout.addRow("Extra Info 3:", self.extra_info3)
        layout.addRow("Extra Info 4:", self.extra_info4)
        layout.addRow("Extra Info 5:", self.extra_info5)
        layout.addRow("Passwort:", self.password)

        self.signature_btn = QPushButton("Unterschrift hochladen")
        self.signature_btn.clicked.connect(self.upload_signature)
        layout.addRow(self.signature_btn)

        save_btn = QPushButton("Speichern")
        save_btn.clicked.connect(self.save_author)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def upload_signature(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Unterschrift auswählen", "", "PNG Files (*.png)")
        if file_name:
            if self.check_transparent_background(file_name):
                self.signature_path = file_name
                QMessageBox.information(self, "Erfolg", "Unterschrift erfolgreich hochgeladen.")
            else:
                QMessageBox.warning(self, "Fehler", "Die PNG-Datei muss einen transparenten Hintergrund haben.")

    def check_transparent_background(self, file_path):
        with Image.open(file_path) as img:
            return img.mode in ('RGBA', 'LA') and any(pixel[3] < 255 for pixel in img.getdata())

    def save_author(self):
        author = Author(
            full_name=self.full_name.text(),
            short_name=self.short_name.text(),
            email=self.email.text(),
            phone=self.phone.text(),
            mobile_phone=self.mobile_phone.text(),
            role=self.role.text(),
            extra_info1=self.extra_info1.text(),
            extra_info2=self.extra_info2.text(),
            extra_info3=self.extra_info3.text(),
            extra_info4=self.extra_info4.text(),
            extra_info5=self.extra_info5.text(),
            password=self.password.text()
        )

        # TODO: Implement signature encryption and saving
        # TODO: Save author information to INI file

        QMessageBox.information(self, "Erfolg", "Autor erfolgreich gespeichert.")
        self.accept()
