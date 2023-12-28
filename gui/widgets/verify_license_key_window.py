import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LicenseKeyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('License Key Entry')
        self.setGeometry(300, 300, 400, 150)

        # Create widgets
        label = QLabel('Please enter license key:')
        self.license_input = QLineEdit(self)
        submit_button = QPushButton('Submit', self)

        # Connect the button click event to a custom function
        submit_button.clicked.connect(self.on_submit)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.license_input)
        layout.addWidget(submit_button)

        # Apply some basic stylings
        self.setStyleSheet(
            "QWidget { background-color: #f0f0f0; }"
            "QLabel { font-size: 14px; margin-bottom: 10px; }"
            "QLineEdit { padding: 5px; font-size: 14px; }"
            "QPushButton { padding: 8px; font-size: 14px; background-color: #4CAF50; color: white; border: none; }"
            "QPushButton:hover { background-color: #45a049; }"
        )

    def on_submit(self):
        # Retrieve the entered license key
        license_key = self.license_input.text()
        
        # Perform some action with the license key (replace this with your logic)
        print(f"License Key Entered: {license_key}")

        # Open another window (replace SecondWindow with your second window class)
        second_window = SecondWindow()
        second_window.show()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Second Window')
        self.setGeometry(400, 400, 400, 150)

        # Create widgets for the second window
        label = QLabel('This is the Second Window!')

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addWidget(label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LicenseKeyWindow()
    window.show()
    sys.exit(app.exec_())