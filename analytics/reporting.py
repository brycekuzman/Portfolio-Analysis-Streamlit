import matplotlib.pyplot as plt

def plot_growth(cumulative, title="Growth of $1"):
    plt.figure(figsize=(10,6))
    cumulative.plot()
    plt.title(title)
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)
    return plt
