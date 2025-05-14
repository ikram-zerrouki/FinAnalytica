
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
from datetime import datetime
from utils.constants import CATEGORY_NAMES


class ExportController(QObject):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller

    def export_to_pdf(self, output_path=None, parent_window=None):
        """Gère l'exportation complète en PDF avec sélection de fichier"""
        try:
            if not output_path:
                output_path, _ = QFileDialog.getSaveFileName(
                    parent_window,
                    "Exporter le rapport",

                    "C:/Users/DELL/PycharmProjects/AnalyseComptableApp2/exports/rapports",
                    "Fichiers PDF (*.pdf)"
                )
                if not output_path:
                    return False, "Export annulé"

            pdf = FPDF()
            pdf.set_auto_page_break(True, 15)

            # Ajout des différentes sections
            self._add_title(pdf)
            self._add_data_section(pdf)
            self._add_results_section(pdf)
            self._add_financial_analysis_section(pdf)
            self._add_graphs_section(pdf)

            pdf.output(output_path)
            return True, "Export PDF réussi"
        except Exception as e:
            return False, f"Erreur d'export: {str(e)}"

    def _add_title(self, pdf):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Rapport d\'Analyse Comptable', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Généré le {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        pdf.ln(20)

    def _add_data_section(self, pdf):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Données Extraites', 0, 1)
        pdf.set_font('Arial', '', 10)

        raw_data = self.main_controller.get_raw_data()
        if not raw_data:
            pdf.cell(0, 10, 'Aucune donnée disponible', 0, 1)
            return

        for year, data in raw_data.items():
            pdf.cell(0, 10, f'Année {year}', 0, 1)
            for key, value in data.items():
                pdf.cell(50, 6, key.replace('_', ' ').title(), 0, 0)
                pdf.cell(0, 6, f'{value:,.2f}', 0, 1)
            pdf.ln(5)

    def _add_results_section(self, pdf):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Résultats Calculés', 0, 1)
        pdf.set_font('Arial', '', 10)

        processed_data = self.main_controller.get_processed_data()
        if processed_data is None or processed_data.empty:
            pdf.cell(0, 10, 'Aucun résultat disponible', 0, 1)
            return

        for col in processed_data.columns:
            pdf.cell(60, 6, col.replace('_', ' ').title(), 0, 0)
            pdf.cell(0, 6, f'{processed_data[col].iloc[-1]:,.2f}', 0, 1)

    def _add_financial_analysis_section(self, pdf):
        """Nouvelle méthode pour ajouter l'analyse financière"""
        if not hasattr(self.main_controller, 'get_financial_results'):
            return

        financial_results = self.main_controller.get_financial_results()
        if not financial_results:
            return

        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Analyse Financière', 0, 1)
        pdf.set_font('Arial', '', 10)

        for category, ratios in financial_results.items():
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 8, CATEGORY_NAMES.get(category, category), 0, 1)
            pdf.set_font('Arial', '', 10)

            for ratio_name, ratio_data in ratios.items():
                pdf.cell(70, 6, ratio_data['description'], 0, 0)
                pdf.cell(0, 6, f"{ratio_data['value']:.2%}", 0, 1)
            pdf.ln(3)

    def _add_graphs_section(self, pdf):
        temp_dir = tempfile.mkdtemp()

        # Graphique des données traitées
        processed_data = self.main_controller.get_processed_data()
        if processed_data is not None and not processed_data.empty:
            plt.figure(figsize=(8, 5))
            processed_data['Chiffre_affaires'].plot(kind='bar')
            plt.title('Évolution du Chiffre d\'Affaires')
            graph_path = os.path.join(temp_dir, 'ca_evolution.png')
            plt.savefig(graph_path)
            plt.close()

            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Graphiques', 0, 1)
            pdf.image(graph_path, x=10, y=20, w=180)

        # Nettoyage des fichiers temporaires
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Erreur nettoyage fichiers temporaires: {str(e)}")