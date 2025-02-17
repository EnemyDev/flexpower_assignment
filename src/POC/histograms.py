import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm
from datetime import datetime
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_and_save_histograms(df):
    # Copy DataFrame to avoid fragmentation
    df = df.copy()
    
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    df['Hour'] = df['Datetime'].dt.hour
    df['QuarterHour'] = df['Datetime'].dt.minute // 15
    
    # Create new DataFrame with all necessary columns
    df_optimized = pd.DataFrame({
        'DayOfWeek': df['Datetime'].dt.day_name(),
        'Month': df['Datetime'].dt.month_name(),
        'Hour': df['Hour'],
        'QuarterHour': df['QuarterHour'],
        'DayAheadPriceHourlyEURMWh': df['DayAheadPriceHourlyEURMWh'],
        'IntradayPriceHourlyEURMWh': df['IntradayPriceHourlyEURMWh']
    })
    
    price_columns = ['DayAheadPriceHourlyEURMWh', 'IntradayPriceHourlyEURMWh']
    
    variables = [
        ('DayOfWeek', 'Day of Week'),
        ('Month', 'Month'),
        ('Hour', 'Hour'),
        ('QuarterHour', 'Quarter Hour')
    ]

    ensure_dir('histograms')  # Ensure the 'histograms' directory exists

    for price_col in price_columns:
        for var, var_label in variables:
            categories = df_optimized[var].unique()
            for cat in categories:
                subset = df_optimized[df_optimized[var] == cat]
                plt.figure(figsize=(12, 8))  # Slightly larger for more legend space
                
                # Histogram plot with increased bins
                ax = sns.histplot(data=subset, x=price_col, kde=True, bins=50)
                plt.title(f'Histogram of {price_col} - {var_label}: {cat}')
                plt.xlabel(f'{price_col} (EUR/MWh)')
                plt.ylabel('Frequency')
                
                # Calculate mean, median, mode, and perform Gaussian fit
                mean_value = subset[price_col].mean()
                median_value = subset[price_col].median()
                mode_series = subset[price_col].value_counts()
                mode_value = mode_series.index[0] if not mode_series.empty else None

                # Gaussian fit
                mu, std = stats.norm.fit(subset[price_col])
                
                # Calculate probabilities
                most_probable_price = mu
                least_probable_lower = mu - 3*std
                least_probable_upper = mu + 3*std
                prob_most = norm.pdf(mu, mu, std)
                prob_least_lower = norm.pdf(least_probable_lower, mu, std)
                prob_least_upper = norm.pdf(least_probable_upper, mu, std)
                
                # Plot mean and median lines
                plt.axvline(mean_value, color='r', linestyle='--', label=f'Mean: {mu:.2f}')
                plt.axvline(median_value, color='g', linestyle='--', label=f'Median: {median_value:.2f}')
                
                # Highlight bars between mean and median
                bin_edges = ax.containers[0].patches[0].get_x()
                bin_width = ax.containers[0].patches[1].get_x() - bin_edges
                for bar in ax.patches:
                    if bar.get_x() + bin_width >= min(mean_value, median_value) and bar.get_x() <= max(mean_value, median_value):
                        bar.set_color('orange')
                    
                    # Highlight mode bar in red
                    if mode_value is not None and bar.get_x() <= mode_value < bar.get_x() + bin_width:
                        bar.set_color('red')

                # Custom legend with matched handles and labels
                ax.legend(
                    handles=[
                        plt.Line2D([0], [0], color='b', linewidth=2, linestyle='-'),
                        plt.Line2D([0], [0], color='r', linewidth=2, linestyle='--'),
                        plt.Line2D([0], [0], color='g', linewidth=2, linestyle='--'),
                        plt.Rectangle((0, 0), 1, 1, color='orange'),
                        plt.Rectangle((0, 0), 1, 1, color='red'),
                        plt.Line2D([0], [0], color='none', marker='o', markersize=10, markerfacecolor='none', markeredgecolor='none')
                    ],
                    labels=[
                        'Kernel Density Estimate', 
                        f'Mean: {mu:.2f}', 
                        f'Median: {median_value:.2f}', 
                        'Between Mean & Median', 
                        f'Mode: {mode_value:.2f}' if mode_value is not None else 'Mode: Not Found',
                        f'Std Dev: {std:.2f}'
                    ],
                    title="Statistics:\n" +
                          f"Most Probable: {most_probable_price:.2f} ({prob_most:.4f})\n" +
                          f"Least Probable Below: {least_probable_lower:.2f} ({prob_least_lower:.4f})\n" +
                          f"Least Probable Above: {least_probable_upper:.2f} ({prob_least_upper:.4f})\n" +
                          f"1σ: {mu-std:.2f}-{mu+std:.2f} (68.27%)\n" +
                          f"2σ: {mu-2*std:.2f}-{mu+2*std:.2f} (95.45%)\n" +
                          f"3σ: {mu-3*std:.2f}-{mu+3*std:.2f} (99.73%)",
                    loc='center left', 
                    bbox_to_anchor=(1, 0.5)
                )
                
                plt.tight_layout()
                
                # Save the histogram into the 'histograms' folder, overwriting if it exists
                filename = f"histograms/{price_col.replace('EURMWh', '')}_{var}_{cat}.png"
                if os.path.exists(filename):
                    os.remove(filename)  # Remove existing file if present
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close()  # Close the figure to free up memory

