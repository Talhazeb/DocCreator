from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from desktop_app.ui.document_dialog import DocumentDialog
from desktop_app.ui.author_dialog import AuthorDialog
from desktop_app.utils.template_manager import TemplateManager

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.template_manager = TemplateManager(config)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('DocCreator')
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.btn_document = QPushButton('Dokument')
        self.btn_author = QPushButton('Autor')
        self.btn_edit_previous = QPushButton('Vorheriges Dokument weiter bearbeiten')
        self.btn_delete_previous = QPushButton('Daten vorheriges Dokument löschen')

        #  Button zum Beenden des Programms
        self.exit_btn = QPushButton("Beenden")
        self.exit_btn.clicked.connect(self.close)
        
        layout.addWidget(self.btn_document)
        layout.addWidget(self.btn_author)
        layout.addWidget(self.btn_edit_previous)
        layout.addWidget(self.btn_delete_previous)
        layout.addWidget(self.exit_btn)

        central_widget.setLayout(layout)

        self.btn_document.clicked.connect(self.open_document_dialog)
        self.btn_author.clicked.connect(self.open_author_dialog)
        self.btn_edit_previous.clicked.connect(self.edit_previous_document)
        self.btn_delete_previous.clicked.connect(self.delete_previous_document)

    def open_document_dialog(self):
        dialog = DocumentDialog(self.config, self.template_manager)
        dialog.exec_()

    def open_author_dialog(self):
        dialog = AuthorDialog(self.config)
        dialog.exec_()

    def edit_previous_document(self):
        # To be implemented
        pass

    def delete_previous_document(self):
        # To be implemented
        pass
