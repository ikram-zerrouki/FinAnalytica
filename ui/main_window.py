from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QWidget,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal
from ui.sidebar import Sidebar
from ui.data_tab import DataTab
from ui.graphs_tab import GraphsTab
from ui.home_tab import HomeTab
from ui.results_tab import ResultsTab
from ui.welcome_page import WelcomePage
from ui.financial_analysis_view import FinancialAnalysisView


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.tabs = {}
        self._init_ui()
        self._init_tabs()
        self._connect_signals()

        # Connect the financial analysis view to the tab controller
        self.controller.tab_controller.financial_view = self.financial_analysis_view

    def _init_ui(self):
        self.stacked_widget = QStackedWidget()

        # 1. Welcome Page
        self.welcome_page = WelcomePage()
        self.stacked_widget.addWidget(self.welcome_page)

        # 2. HomeTab seul
        self.home_widget = QWidget()
        home_layout = QVBoxLayout(self.home_widget)
        home_layout.setContentsMargins(0, 0, 0, 0)
        self.home_tab = HomeTab(self.controller)
        home_layout.addWidget(self.home_tab)
        self.stacked_widget.addWidget(self.home_widget)

        # 3. Vue complète avec sidebar
        self.main_widget = QWidget()
        main_layout = QHBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: white;")
        self.content_area.setLayout(QVBoxLayout())
        main_layout.addWidget(self.content_area, 1)

        self.stacked_widget.addWidget(self.main_widget)

        # 4. Financial Analysis View (without sidebar)
        self.form_widget = QWidget()
        form_layout = QVBoxLayout(self.form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        self.financial_analysis_view = FinancialAnalysisView(self.controller)  # Pass controller here
        form_layout.addWidget(self.financial_analysis_view)
        self.stacked_widget.addWidget(self.form_widget)

        self.setCentralWidget(self.stacked_widget)
        self.show_welcome_page()

    def _init_tabs(self):
        self.tabs = {
            "Accueil": HomeTab(self.controller),
            "Données": DataTab(self.controller),
            "Résultats": ResultsTab(self.controller),
            "Graphiques": GraphsTab(self.controller)
        }

    def _connect_signals(self):
        self.welcome_page.home_requested.connect(self.show_home_tab)
        self.home_tab.return_requested.connect(self.show_welcome_page)
        self.home_tab.import_successful.connect(self.show_main_app)
        self.home_tab.manual_entry_requested.connect(self.show_form_view)
        self.sidebar.return_requested.connect(self.show_home_tab)
        self.sidebar.nav_requested.connect(self._handle_navigation)

        # Connect financial analysis view signals
        if hasattr(self.financial_analysis_view, 'return_requested'):
            self.financial_analysis_view.return_requested.connect(self.show_home_tab)

        # Connect the calculate signal from data input to tab controller
        if hasattr(self.financial_analysis_view.data_input, 'calculate_clicked'):
            self.financial_analysis_view.data_input.calculate_clicked.connect(
                self.controller.tab_controller.calculate_ratios
            )
    def show_welcome_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_home_tab(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_main_app(self):
        self.stacked_widget.setCurrentIndex(2)
        self._show_page("Données")

    def show_form_view(self):
        """Shows the financial analysis view instead of data input form"""
        self.stacked_widget.setCurrentIndex(3)

    def _handle_navigation(self, page_name):
        self._show_page(page_name)

    def _show_page(self, page_name):
        if page_name not in self.tabs:
            return

        layout = self.content_area.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        layout.addWidget(self.tabs[page_name])

        if page_name == "Données":
            self.tabs["Données"].update_data()
        elif page_name == "Résultats":
            self.tabs["Résultats"].update_results()
        elif page_name == "Graphiques":
            self.tabs["Graphiques"].update_graphs()