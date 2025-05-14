import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ui.main_window import MainWindow
from ui.welcome_page import WelcomePage
from ui.help_page import HelpPage
from controllers.main_controller import MainController


class AppManager(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.controller = MainController()
        self._init_ui()
        self.setup_connections()

    def _init_ui(self):
        # Welcome Page
        self.welcome_page = WelcomePage()
        self.addWidget(self.welcome_page)

        # Help Page
        self.help_page = HelpPage()
        self.addWidget(self.help_page)

        # Main App
        self.main_window = MainWindow(self.controller)
        self.addWidget(self.main_window)

        self.setCurrentIndex(0)
        self.setWindowTitle("Analyse Comptable")
        self.setGeometry(100, 100, 1000, 700)

    def setup_connections(self):
        # Connectez tous les signaux ici pour une meilleure visibilité
        self.welcome_page.home_requested.connect(self.show_main_app)
        self.welcome_page.help_requested.connect(self.show_help_page)
        self.help_page.back_requested.connect(self.show_welcome_page)
        self.controller.return_to_welcome_requested.connect(self.show_welcome_page)

        # Connectez le signal de retour du HomeTab
        self.main_window.home_tab.return_requested.connect(self.show_welcome_page)

    def show_main_app(self):
        self.setCurrentIndex(2)  # Index 2 = MainWindow

    def show_help_page(self):
        self.setCurrentIndex(1)  # Index 1 = HelpPage

    def show_welcome_page(self):
        self.setCurrentIndex(0)  # Index 0 = WelcomePage


def main():
    app = QApplication(sys.argv)

    # Apply stylesheet if needed
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = AppManager()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()