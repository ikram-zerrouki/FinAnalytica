from PyQt5.QtCore import QObject
from models.financial_model import FinancialModel
from ui.financial_analysis_view import FinancialAnalysisView


class TabController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialisation du modèle avant de connecter les signaux
        self.financial_model = FinancialModel()
        self.financial_view = FinancialAnalysisView()

        # Connecter les signaux
        self._connect_signals()

    def _connect_signals(self):
        """Connecte tous les signaux nécessaires"""
        # Connexion du modèle
        self.financial_model.calculation_complete.connect(self._handle_calculation_results)

        # Connexions de la vue
        self.financial_view.data_input.calculate_clicked.connect(self.calculate_ratios)
        self.financial_view.results_view.graph_type_changed.connect(self.handle_graph_type_changed)

    def calculate_ratios(self):
        """Calcule les ratios financiers à partir des données saisies"""
        try:
            # Get data from view
            data = self.financial_view.data_input.get_input_data()

            # Update model and calculate
            self.financial_model.update_data(data)
            self.financial_model.calculate_all_ratios()  # Le signal calculation_complete sera émis

        except ValueError as e:
            print(f"Erreur de saisie: {str(e)}")
        except Exception as e:
            print(f"Erreur lors du calcul des ratios: {str(e)}")

    def handle_graph_type_changed(self, graph_type):
        """Gère le changement de type de graphique"""
        self.financial_view.results_view.current_graph_type = graph_type
        self.financial_view.results_view.update_graph()

    def get_view(self):
        """Retourne la vue pour intégration dans l'interface principale"""
        return self.financial_view

    def _handle_calculation_results(self, ratios):
        """Reçoit et affiche les résultats du calcul"""
        try:
            # Get all graph data from the model
            graph_data = {
                'liquidity': self.financial_model.get_graph_data('liquidity'),
                'solvency': self.financial_model.get_graph_data('solvency'),
                'profitability': self.financial_model.get_graph_data('profitability'),
                'activity': self.financial_model.get_graph_data('activity')
            }

            # Update the results view with both ratios and graph data
            self.financial_view.results_view.display_results(ratios)
            self.financial_view.results_view.update_graph_data(graph_data)

            # Switch to results tab
            self.financial_view.show_results_tab()

        except Exception as e:
            print(f"Erreur d'affichage des résultats: {str(e)}")