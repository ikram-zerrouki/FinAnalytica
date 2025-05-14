# Devise
CURRENCY = "DZD"

# Category names
CATEGORY_NAMES = {
    'liquidity': "Liquidité",
    'solvency': "Solvabilité",
    'profitability': "Rentabilité",
    'activity': "Activité"
}

# ... (le reste de votre fichier constants.py existant)



# Category names
CATEGORY_NAMES = {
    'liquidity': "Liquidité",
    'solvency': "Solvabilité",
    'profitability': "Rentabilité",
    'activity': "Activité"
}

# Interpretation thresholds
LIQUIDITY_THRESHOLDS = [
    (2, "Très bonne liquidité - L'entreprise peut facilement couvrir ses dettes court terme"),
    (1, "Liquidité satisfaisante - L'entreprise peut couvrir ses dettes court terme"),
    (0, "Liquidité insuffisante - Risque de difficultés à payer les dettes court terme")
]

DEBT_EQUITY_THRESHOLDS = [
    (0.5, "Structure financière très saine - Faible endettement"),
    (1, "Structure financière équilibrée - Endettement modéré"),
    (float('inf'), "Endettement élevé - Risque financier accru")
]

LEVERAGE_THRESHOLDS = [
    (2, "Faible levier - Peu d'effet de levier financier"),
    (5, "Levier modéré - Utilisation raisonnable de la dette"),
    (float('inf'), "Levier élevé - Forte dépendance à la dette")
]

INTEREST_COVERAGE_THRESHOLDS = [
    (5, "Très bonne capacité à couvrir les intérêts"),
    (2, "Capacité satisfaisante à couvrir les intérêts"),
    (0, "Capacité insuffisante - Risque de défaut sur les intérêts")
]

PROFITABILITY_THRESHOLDS = [
    (0.2, "Marge excellente - Très bonne rentabilité"),
    (0.1, "Marge satisfaisante - Rentabilité correcte"),
    (0, "Marge faible - Rentabilité insuffisante"),
    (-float('inf'), "Marge négative - Activité non rentable")
]

INVENTORY_TURNOVER_THRESHOLDS = [
    (10, "Rotation très rapide - Gestion des stocks excellente"),
    (5, "Rotation rapide - Bonne gestion des stocks"),
    (2, "Rotation moyenne - Gestion des stocks acceptable"),
    (0, "Rotation lente - Stocks potentiellement obsolètes")
]

DSO_THRESHOLDS = [
    (30, "Recouvrement très rapide - Excellente gestion clients"),
    (60, "Recouvrement rapide - Bonne gestion clients"),
    (90, "Recouvrement moyen - Gestion clients acceptable"),
    (float('inf'), "Recouvrement lent - Risque de créances douteuses")
]

DPO_THRESHOLDS = [
    (30, "Paiement rapide - Faible utilisation du crédit fournisseur"),
    (60, "Paiement dans les délais - Utilisation modérée du crédit fournisseur"),
    (90, "Paiement lent - Bonne utilisation du crédit fournisseur"),
    (float('inf'), "Paiement très lent - Risque de tensions avec les fournisseurs")
]

def get_interpretation(value, thresholds):
    for limit, interpretation in sorted(thresholds, reverse=True):
        if value >= limit:
            return interpretation
    return "Non interprétable"