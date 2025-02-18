import pandas as pd
import matplotlib.pyplot as plt
from ...data_processing.provider import load_cleaned_data
from .da_id_strategy_simple import find_spread_hours
from .da_id_strategy_ml import preprocess_data, create_model
from .da_id_backtest import backtest_simple_strategy, backtest_ml_strategy
from .visualisation import plot_combined_strategy


def run_da_id_strategy():
    df = load_cleaned_data()

    buy_hours = find_spread_hours(df)
    print("Strategy Explanation:")
    print("- This strategy uses historical data to identify hours where intraday prices are typically higher than day-ahead prices.")
    print("- We buy on the day-ahead market for those hours, assuming the trend will continue, with a 100 MW position.")
    print("- This approach does not use future intraday prices but relies on historical patterns, making it more practical for real-world application.")
    print("- Performance might vary if market conditions change or if our historical pattern analysis does not hold for future periods.")
    print("- Further enhancements could include seasonal adjustments, weekday/weekend differentiation, or incorporating weather forecasts.")
    backtest_simple_strategy(df, buy_hours)
    sdf2 = df.iloc[len(df) // 2:]
    s_df = backtest_simple_strategy(sdf2,buy_hours)
    df = preprocess_data(df)
    half_length = len(df) // 2
    df1 = df.iloc[:half_length]  # First half for training
    df2 = df.iloc[half_length:]  # Second half for testing
    model = create_model(df1)
    
    print("Strategy Explanation:")
    print("- This strategy uses machine learning to predict when to go long based on time, day, season, and renewable production.")
    print("- It considers buying on day-ahead if the prediction suggests intraday prices will be higher, with a 100 MW position.")
    print("- Factors like hour, day of week, and total renewable production are used to inform these decisions.")
    print("- The model's accuracy gives an idea of how well historical patterns predict future price movements.")
    print("- Real-world application would need to account for transaction costs, market impact, and further variables.")
    ml_df = backtest_ml_strategy(df2,model)
    plot_combined_strategy(s_df, ml_df)
    
def calculate_metrics(df):
    pass
    
if __name__ == "__main__":
    run_da_id_strategy()
    