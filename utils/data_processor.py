import pandas as pd

class DataProcessor:
    @staticmethod
    def calculate_indicators(raw_data):
        df = pd.DataFrame(raw_data).T
        df['Cout_production'] = df['Achats_consommes'] + df['Services_exterieurs']
        df['Marge_brute'] = df['Chiffre_affaires'] - df['Cout_production']
        df['Taux_marge_brute'] = df['Marge_brute'] / df['Chiffre_affaires'] * 100
        return df