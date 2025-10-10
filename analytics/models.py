# models.py

# Asset class growth rates and volatility (annual)
growth_rates = {
    "US Equities": 0.10,
    "International Equities": 0.09,
    "Core Fixed Income": 0.04,
    "Alternatives": 0.08
}

asset_volatility = {
    "US Equities": 0.18,
    "International Equities": 0.20,
    "Core Fixed Income": 0.05,
    "Alternatives": 0.15
}

#Define model portfolio advisory fee
model_fee = .0025 #.025% 

# Define model portfolios with allocations
model_portfolios = {
    "Conservative": {
        "US Equities": 0.15,
        "International Equities": 0.20,
        "Core Fixed Income": 0.60,
        "Alternatives": 0.05
    },
    "Moderately Conservative": {
        "US Equities": 0.25,
        "International Equities": 0.25,
        "Core Fixed Income": 0.40,
        "Alternatives": 0.10
    },
    "Balanced": {
        "US Equities": 0.30,
        "International Equities": 0.25,
        "Core Fixed Income": 0.30,
        "Alternatives": 0.15
    },
    "Moderately Aggressive": {
        "US Equities": 0.40,
        "International Equities": 0.20,
        "Core Fixed Income": 0.15,
        "Alternatives": 0.25
    },
    "Aggressive": {
        "US Equities": 0.50,
        "International Equities": 0.15,
        "Core Fixed Income": 0.00,
        "Alternatives": 0.35
    }
}