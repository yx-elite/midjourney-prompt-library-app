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
from PyQt5.QtWidgets import (
    QDesktopWidget, QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QFrame, QDialog, QSpacerItem, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QUrl, QSize, QPoint
from auth import LoginWindow
from config import webpageURL


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    """Main application window for Elite Creations Studio - MidJourney Prompt Library"""

    def __init__(self):
        super().__init__()
        self.initUI()
        self.showMaximized()

    def initUI(self):
        """Initialize the user interface"""

        self.setWindowIcon(QIcon(resource_path('app-icon.png')))
        self.setWindowTitle('Elite Creations Studio - MidJourney Prompt Library')
        self.loadCustomFont()
        
        # Main widget and layout
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("mainContainer")
        self.central_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Top container with navigation and search options
        self.setupTopContainer()

        # Web view container with rounded corners
        self.setupWebView()

        # Connections
        self.search_button.clicked.connect(self.search_webpage)
        self.search_bar.returnPressed.connect(self.search_webpage)

        # Apply dark theme stylesheet from external file
        self.applyExternalStylesheet()

        # Overlapping icons on the QWebEngineView
        self.setupOverlappingIcons()

    def loadCustomFont(self):
        """Load custom fonts for the application"""

        font_dir = "font/"
        font_files = [
            "Poppins-Regular.ttf",
            "Poppins-Bold.ttf",
            "Poppins-Italic.ttf",
            "Poppins-MediumItalic.ttf",
            "Poppins-SemiboldItalic.ttf",
        ]

        for font_file in font_files:
            font_path = font_dir + font_file
            QFontDatabase.addApplicationFont(font_path)
        
        # Set the Poppins font for the entire application
        app_font = QFont("Poppins", 9)  # You can adjust the size
        QApplication.setFont(app_font)

    def setupTopContainer(self):
        """Set up the top container containing navigation and search options"""

        self.home_button = QPushButton("Elite Creations")
        self.home_button.setObjectName("homeButton")
        self.home_button.setCursor(Qt.PointingHandCursor)
        self.home_button.clicked.connect(self.toggle_home_button)
        
        self.title_des = QLabel("MJ Prompt Library")
        self.title_des.setObjectName("titleDescription")

        # Search bar and button layout
        self.setupSearchBar()
        
        self.spacer_item1 = QSpacerItem(170, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.logout_button = QPushButton("  Logout")
        self.logout_button.setObjectName("iconTextBtn")
        self.logout_button.setIcon(QIcon(resource_path('img\\logout-64.png')))
        self.logout_button.setIconSize(QSize(27, 27))
        self.logout_button.clicked.connect(self.toggle_logout_button)
        
        self.top_container = QFrame()
        self.top_container.setObjectName("topContainer")
        self.top_layout = QHBoxLayout(self.top_container)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.home_button)
        self.top_layout.addWidget(self.title_des)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.search_container)
        self.top_layout.addStretch()
        self.top_layout.addItem(self.spacer_item1)
        self.top_layout.addWidget(self.logout_button)
        self.top_container.setLayout(self.top_layout)
        
        self.central_layout.addWidget(self.top_container)

    def setupSearchBar(self):
        """Set up the search bar and associated buttons"""

        self.search_container = QFrame()
        self.search_container.setObjectName("searchContainer")
        self.search_container.setMinimumWidth(800)
        self.search_container.setMaximumWidth(900)

        self.search_layout = QHBoxLayout(self.search_container)
        
        self.search_icon_bar_frame = QFrame()
        self.search_icon_bar_frame.setObjectName("searchBar")
        self.search_icon_bar_layout = QHBoxLayout(self.search_icon_bar_frame)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search anything here...")

        # Search button with an icon
        self.search_icon = QPushButton()
        self.search_icon.setObjectName("iconBtn")
        self.search_icon.setIcon(QIcon(resource_path('img\\search-12-64.png')))
        self.search_icon.clicked.connect(self.search_webpage)

        # Clear button (cross button)
        self.clear_button = QPushButton()
        self.clear_button.setObjectName("iconBtn")
        self.clear_button.setIcon(QIcon(resource_path('img\\cancel-64.png')))
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setVisible(False)     # Initially hide the clear button

        # Search text button without an icon
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_webpage)

        # Add the search bar, icon, and buttons to the layout
        self.search_icon_bar_layout.addWidget(self.search_icon)
        self.search_icon_bar_layout.addWidget(self.search_bar)
        self.search_icon_bar_layout.addWidget(self.clear_button)
        self.search_icon_bar_layout.setContentsMargins(10, 0, 10, 0)
        self.search_layout.addWidget(self.search_icon_bar_frame)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.setContentsMargins(0, 0, 0, 0)

        # Connect the textChanged signal to show/hide the clear button
        self.search_bar.textChanged.connect(self.toggle_clear_button)

    def setupWebView(self):
        """Set up the web view container"""

        self.webContainer = QFrame(self)
        self.webContainer.setObjectName("webContainer")
        self.webLayout = QVBoxLayout(self.webContainer)
        self.webContainer.setLayout(self.webLayout)
        self.central_layout.addWidget(self.webContainer, 1)
        # Web view
        self.web = QWebEngineView()
        self.webLayout.addWidget(self.web)
        self.web.load(QUrl(webpageURL))

    def setupOverlappingIcons(self):
        """Set up overlapping icons on the web view"""

        # Web Container Geometry
        web_container_pos = self.mapToGlobal(QPoint(0, 0))

        # Create a frame to contain the buttons
        action_frame = QWidget(self)
        action_frame.setObjectName("actionFrame")
        button_layout = QHBoxLayout(action_frame)

        # Undo Button
        undo_icon = QPushButton(action_frame)
        undo_icon.setObjectName("iconBtn")
        undo_icon.setIcon(QIcon(resource_path('img\\undo-64.png')))
        undo_icon.setIconSize(QSize(20, 20))
        undo_icon.clicked.connect(lambda: self.web.back())
        button_layout.addWidget(undo_icon)

        # Redo Button
        redo_icon = QPushButton(action_frame)
        redo_icon.setObjectName("iconBtn")
        redo_icon.setIcon(QIcon(resource_path('img\\redo-64.png')))
        redo_icon.setIconSize(QSize(20, 20))
        redo_icon.clicked.connect(lambda: self.web.forward())
        button_layout.addWidget(redo_icon)

        # Reload Button
        reload_icon = QPushButton(action_frame)
        reload_icon.setObjectName("iconBtn")
        reload_icon.setIcon(QIcon(resource_path('img\\reload-64.png')))
        reload_icon.setIconSize(QSize(20, 20))
        reload_icon.clicked.connect(lambda: self.web.reload())
        button_layout.addWidget(reload_icon)

        # Set the geometry of the button frame
        action_frame.setGeometry(50, 120, 150, 45)

    def search_webpage(self):
        """Search the webpage for the entered text"""

        text = self.search_bar.text()
        self.web.findText(text)
    
    def toggle_home_button(self):
        """Load the homepage"""

        self.web.load(QUrl(webpageURL))

    def toggle_clear_button(self, text):
        """Toggle visibility of the clear button based on text input"""

        self.clear_button.setVisible(bool(text))
    
    def toggle_logout_button(self):
        """Toggle to the login window upon logout"""

        self.close()  # Close the MainWindow
        auth_page = LoginWindow()
        if auth_page.exec_() == QDialog.Accepted:
            self.show()

    def clear_search(self):
        """Clear the search bar and hide the clear button"""

        self.search_bar.clear()
        self.clear_button.setVisible(False)

    def applyExternalStylesheet(self):
        """Apply external stylesheet for dark theme"""

        dirname = os.path.dirname(__file__)
        stylesheet_path = os.path.join(dirname, 'main_style.qss')
        with open(stylesheet_path, 'r') as f:
            self.setStyleSheet(f.read())

def main():
    """Main function to start the application"""

    app = QApplication(sys.argv)
    auth_page = LoginWindow()
    if auth_page.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
