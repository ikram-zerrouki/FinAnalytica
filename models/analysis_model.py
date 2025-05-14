import pandas as pd
import numpy as np
from models.bilan_model import BilanModel


class AnalysisModel(BilanModel):
    def extract_net_value_from_df(self, df, keyword):
        norm_keyword = self.normalize(keyword)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                cell_value = df.iat[i, j]
                cell = self.normalize(cell_value)

                if norm_keyword == cell:
                    if j + 3 < len(df.columns):
                        val = self.clean_value(df.iat[i, j + 3])
                        if isinstance(val, (int, float)):
                            return val

                    for row in range(20):
                        for col in range(len(df.columns)):
                            header_value = df.iat[row, col] if row < len(df) else ""
                            if isinstance(header_value, str) and "net" in self.normalize(header_value):
                                if i < len(df) and col < len(df.columns):
                                    val = self.clean_value(df.iat[i, col])
                                    if isinstance(val, (int, float)):
                                        return val

        return self.extract_value_from_df(df, keyword)

    def extract_value_from_df(self, df, keyword):
        norm_keyword = self.normalize(keyword)

        # First attempt: exact match
        for i in range(len(df)):
            for j in range(len(df.columns)):
                cell_value = df.iat[i, j]
                cell = self.normalize(cell_value)

                if norm_keyword == cell:
                    for k in range(j + 1, len(df.columns)):
                        val = self.clean_value(df.iat[i, k])
                        if isinstance(val, (int, float)) and val != 0:
                            return val

                    if i + 1 < len(df):
                        for k in range(len(df.columns)):
                            val = self.clean_value(df.iat[i + 1, k])
                            if isinstance(val, (int, float)) and val != 0:
                                return val

        # Second attempt: partial match
        for i in range(len(df)):
            for j in range(len(df.columns)):
                cell_value = df.iat[i, j]
                if cell_value is None or pd.isna(cell_value):
                    continue

                cell = self.normalize(cell_value)
                if not cell or not norm_keyword:
                    continue

                if cell in norm_keyword or norm_keyword in cell:
                    for k in range(j + 1, len(df.columns)):
                        val = self.clean_value(df.iat[i, k])
                        if isinstance(val, (int, float)) and val != 0:
                            return val

                    if i + 1 < len(df):
                        for k in range(len(df.columns)):
                            val = self.clean_value(df.iat[i + 1, k])
                            if isinstance(val, (int, float)) and val != 0:
                                return val

        return 0

    def load_excel_data(self, file_path):
        try:
            xls = pd.ExcelFile(file_path)
            self.raw_data = {}

            for year in ['2021', '2022', '2023']:
                df = pd.read_excel(xls, sheet_name=year).fillna("")
                year_int = int(year)
                self.raw_data[year_int] = self._extract_year_data(df)

            self._process_data()
            self._analyze_trends()
            self.data_updated.emit()
            return True, "Données chargées avec succès"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def _extract_year_data(self, df):
        return {
            'Chiffre_affaires': self.extract_value_from_df(df, "PROOUCTION DE L'EXERCICE"),
            'Achats_consommes': self.extract_value_from_df(df, "Achats consommes"),
            'Services_exterieurs': self.extract_value_from_df(df, "Services extérieurs et autres consornmations"),
            'Charges_personnel': self.extract_value_from_df(df, "Charges de personnel"),
            'Impots_taxes': self.extract_value_from_df(df, "Impots, taxes et versements assimilés"),
            'Dotations_amortissements': self.extract_value_from_df(df,
                                                                   "Dotations aux amortissernonts, provisions et portos do valeurs"),
            'Resultat_net': self.extract_value_from_df(df, "RESULTAT NET DE L'EXERCICE"),
            'Valeur_ajoutee': self.extract_value_from_df(df, "VALEUR AJOUTEE D'EXPLOITATION"),
            'EBE': self.extract_value_from_df(df, "EXCEDENT BRUT D'EXPLOITATION"),
            'Total_actif': self.extract_net_value_from_df(df, "TOTAL GENERAL ACTIF"),
            'Stocks': self.extract_net_value_from_df(df, "Stocks et encours"),
            'Tresorerie': self.extract_net_value_from_df(df, "Trésorerie"),
            'Actif_courant': self.extract_net_value_from_df(df, "TOTAL ACTIF COURANT"),
            'Capitaux_propres': self.extract_value_from_df(df, "TOTAL 1"),
            'Total_passif': self.extract_value_from_df(df, "TOTAL GENERAL PASSIF"),
            'Dettes_fournisseurs': self.extract_value_from_df(df, "Fournisseurs et comptes rattaches"),
            'Passif_courant': self.extract_value_from_df(df, "TOTAL 3"),
            'Total_charges': self.extract_value_from_df(df, "TOTAL DES CHARGES OES ACTIVITES ORDINAIRES")
        }

    def _process_data(self):
        self.processed_data = pd.DataFrame(self.raw_data).T

        # Calculs des indicateurs
        self.processed_data['Cout_production'] = self.processed_data['Achats_consommes'] + self.processed_data[
            'Services_exterieurs']
        self.processed_data['Charges_variables'] = self.processed_data['Achats_consommes'] + self.processed_data[
            'Services_exterieurs']
        self.processed_data['Charges_fixes'] = self.processed_data['Charges_personnel'] + self.processed_data[
            'Impots_taxes']
        self.processed_data['Marge_brute'] = self.processed_data['Chiffre_affaires'] - self.processed_data[
            'Cout_production']
        self.processed_data['Taux_marge_brute'] = self.processed_data['Marge_brute'] / self.processed_data[
            'Chiffre_affaires'] * 100
        self.processed_data['Taux_rentabilite'] = self.processed_data['Resultat_net'] / self.processed_data[
            'Chiffre_affaires'] * 100
        self.processed_data['ROE'] = self.processed_data['Resultat_net'] / self.processed_data['Capitaux_propres'] * 100
        self.processed_data['ROA'] = self.processed_data['Resultat_net'] / self.processed_data['Total_actif'] * 100
        self.processed_data['Ratio_productivite'] = self.processed_data['Valeur_ajoutee'] / self.processed_data[
            'Charges_personnel']
        self.processed_data['Ratio_endettement'] = (self.processed_data['Total_passif'] - self.processed_data[
            'Capitaux_propres']) / self.processed_data['Capitaux_propres'] * 100
        self.processed_data['Ratio_liquidite'] = self.processed_data['Actif_courant'] / self.processed_data[
            'Passif_courant']
        self.processed_data['BFR'] = self.processed_data['Stocks'] + (
                    self.processed_data['Actif_courant'] - self.processed_data['Stocks'] - self.processed_data[
                'Tresorerie']) - (self.processed_data['Passif_courant'])
        self.processed_data['Taux_taxes'] = self.processed_data['Impots_taxes'] / self.processed_data[
            'Chiffre_affaires'] * 100
        self.processed_data['Variation_stocks'] = self.processed_data['Stocks'].diff()
        self.processed_data['Variation_CA'] = self.processed_data['Chiffre_affaires'].diff() / self.processed_data[
            'Chiffre_affaires'].shift(1) * 100

    def _analyze_trends(self):
        df = self.processed_data
        self.trends = {
            'tendance_ca': "En croissance" if df['Chiffre_affaires'].iloc[-1] > df['Chiffre_affaires'].iloc[
                0] else "En baisse",
            'tendance_rentabilite': "Amélioration" if df['Taux_rentabilite'].iloc[-1] > df['Taux_rentabilite'].iloc[
                0] else "Détérioration",
            'situation_liquidite': "Excellente" if df['Ratio_liquidite'].mean() > 1.5 else "Bonne" if df[
                                                                                                          'Ratio_liquidite'].mean() > 1 else "Problématique",
            'situation_endettement': "Faible" if df['Ratio_endettement'].mean() < 50 else "Modéré" if df[
                                                                                                          'Ratio_endettement'].mean() < 100 else "Élevé",
            'tendance_marge': "Amélioration" if df['Taux_marge_brute'].iloc[-1] > df['Taux_marge_brute'].iloc[
                0] else "Détérioration"
        }