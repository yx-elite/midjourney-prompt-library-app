from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(400, 300, 400, 200)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        
        # Apply dark theme stylesheet from external file
        self.applyExternalStylesheet()

    def handle_login(self):
        # Add your login logic here
        # For simplicity, let's just accept any non-empty username/password
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.accept()

    def applyExternalStylesheet(self):
        with open('auth_style.qss', 'r') as f:
            self.setStyleSheet(f.read())
