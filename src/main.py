from getch import getch

from .analysis import total_volume, pnl, renewable_forcasts, average_production, min_max_production, average_price_weak_weekend_price, average_product_value
from .backtesting.battery.main import run_battery_strategy
from .backtesting.da_id.main import run_da_id_strategy

print('========\nTask 1.1\n========')
print(f'Total buy volume: \t{total_volume.compute_total_buy_volume()}')
print(f'Total sell volume: \t{total_volume.compute_total_sell_volume()}')

pnl.all_strategy_pnl()
print('\n========\nTask 1.2\n========')
strategies_results = pnl.all_strategy_pnl()
if strategies_results is not None:    
    for strategy in strategies_results:
        print(f'{strategy["strategy"]} \t{strategy["pnl"]}')
else:
    print("No strategies found")
    
print('\n========\nTask 1.3\n========')
print(f"Please read readme file in order to see how to run the server")

print('\n========\nTask 2.1\n========')
forecast_sums = renewable_forcasts.get_forecast_sum()
if forecast_sums is not None:
    for key, value in forecast_sums.items():
        print(f"{key} \t{value}")
else:
    print("No forecast found")
    
print("""
========
Task 2.2
========
Please select an option:
(1) Show interactive chart
(2) Save chart image
      """)
while(1):
    selected_option =  getch()
    if selected_option == '1':
        average_production.get_average_production_charts()
        break
    elif selected_option == '2':
        average_production.get_average_production_charts(mode = 'save')
        break
    else:
        print("Invalid option selected")

print('\n========\nTask 2.3\n========')
average_value = average_product_value.get_average_product_value()
print(f"Average value for Wind Power in 2021: {average_value['Average wind value']:.2f} EUR/MWh")
print(f"Average value for PV Power in 2021: {average_value['Average PV value']:.2f} EUR/MWh")
print(f"Average Day Ahead Price in 2021: {average_value['Average DA price']:.2f} EUR/MWh")

print('\n========\nTask 2.4\n========')
min_max_renewable = min_max_production.find_min_max_production()
print("""Day with maximum renewable production:
    Date: \t"""+str(min_max_renewable['max']['Date'])+"""
    Total Renewable MWh: \t"""+str(min_max_renewable['max']['TotalRenewableMWh'])+"""
    DayAheadPriceHourlyEURMWh: \t"""+str(min_max_renewable['max']['DayAheadPriceHourlyEURMWh'])+"""
Day with minimum renewable production:
    Date: \t"""+str(min_max_renewable['min']['Date'])+"""
    Total Renewable MWh: \t"""+str(min_max_renewable['min']['TotalRenewableMWh'])+"""
    DayAheadPriceHourlyEURMWh: \t"""+str(min_max_renewable['min']['DayAheadPriceHourlyEURMWh']))

print('\n========\nTask 2.5\n========')
average_price_weak_weekend = average_price_weak_weekend_price.weekday_vs_weekend_prices()
print(f"Average Day Ahead Price during Weekdays: {average_price_weak_weekend['avg_weekday_price']:.2f} EUR/MWh")
print(f"Average Day Ahead Price during Weekends: {average_price_weak_weekend['avg_weekend_price']:.2f} EUR/MWh")

print('\n========\nTask 2.6\n========')
run_battery_strategy()

print('\n========\nTask 2.7\n========')
run_da_id_strategy()








# Quarter 2021Q1: Charge at 3:00, Discharge at 18:00
# Quarter 2021Q2: Charge at 14:00, Discharge at 20:00
# Quarter 2021Q3: Charge at 3:00, Discharge at 19:00
# Quarter 2021Q4: Charge at 3:00, Discharge at 18:00