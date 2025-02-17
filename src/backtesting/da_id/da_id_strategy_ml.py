import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def preprocess_data(df):
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    df['Hour'] = df['Datetime'].dt.hour
    df['DayOfWeek'] = df['Datetime'].dt.dayofweek
    # df['Month'] = df['Datetime'].dt.month
    df['TotalRenewable'] = df['WindDayAheadForecastMW'] + df['PVDayAheadForecastMW']
    
    # Determine if it's beneficial to go long (buy on day-ahead, sell on intraday)
    df['Decision'] = (df['IntradayPriceHourlyEURMWh'] > df['DayAheadPriceHourlyEURMWh']).astype(int)
    
    return df

def create_model(df):
    features = ['Hour', 'DayOfWeek', 'TotalRenewable', 'DayAheadPriceHourlyEURMWh']
    X = df[features]
    y = df['Decision']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    
    return clf