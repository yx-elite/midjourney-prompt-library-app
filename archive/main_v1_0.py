import sys
from PyQt5.QtWidgets import (
    QDesktopWidget, QMainWindow, QApplication, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QHBoxLayout, QFrame, QDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import QUrl, QSize, QPoint
from archive.auth_v1_0 import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('Elite Creations Studio - MidJourney Prompt Library')
        self.loadCustomFont()

        # Calculate the center position of the screen
        # desktop = QDesktopWidget()
        # screen_geometry = desktop.screenGeometry(desktop.primaryScreen())
        # x = (screen_geometry.width() - 1500) // 2
        # y = (screen_geometry.height() - 900) // 2
        # self.setGeometry(x, y, 1500, 900)

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("mainContainer")
        self.central_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Search bar and button layout
        self.setupSearchBar()

        # Web view container with rounded corners
        self.setupWebView()

        # Connections
        self.search_button.clicked.connect(self.search_webpage)
        self.search_button.clicked.connect(self.search_webpage)
        self.search_bar.returnPressed.connect(self.search_webpage)

        # Apply dark theme stylesheet from external file
        self.applyExternalStylesheet()

        # Overlapping icons on the QWebEngineView
        self.setupOverlappingIcons()

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
        
        # Set the Poppins font for the entire application
        app_font = QFont("Poppins", 9)  # You can adjust the size
        QApplication.setFont(app_font)

    def setupSearchBar(self):
        # Search bar and button layout
        self.search_container = QFrame()
        self.search_container.setObjectName("searchContainer")

        self.search_layout = QHBoxLayout(self.search_container)
        
        self.search_icon_bar_frame = QFrame()
        self.search_icon_bar_frame.setObjectName("searchBar")
        self.search_icon_bar_layout = QHBoxLayout(self.search_icon_bar_frame)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search anything here...")

        # Search button with an icon
        self.search_icon = QPushButton()
        self.search_icon.setObjectName("iconBtn")
        self.search_icon.setIcon(QIcon('img/search-12-64.png'))
        self.search_icon.clicked.connect(self.search_webpage)

        # Clear button (cross button)
        self.clear_button = QPushButton()
        self.clear_button.setObjectName("iconBtn")
        self.clear_button.setIcon(QIcon('img/cancel-64.png'))
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
        self.central_layout.addWidget(self.search_container, 0)

        # Connect the textChanged signal to show/hide the clear button
        self.search_bar.textChanged.connect(self.toggle_clear_button)

    def setupWebView(self):
        # Web view container with rounded corners
        self.webContainer = QFrame(self)
        self.webContainer.setObjectName("webContainer")
        self.webLayout = QVBoxLayout(self.webContainer)
        self.webContainer.setLayout(self.webLayout)
        self.central_layout.addWidget(self.webContainer, 1)
        # Web view
        self.web = QWebEngineView()
        self.webLayout.addWidget(self.web)
        self.web.load(QUrl("https://test1001.super.site/"))

    def setupOverlappingIcons(self):
        # Web Container Geometry
        web_container_pos = self.mapToGlobal(QPoint(0, 0))

        # Create a frame to contain the buttons
        action_frame = QWidget(self)
        action_frame.setObjectName("actionFrame")
        button_layout = QHBoxLayout(action_frame)

        # Undo Button
        undo_icon = QPushButton(action_frame)
        undo_icon.setObjectName("iconBtn")
        undo_icon.setIcon(QIcon('img/undo-64.png'))
        undo_icon.setIconSize(QSize(20, 20))
        undo_icon.clicked.connect(lambda: self.web.back())
        button_layout.addWidget(undo_icon)

        # Redo Button
        redo_icon = QPushButton(action_frame)
        redo_icon.setObjectName("iconBtn")
        redo_icon.setIcon(QIcon('img/redo-64.png'))
        redo_icon.setIconSize(QSize(20, 20))
        redo_icon.clicked.connect(lambda: self.web.forward())
        button_layout.addWidget(redo_icon)

        # Reload Button
        reload_icon = QPushButton(action_frame)
        reload_icon.setObjectName("iconBtn")
        reload_icon.setIcon(QIcon('img/reload-64.png'))
        reload_icon.setIconSize(QSize(20, 20))
        reload_icon.clicked.connect(lambda: self.web.reload())
        button_layout.addWidget(reload_icon)

        # Set the geometry of the button frame
        action_frame.setGeometry(50, 120, 150, 45)

    def search_webpage(self):
        text = self.search_bar.text()
        self.web.findText(text)

    def toggle_clear_button(self, text):
        self.clear_button.setVisible(bool(text))

    def clear_search(self):
        self.search_bar.clear()
        self.clear_button.setVisible(False)

    def applyExternalStylesheet(self):
        with open('main_style.qss', 'r') as f:
            self.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    auth_page = LoginWindow()
    if auth_page.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
