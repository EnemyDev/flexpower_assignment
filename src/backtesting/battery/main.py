import pandas as pd
import matplotlib.pyplot as plt
import uuid
from ...data_processing.provider import load_cleaned_data
from ...analysis.best_hours import find_best_hours
from .battery_strategy import find_best_quarterly_strategy
from .battery_backtest import calculate_metrics, backtest_and_cache
from .visualisation import plot_equity_curves, plot_quarterly_best_strategy

def run_battery_strategy():
    df = load_cleaned_data()

    price_columns = ['DayAheadPriceHourlyEURMWh', 'IntradayPriceHourlyEURMWh']
    metrics_comparison = {}
    strategy_cache = {}

    for price_col in price_columns:
        plot_equity_curves(df, price_col, strategy_cache)
        # @TODO debug wiered results
        # plot_quarterly_best_strategy(df, price_col, strategy_cache)

        charge_hours, discharge_hours = find_best_hours(df, price_col)
        best_annual_profit = 0
        best_annual_strategy = None
        for ch in charge_hours:
            for dh in discharge_hours:
                strategy_name = f"annual_{ch}_{dh}_{price_col}"
                strategy = backtest_and_cache(df, ch, dh, strategy_name, price_col, strategy_cache)
                metrics = calculate_metrics(strategy)
                metrics_comparison[f"{price_col}_annual_{ch}_{dh}"] = metrics
                print(f"Strategy ({price_col}): Charge {ch}:00 - Discharge {dh}:00")
                # print(f"  Maximum Drawdown: {metrics[0]:.2f}")
                # print(f"  Maximum Runup: {metrics[1]:.2f}")
                print(f"  Maximum Win Streak: {metrics[2]}")
                print(f"  Maximum Lose Streak: {metrics[3]}")
                print(f"  Total Wins: {metrics[4]}")
                print(f"  Total Losses: {metrics[5]}")
                print(f"  Final Cumulative Profit: {metrics[6]:.2f}\n")
                if metrics[6] > best_annual_profit:  # Final Cumulative Profit
                    best_annual_profit = metrics[6]
                    best_annual_strategy = metrics

        metrics_comparison[f"best_annual_{price_col}"] = best_annual_strategy

        # @TODO debug wiered results
        # Calculate and print metrics for the best quarterly strategy
        # best_quarterly_strategies = find_best_quarterly_strategy(df, price_col, strategy_cache)
        # all_strategies = []
        # for quarter, group in df.groupby('Quarter'):
        #     if quarter in best_quarterly_strategies:
        #         charge_hour, discharge_hour = best_quarterly_strategies[quarter]
        #         strategy_name = f"quarterly_{charge_hour}_{discharge_hour}_{price_col}_{quarter}"
        #         strategy = backtest_and_cache(group, charge_hour, discharge_hour, strategy_name, price_col, strategy_cache)

        #         if not strategy.empty:
        #             if all_strategies:
        #                 last_profit = all_strategies[-1]['Cumulative_Profit'].iloc[-1]
        #                 strategy['Cumulative_Profit'] += last_profit
        #             all_strategies.append(strategy)

        # if all_strategies:
        #     quarterly_strategy = pd.concat(all_strategies, ignore_index=True)
        #     quarterly_metrics = calculate_metrics(quarterly_strategy)
        #     metrics_comparison[f"best_quarterly_{price_col}"] = quarterly_metrics
        #     print(f"Best Quarterly Strategy Metrics ({price_col}):")
        #     # print(f"  Maximum Drawdown: {quarterly_metrics[0]:.2f}")
        #     # print(f"  Maximum Runup: {quarterly_metrics[1]:.2f}")
        #     print(f"  Maximum Win Streak: {quarterly_metrics[2]}")
        #     print(f"  Maximum Lose Streak: {quarterly_metrics[3]}")
        #     print(f"  Total Wins: {quarterly_metrics[4]}")
        #     print(f"  Total Losses: {quarterly_metrics[5]}")
        #     print(f"  Final Cumulative Profit: {quarterly_metrics[6]:.2f}\n")

    print("\nComparison of DA vs ID Prices:")
    for strategy_type in ['best_annual', 'best_quarterly']:
        da_profit = metrics_comparison[f"{strategy_type}_DayAheadPriceHourlyEURMWh"][6] if f"{strategy_type}_DayAheadPriceHourlyEURMWh" in metrics_comparison else 0
        id_profit = metrics_comparison[f"{strategy_type}_IntradayPriceHourlyEURMWh"][6] if f"{strategy_type}_IntradayPriceHourlyEURMWh" in metrics_comparison else 0
        
        profit_diff = id_profit - da_profit
        better_market = "Intraday" if profit_diff > 0 else "Day-Ahead" if profit_diff < 0 else "Equal"
        print(f"{strategy_type.capitalize()} Strategy:")
        print(f"  Profit Difference (ID - DA): {profit_diff:.2f}")
        print(f"  Better Market: {better_market}")
        print()

if __name__ == "__main__":
    run_battery_strategy()