# Load the CSV file with correct date format parsing
df = pd.read_csv('cleaned.csv', 
                 parse_dates=['time'], 
                 date_format='%m/%d/%y %H:%M')

create_and_save_histograms(df)

print("\n\nTutorial on Using Histograms for Strategy Formation:")

print("""
**How to Use These Histograms for Strategy Formation:**

1. **Understand Price Distribution:**
   - Each histogram shows how prices are distributed for a specific day or month. Look for skewness (asymmetry) or kurtosis (how heavy the tails are), which can indicate price volatility or stability.

2. **Identify Trends:**
   - **Days:** If certain days of the week consistently show lower or higher prices, consider:
     - Buying on days with lower average prices.
     - Selling on days when prices tend to peak.
   - **Months:** Similar to days, if there are seasonal patterns, you might:
     - Accumulate positions during months with lower prices.
     - Liquidate during expected high-price months.

3. **Probability of Price Levels:**
   - **Most Probable Prices:** Use the mean (printed as 'Most Probable Price') to set expectations for typical trading conditions. 
   - **Least Probable Prices:** Prices beyond three standard deviations from the mean are rare. These can be used to:
     - Set stop-loss or take-profit levels outside of normal price ranges.
     - Look for arbitrage opportunities if you see prices approaching these extremes.

4. **Risk Assessment:**
   - The standard deviation gives an idea of how much prices might typically fluctuate. Higher volatility might require:
     - More conservative position sizing.
     - More frequent adjustments to trading strategies.

5. **Strategy Development:**
   - **Day-Based Strategies:** Trading based on day of the week could involve setting automated trades for buying or selling at certain times or prices on specific days.
   - **Seasonal Trading:** Use monthly patterns to forecast when to enter or exit the market, considering seasonal demand changes or renewable energy production cycles.
   - **Price Thresholds:** Establish price thresholds for buying or selling based on where the bulk of the data lies (e.g., within one standard deviation of the mean).

6. **Scenario Planning:**
   - Use these distributions to simulate different market scenarios. How would your strategy perform if prices move outside the typical range?

7. **Combining with Other Data:**
   - Integrate these insights with weather forecasts, renewable energy production forecasts, or economic indicators for a more robust strategy. 

**Remember:**
- These histograms are based on historical data. Market conditions can change due to new policies, technological innovations, or unexpected events.
- Always validate strategies with backtesting and consider market liquidity, transaction costs, and potential slippage in real trading scenarios.
- The Kolmogorov-Smirnov test helps assess if you can trust the normal distribution assumptions; if not, your strategy might need adjustments for non-normal distribution behaviors.
""")