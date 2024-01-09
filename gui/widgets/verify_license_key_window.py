from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from utils import verify_license_key as server_verify_license_key
from models.token_model import TokenModel
from database import SessionLocal
from globals import secure_crypto



class LicenseKeyVerificationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.license_key_input = None
        self.init_ui()
        self.license_server_url = "http://127.0.0.1:8000/verify/key"

    def init_ui(self):
        # Set up the main layout
        layout = QVBoxLayout()

        # Label
        label = QLabel('Please Enter License Key:')
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)

        # Input field for license key
        self.license_key_input = QLineEdit(self)
        self.license_key_input.setFont(QFont('Arial', 12))
        layout.addWidget(self.license_key_input)

        # Verification Button
        verify_button = QPushButton('Verify', self)
        verify_button.clicked.connect(self.verify_license_key)
        verify_button.setFont(QFont('Arial', 12))
        verify_button.setStyleSheet('background-color: #4CAF50; color: white;')
        layout.addWidget(verify_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('License Key Verification (Unverified)')
        self.setGeometry(300, 300, 400, 200)

    def verify_license_key(self):
        db = SessionLocal()
        license_key_input = self.license_key_input.text()
        try:
            server_response_token = server_verify_license_key.verify_license_key(self.license_server_url,
                                                                                 license_key_input)
            token_in_db = db.query(TokenModel).filter_by().first()
            if token_in_db:
                db.delete(token_in_db)
                db.commit()


            encrypted_token = secure_crypto.encrypt(server_response_token)
            token = TokenModel(token=encrypted_token)
            db.add(token)
            db.commit()
        except Exception as e:
            self.show_error_message(str(e))


    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)
