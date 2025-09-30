
from .models import model_portfolios


def get_user_portfolio():
    """Get user's current portfolio input."""
    print("Enter your current portfolio (ticker: dollar_amount):")
    print("Example: AAPL:10000,MSFT:5000")
    print("Or press Enter to use default: AAPL:10000,PULS:10000,VOO:20000")
    
    user_input = input("Portfolio: ").strip()
    
    if not user_input:
        return {"AAPL": 10000, "PULS": 10000, "VOO": 20000}
    
    portfolio = {}
    try:
        for item in user_input.split(','):
            ticker, amount = item.strip().split(':')
            portfolio[ticker.upper()] = float(amount)
        return portfolio
    except ValueError:
        print("Invalid format. Using default portfolio.")
        return {"AAPL": 10000, "PULS": 10000, "VOO": 20000}


def get_model_portfolio_choice():
    """Get user's model portfolio selection."""
    print("\nAvailable Model Portfolios:")
    for i, name in enumerate(model_portfolios.keys(), 1):
        print(f"{i}. {name}")
        allocations = model_portfolios[name]
        for ticker, weight in allocations.items():
            print(f"   {ticker}: {weight:.0%}")
        print()
    
    while True:
        try:
            choice = input("Select model portfolio (1-5): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(model_portfolios):
                portfolio_name = list(model_portfolios.keys())[choice_num - 1]
                return portfolio_name, model_portfolios[portfolio_name]
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Invalid input. Please enter a number 1-5.")
        except KeyboardInterrupt:
            print("\nUsing default: Conservative portfolio")
            return "Conservative", model_portfolios["Conservative"]
