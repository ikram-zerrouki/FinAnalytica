

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from models.analysis_model import AnalysisModel
from models.financial_model import FinancialModel
from controllers.file_controller import FileController
from controllers.export_controller import ExportController
from controllers.tab_controller import TabController


class MainController(QObject):
    operation_completed = pyqtSignal(bool, str)
    financial_analysis_completed = pyqtSignal(dict)
    return_to_welcome_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Modèles
        self.model = AnalysisModel()
        self.financial_model = FinancialModel()


        # Contrôleurs
        self.file_controller = FileController(self)
        self.export_controller = ExportController(self)
        self.tab_controller = TabController(self)

        # Connexions des signaux
        self._connect_signals()

    def _connect_signals(self):
        """Connecte tous les signaux entre contrôleurs et modèles"""
        self.model.data_updated.connect(
            lambda: self.operation_completed.emit(True, "Données mises à jour")
        )

        self.financial_model.calculation_complete.connect(
            self._handle_financial_results
        )

    def _handle_financial_results(self, results):
        """Traite les résultats financiers et émet le signal"""
        self.financial_analysis_completed.emit(results)
        self.model.update_financial_data(results)

    # Méthodes d'accès aux données
    def get_raw_data(self):
        return self.model.raw_data

    def get_processed_data(self):
        return self.model.processed_data

    def get_trends(self):
        return self.model.trends

    def get_financial_results(self):
        """Retourne les derniers résultats financiers calculés"""
        return getattr(self.financial_model, 'ratios', None)

    def calculate_financial_ratios(self, input_data):
        """Lance le calcul des ratios financiers"""
        try:
            self.financial_model.update_data(input_data)
            return self.financial_model.calculate_all_ratios()
        except Exception as e:
            self.operation_completed.emit(False, f"Erreur calcul ratios: {str(e)}")
            return None

    def export_report(self, parent_window=None):
        """Point d'entrée pour l'export du rapport"""
        success, message = self.export_controller.export_to_pdf(
            parent_window=parent_window
        )
        self.operation_completed.emit(success, message)