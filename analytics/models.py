# models.py

# Define projected annual growth rates for each asset class
growth_rates = {
    "US Equities": 0.10,           # 10% annual growth
    "International Equities": 0.08, # 8% annual growth
    "Core Fixed Income": 0.04,      # 4% annual growth
    "Alternatives": 0.11            # 11% annual growth
}

#Define model portfolio advisory fee
model_fee = .0025 #.025% 

# Define model portfolios with allocations
model_portfolios = {
    "Conservative": {
        "VOO": 0.25,
        "VXUS": 0.20,
        "BND": 0.50,
        "VNQ": 0.05
    },
    "Moderately Conservative": {
        "VOO": 0.30,
        "VXUS": 0.25,
        "BND": 0.35,
        "VNQ": 0.10
    },
    "Balanced": {
        "VOO": 0.35,
        "VXUS": 0.30,
        "BND": 0.25,
        "VNQ": 0.10
    },
    "Moderately Aggressive": {
        "VOO": 0.40,
        "VXUS": 0.35,
        "BND": 0.15,
        "VNQ": 0.10
    },
    "Aggressive": {
        "VOO": 0.45,
        "VXUS": 0.35,
        "BND": 0.10,
        "VNQ": 0.10
    }
}