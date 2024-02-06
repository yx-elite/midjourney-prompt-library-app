from PyQt5.QtWidgets import (
    QDesktopWidget, QDialog, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QCheckBox, QHBoxLayout,
    QApplication, QFrame
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase, QDesktopServices
from PyQt5.QtCore import Qt, QSettings, QUrl

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('User Login')
        self.loadCustomFont()

        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry(desktop.primaryScreen())
        x = (screen_geometry.width() - 400) // 2
        y = (screen_geometry.height() - 500) // 2
        self.setGeometry(x, y, 400, 500)

        self.auth_frame = QFrame()
        self.auth_frame.setObjectName('authContainer')
        self.auth_layout = QVBoxLayout(self.auth_frame)

        self.login_label = QLabel('Sign In')
        self.login_label.setObjectName('titleLabel')

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Eg. EliteCreations')

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Minimum 8 characters')

        self.show_hide_button = QPushButton()
        self.show_hide_button.setObjectName('hideShowBtn')
        self.show_hide_button.setIcon(QIcon('img/show-64.png'))  # Replace with your actual show icon file
        self.show_hide_button.setFlat(True)
        self.show_hide_button.clicked.connect(self.toggle_password_visibility)
        
        self.password_input_frame = QFrame()
        self.password_input_frame.setObjectName('passwordInput')

        self.password_layout = QHBoxLayout(self.password_input_frame)
        self.password_layout.addWidget(self.password_input)
        self.password_layout.addWidget(self.show_hide_button)
        self.password_layout.setContentsMargins(0, 0, 0, 0)

        self.checkbox_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox('Remember Me')
        self.remember_checkbox.setObjectName('checkBox')
        self.load_saved_credentials()
        self.checkbox_layout.addWidget(self.remember_checkbox)
        self.checkbox_layout.addStretch()

        self.forgot_password_link = QLabel("<a href='https://example.com/forgot_password' style='font-size: 14px; color: white; text-decoration:none;'>Forgot Password?</a>")
        self.forgot_password_link.setContentsMargins(0, 0, 0, 10)
        self.forgot_password_link.setObjectName('externalLinkText')
        self.forgot_password_link.setOpenExternalLinks(True)
        self.checkbox_layout.addWidget(self.forgot_password_link)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        self.auth_layout.addStretch()
        self.auth_layout.addWidget(self.login_label)
        self.auth_layout.addWidget(self.username_label)
        self.auth_layout.addWidget(self.username_input)
        self.auth_layout.addWidget(self.password_label)
        self.auth_layout.addWidget(self.password_input_frame)
        self.auth_layout.addLayout(self.checkbox_layout)
        self.auth_layout.addWidget(self.login_button)
        self.auth_layout.addStretch()

        self.applyExternalStylesheet()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.auth_frame)

    def loadCustomFont(self):
        font_dir = "font/"
        font_files = [
            "Poppins-Regular.ttf",
            "Poppins-Bold.ttf",
            "Poppins-Italic.ttf",
        ]

        for font_file in font_files:
            font_path = font_dir + font_file
            QFontDatabase.addApplicationFont(font_path)

        app_font = QFont("Poppins", 9)
        QApplication.setFont(app_font)

    def load_saved_credentials(self):
        settings = QSettings('YourCompany', 'YourApp')
        remember_me = settings.value('RememberMe', type=bool)

        if remember_me:
            saved_username = settings.value('Username')
            saved_password = settings.value('Password')

            if saved_username:
                self.username_input.setText(saved_username)

            if saved_password:
                self.password_input.setText(saved_password)

            self.remember_checkbox.setChecked(True)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.remember_checkbox.isChecked():
            settings = QSettings('YourCompany', 'YourApp')
            settings.setValue('RememberMe', True)
            settings.setValue('Username', username)
            settings.setValue('Password', password)
        else:
            settings = QSettings('YourCompany', 'YourApp')
            settings.setValue('RememberMe', False)
            settings.remove('Username')
            settings.remove('Password')

        if username and password:
            self.accept()

    def applyExternalStylesheet(self):
        with open('auth_style.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_hide_button.setIcon(QIcon('img/hide-64.png'))  # Replace with your actual hide icon file
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_hide_button.setIcon(QIcon('img/show-64.png'))  # Replace with your actual show icon file

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
