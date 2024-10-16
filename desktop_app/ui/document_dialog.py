from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QMessageBox
from desktop_app.utils.pdf_creator import create_pdf
from desktop_app.models.author import Author

class DocumentDialog(QDialog):
    def __init__(self, config, template_manager):
        super().__init__()
        self.config = config
        self.template_manager = template_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dokument erstellen")
        
        # Erstellen Sie ein Hauptlayout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Erstellen Sie ein Formlayout für die Eingabefelder
        self.form_layout = QFormLayout()
        main_layout.addLayout(self.form_layout)

        # Fügen Sie Buttons hinzu
        create_btn = QPushButton("Erstellen")
        create_btn.clicked.connect(self.create_document)
        main_layout.addWidget(create_btn)

        # Aktualisieren Sie das Formular
        self.update_form()

    def get_author_names(self):
        # This should be implemented to get the list of author short names
        # For now, we'll return a dummy list
        return ["Author1", "Author2"]

    def update_form(self):
        # Löschen Sie zuerst alle vorhandenen Widgets im Formlayout
        for i in reversed(range(self.form_layout.rowCount())):
            self.form_layout.removeRow(i)

        # Fügen Sie neue Eingabefelder hinzu
        # (Hier sollten Sie Ihre Logik zum Hinzufügen von Feldern implementieren)
        self.form_layout.addRow("Feldname:", QLineEdit())

    def create_document(self):
        # Implementieren Sie hier die Logik zum Erstellen des Dokuments
        pass

    def create_pdf(self):
        # Collect form data
        form_data = {}
        for i in range(4, self.layout().rowCount() - 1):  # Skip template, author, password, and create button
            question = self.layout().itemAt(i, QFormLayout.LabelRole).widget().text()
            answer = self.layout().itemAt(i, QFormLayout.FieldRole).widget().text()
            form_data[question] = answer

        selected_template = self.template_combo.currentText()
        selected_author = self.author_combo.currentText()
        password = self.password.text()

        author = Author.load(selected_author, self.config)
        if author and author.decrypt_signature(self.config):
            pdf_path = create_pdf(self.config, selected_template, form_data, author)
            QMessageBox.information(self, "Erfolg", f"PDF wurde erstellt und gespeichert unter: {pdf_path}")
            self.accept()
        else:
            QMessageBox.warning(self, "Fehler", "Autor nicht gefunden oder Passwort falsch.")
