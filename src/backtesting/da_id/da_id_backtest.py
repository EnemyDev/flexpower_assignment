from .visualisation import plot_simple_strategy, plot_ml_strategy

def backtest_simple_strategy(df, buy_hours):
    df = df.sort_values('Datetime')
    
    # Apply strategy: Buy on day-ahead if the hour is in our 'buy_hours' list
    df['Decision'] = df['Datetime'].dt.hour.isin(buy_hours)
    df['Transaction'] = df['Decision'].astype(int)  # 1 for buy on day-ahead, 0 for no action
    
    # Adjust profit calculation for 100 MW position
    df['Profit'] = df['Transaction'] * (df['IntradayPriceHourlyEURMWh'] - df['DayAheadPriceHourlyEURMWh']) * 100  # 100 MW
    
    # Cumulative performance
    df['Cumulative_Profit'] = df['Profit'].cumsum()
    print(f"\nThe simple strategy, trading 100MWH produced {df['Cumulative_Profit'].values[-1:][0]} profit\n")
    plot_simple_strategy(df)
    return df
    # Plotting the strategy performance
    
def backtest_ml_strategy(df, model):
    # Make sure we're working with a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Predict using the model
    features = ['Hour', 'DayOfWeek', 'TotalRenewable', 'DayAheadPriceHourlyEURMWh']
    df['Predicted_Decision'] = model.predict(df[features])
    
    # Calculate profit based on predictions
    df['Profit'] = df['Predicted_Decision'] * (df['IntradayPriceHourlyEURMWh'] - df['DayAheadPriceHourlyEURMWh']) * 100  # 100 MW
    
    # Cumulative performance
    df['Cumulative_Profit'] = df['Profit'].cumsum()
    #@TODO implement metrics and trades exports.
    metrics = calculate_metrics(df)
    print(f"\nThe ML strategy, trading 100MWH produced {df['Cumulative_Profit'].values[-1:][0]} profit\n")
    plot_ml_strategy(df)
    return df
    
def calculate_metrics(df):
    pass
