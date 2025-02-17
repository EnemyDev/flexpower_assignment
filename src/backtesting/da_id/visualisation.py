from matplotlib import pyplot as plt

def plot_simple_strategy(df):
    plt.figure(figsize=(15, 7))
    plt.plot(df['Datetime'].dt.date, df['Cumulative_Profit'])
    plt.title('Trading Strategy Performance - Buy on Day-Ahead if Intraday Typically Higher (100 MW)')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit (EUR)')
    plt.grid(True)
    plt.show()

def plot_ml_strategy(df):
    plt.figure(figsize=(15, 7))
    plt.plot(df['Datetime'].dt.date, df['Cumulative_Profit'])
    plt.title('Enhanced Trading Strategy Performance - Using Time, Renewables, and Prices')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit (EUR)')
    plt.grid(True)
    plt.show()
