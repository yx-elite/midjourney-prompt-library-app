"""
# Main Code Version: 1.2
# Auth Code Version: 1.1

- Comment reorganised
- Deploy bug fixed
- Resource_path function added, \\ for image path
- Stylesheet deployment reference fixed

"""

import os
import sys
import pyrebase
from PyQt5.QtWidgets import (
    QDesktopWidget, QDialog, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QCheckBox, QHBoxLayout,
    QApplication, QFrame, QWidget
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase, QRegion
from PyQt5.QtCore import Qt, QSettings, QSize, QRect
from config import firebaseConfig


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Set window dimensions and corner radius
window_width = 1150
window_height = 700
window_radius = 15

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(window_width, window_height)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Set rounded corners for the window
        self.setMask(self.getMask())

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('User Login')
        # Load custom font
        self.loadCustomFont()
        # Position the window in the center of the screen
        self.centerWindow()

        # Main layout for the login window
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side: Image
        self.img = QLabel(self)
        self.img.setObjectName('coverImage')
        self.loadImage()
        
        # Right side: Authentication Frame
        self.auth_frame = QFrame()
        self.auth_frame.setObjectName('authContainer')
        self.auth_frame.setFixedSize(350, 600)
        self.auth_layout = QVBoxLayout(self.auth_frame)
        self.setupAuthLayout()

        # Add widgets to the main layout
        main_layout.addWidget(self.img)
        main_layout.addStretch()
        main_layout.addWidget(self.auth_frame)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Setup close button
        self.setupOverlappingIcons()
        # Apply external stylesheet
        self.applyExternalStylesheet()

    def loadImage(self):
        pixmap = QPixmap(resource_path('img\\luffy-cover.png'))
        pixmap = pixmap.scaled(600, 700)
        self.img.setPixmap(pixmap)

    def setupAuthLayout(self):
        # Add authentication widgets to the layout
        self.addAuthWidgets()

    def getMask(self):
        # Create rounded mask for the window
        radius = window_radius
        base = self.rect()
        ellipse = QRect(0, 0, 2 * radius , 2 * radius)

        base_region = QRegion(base.adjusted(radius, 0, -radius, 0))
        base_region |= QRegion(base.adjusted(0, radius, 0, -radius))
        
        base_region |= QRegion(ellipse, QRegion.Ellipse)
        ellipse.moveTopRight(base.topRight())
        base_region |= QRegion(ellipse, QRegion.Ellipse)
        ellipse.moveBottomRight(base.bottomRight())
        base_region |= QRegion(ellipse, QRegion.Ellipse)
        ellipse.moveBottomLeft(base.bottomLeft())
        base_region |= QRegion(ellipse, QRegion.Ellipse)

        return base_region

    def centerWindow(self):
        # Center the window on the screen
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry(desktop.primaryScreen())
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

    def loadCustomFont(self):
        # Load custom font for the application
        font_dir = "font\\"
        font_files = [
            "Poppins-Regular.ttf",
            "Poppins-Bold.ttf",
            "Poppins-Italic.ttf",
        ]

        for font_file in font_files:
            font_path = font_dir + font_file
            QFontDatabase.addApplicationFont(resource_path(font_path))

        app_font = QFont("Poppins", 9)
        QApplication.setFont(app_font)
    
    def setupOverlappingIcons(self):
        # Setup close button on the window
        action_frame = QWidget(self)
        action_frame.setObjectName("action_frame")

        close_button = QPushButton(action_frame)
        close_button.setObjectName("closeButton")
        close_button.setIcon(QIcon(resource_path('img\\close-64.png')))
        close_button.setIconSize(QSize(20, 20))
        close_button.clicked.connect(self.reject)

        # Create a layout for the action_frame
        action_layout = QHBoxLayout(action_frame)
        action_layout.addWidget(close_button)

        # Set the layout for the action_frame
        action_frame.setLayout(action_layout)
        action_frame.setGeometry(1080, 10, 60, 60)

    def applyExternalStylesheet(self):
        # Apply external stylesheet for styling
        dirname = os.path.dirname(__file__)
        stylesheet_path = os.path.join(dirname, 'auth_style.qss')
        with open(stylesheet_path, 'r') as f:
            self.setStyleSheet(f.read())

    def addAuthWidgets(self):
        # Add authentication widgets to the layout
        self.login_label = QLabel('Welcome Back')
        self.login_label.setObjectName('titleLabel')

        self.email_label = QLabel('Email Address:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Eg. elitecreations@gmail.com')

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Minimum 8 characters')

        self.show_hide_button = QPushButton()
        self.show_hide_button.setObjectName('hideShowBtn')
        self.show_hide_button.setIcon(QIcon(resource_path('img\\show-64.png')))
        self.show_hide_button.setFlat(True)
        self.show_hide_button.clicked.connect(self.toggle_password_visibility)
        
        self.password_input_frame = QFrame()
        self.password_input_frame.setObjectName('passwordInput')

        self.password_layout = QHBoxLayout(self.password_input_frame)
        self.password_layout.addWidget(self.password_input)
        self.password_layout.addWidget(self.show_hide_button)
        self.password_layout.setContentsMargins(0, 0, 0, 0)
        
        self.error_label = QLabel('')
        self.error_label.setObjectName('errorMessage')
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)  # Enable word wrapping

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setContentsMargins(0, 0, 0, 5)
        self.remember_checkbox = QCheckBox('Remember Me')
        self.remember_checkbox.setObjectName('checkBox')
        self.load_saved_credentials()
        self.checkbox_layout.addWidget(self.remember_checkbox)
        self.checkbox_layout.addStretch()
        
        self.forgot_password_button = QPushButton("Forgot Password?", self)
        self.forgot_password_button.setObjectName('forgotPassword')
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.forgot_password)
        self.checkbox_layout.addWidget(self.forgot_password_button)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        self.auth_layout.addStretch()
        self.auth_layout.addWidget(self.login_label)
        self.auth_layout.setAlignment(self.login_label, Qt.AlignCenter)
        self.auth_layout.addWidget(self.email_label)
        self.auth_layout.addWidget(self.email_input)
        self.auth_layout.addWidget(self.password_label)
        self.auth_layout.addWidget(self.password_input_frame)
        self.auth_layout.addWidget(self.error_label)
        self.auth_layout.addLayout(self.checkbox_layout)
        self.auth_layout.addWidget(self.login_button)
        self.auth_layout.addStretch()

    def load_saved_credentials(self):
        # Load saved credentials if "Remember Me" is checked
        settings = QSettings('Elite Creations', 'MJ Prompt Library')
        remember_me = settings.value('RememberMe', type=bool)

        if remember_me:
            saved_email = settings.value('Email')
            saved_password = settings.value('Password')

            if saved_email:
                self.email_input.setText(saved_email)

            if saved_password:
                self.password_input.setText(saved_password)

            self.remember_checkbox.setChecked(True)

    def handle_login(self):
        # Handle login process
        email = self.email_input.text()
        password = self.password_input.text()

        try:
            auth.sign_in_with_email_and_password(email, password)
            print('Authentication successful')

            if self.remember_checkbox.isChecked():
                settings = QSettings('Elite Creations', 'MJ Prompt Library')
                settings.setValue('RememberMe', True)
                settings.setValue('Email', email)
                settings.setValue('Password', password)
            else:
                settings = QSettings('Elite Creations', 'MJ Prompt Library')
                settings.setValue('RememberMe', False)
                settings.remove('Email')
                settings.remove('Password')

            self.accept()

        except Exception as e:
            print('Authentication failed')
            # Clear the email and password inputs
            self.email_input.clear()
            self.password_input.clear()
            self.email_input.setStyleSheet("")
            self.error_label.setText("Incorrect email or password. Please try again.")
            
            settings = QSettings('Elite Creations', 'MJ Prompt Library')
            settings.setValue('RememberMe', False)
            settings.remove('Email')
            settings.remove('Password')

    def forgot_password(self):
        # Handle forgot password functionality
        email = self.email_input.text().strip()  # Remove leading and trailing whitespaces
        if not email:
            # If no email input, show red border and set error label text
            self.email_input.setStyleSheet("border: 2px solid red;")
            self.error_label.setText('Enter your email and click on "Forgot Password?" again to reset your password.')
            return

        try:
            # Reset the styles and error label text
            self.email_input.setStyleSheet("")
            self.error_label.setText(f"Password reset instructions successfully sent to {email}.")
            self.error_label.setStyleSheet("color: #4AFF00;")

            # Send password reset email
            auth.send_password_reset_email(email)
            print('Password reset email sent.')
        except Exception as e:
            # Handle the exception and set the error label text accordingly
            self.email_input.setStyleSheet("border: 2px solid red;")
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText("Invalid email detected. Please try again.")
            self.email_input.clear()
            print(f'Error sending password reset email: {e}')

    def toggle_password_visibility(self):
        # Toggle visibility of password
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_hide_button.setIcon(QIcon(resource_path('img\\hide-64.png')))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_hide_button.setIcon(QIcon(resource_path('img\\show-64.png')))
