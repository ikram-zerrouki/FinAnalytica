"""from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os


class ReportGenerator:
    @staticmethod
    def generate_pdf_report(data, output_path):
        pdf = FPDF()
        pdf.set_auto_page_break(True, 15)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Rapport d\'Analyse Comptable', 0, 1, 'C')

        temp_dir = tempfile.mkdtemp()
        graph_path = os.path.join(temp_dir, 'ca_evolution.png')

        plt.figure(figsize=(8, 4))
        data['Chiffre_affaires'].plot(kind='bar')
        plt.title('Évolution du Chiffre d\'Affaires')
        plt.savefig(graph_path)
        plt.close()

        pdf.image(graph_path, x=10, y=30, w=180)
        pdf.output(output_path)
        return True"""

from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
from datetime import datetime
from utils.constants import CATEGORY_NAMES


class ReportGenerator:
    @staticmethod
    def generate_financial_report(ratios, output_path):
        """Génère un rapport PDF complet avec les ratios financiers"""
        pdf = FPDF()
        pdf.set_auto_page_break(True, 15)

        # Page de titre
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Rapport d\'Analyse Financière', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Généré le {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        pdf.ln(20)

        # Génération des graphiques
        temp_dir = tempfile.mkdtemp()

        # Graphique pour chaque catégorie
        for category, ratios_data in ratios.items():
            # Création du graphique
            plt.figure(figsize=(8, 4))
            labels = [r['description'] for r in ratios_data.values()]
            values = [r['value'] for r in ratios_data.values()]

            plt.bar(labels, values)
            plt.title(f"Ratios de {CATEGORY_NAMES.get(category, category)}")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            graph_path = os.path.join(temp_dir, f'{category}.png')
            plt.savefig(graph_path)
            plt.close()

            # Ajout au PDF
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, CATEGORY_NAMES.get(category, category), 0, 1)
            pdf.image(graph_path, x=10, y=30, w=180)

        pdf.output(output_path)
        return True