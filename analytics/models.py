# models.py

# Define projected annual growth rates for each asset class
growth_rates = {
    "US Stock": 0.09,              # 9% annual growth
    "International Stock": 0.08,   # 8% annual growth
    "US Bond": 0.035,              # 3.5% annual growth
    "International Bond": 0.04     # 4% annual growth
}

asset_volatility = {
    "US Stock": 0.15,              # 15% volatility
    "International Stock": 0.16,   # 16% volatility
    "US Bond": 0.04,               # 4% volatility
    "International Bond": 0.05     # 5% volatility
}

#Define model portfolio advisory fee
model_fee = .0025 #.025% 

# Define model portfolios with allocations
model_portfolios = {
    "Conservative": {
        "VOO": 0.15,
        "VXUS": 0.20,
        "BND": 0.60,
        "VNQ": 0.05
    },
    "Moderately Conservative": {
        "VOO": 0.25,
        "VXUS": 0.25,
        "BND": 0.40,
        "VNQ": 0.10
    },
    "Balanced": {
        "VOO": 0.30,
        "VXUS": 0.25,
        "BND": 0.30,
        "VNQ": 0.15
    },
    "Moderately Aggressive": {
        "VOO": 0.40,
        "VXUS": 0.20,
        "BND": 0.15,
        "VNQ": 0.25
    },
    "Aggressive": {
        "VOO": 0.50,
        "VXUS": 0.15,
        "BND": 0.00,
        "VNQ": 0.35
    }
}