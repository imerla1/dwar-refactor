import sys
import time
from utils import check_network, license_server_health, token_manager
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QFrame, QLabel,
                             QMessageBox, QProgressBar,
                             QVBoxLayout, QWidget)
from database import SessionLocal
from widgets.verify_license_key_window import LicenseKeyVerificationWidget


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.license_server_health_url = "http://localhost:8000/health"
        self.progressBar = None
        self.labelDescription = None
        self.labelTitle = None
        self.frame = None
        self.db = SessionLocal()
        self.setWindowTitle('DwarMaster')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText('Dwar Master')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Initialization</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

    def loading(self):
        # Update progress bar based on the counter
        self.progressBar.setValue(self.counter)

        # Perform actions based on the progress counter
        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Checking Network Connection</strong>')
            # Simulate API call 1
            if check_network.check_internet_connection():
                self.counter += 1
            else:
                # Display error message for API call 1
                self.show_error_message('Please check internet connection')
                self.timer.stop()
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Checking License Server status</strong>')
            # Simulate API call 2
            if license_server_health.get_license_server_health(self.license_server_health_url):
                self.counter += 1
            else:
                # Display error message for API call 2
                print("license server failed")
                self.show_error_message('License server Failed')
                self.timer.stop()
                self.close()
        elif self.counter == int(self.n * 0.9):
            self.labelDescription.setText('<strong>Checking Token State</strong>')
            jwt_token = token_manager.fetch_jwt_token(self.db)
            if jwt_token:
                print(jwt_token)

            else:
                self.timer.stop()
                self.close()
                self.new_window = LicenseKeyVerificationWidget()
                self.new_window.show()
            self.counter += 1
                

        elif self.counter >= self.n:
            # API calls are complete, stop the timer, close splash screen, and proceed
            self.timer.stop()
            self.close()

            print("Finished 100%")

        # Increment the counter for the loading progress
        self.counter += 1

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)
