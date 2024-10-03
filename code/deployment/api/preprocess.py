# lets train a an ensemble model for a tabilar data
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple


def preprocess_data(df: pd.DataFrame, train: bool = True) -> pd.DataFrame or Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # delete last two digits from DepTime
    df['Hour'] = df['DepTime'].apply(lambda x: x // 100)
    df['Hour'] = df['Hour'].apply(lambda x: 0 if x == 24 else (1 if x == 25 else x))
    df['Minute'] = df['DepTime'] % 100

    # parts of the day
    df['Time_of_day'] = pd.cut(df['Hour'], bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'])

    # drop DepTime
    df.drop('DepTime', axis=1, inplace=True)

    df['Month'] = df['Month'].str[2:].astype(int)
    df['DayofMonth'] = df['DayofMonth'].str[2:].astype(int)

    df['Summer'] = df['Month'].isin([6, 7, 8])
    df['Autumn'] = df['Month'].isin([9, 10, 11])
    df['Winter'] = df['Month'].isin([12, 1, 2])
    df['Spring'] = df['Month'].isin([3, 4, 5])

    # combined features
    df['Route'] = df['Origin'] + '_' + df['Dest']

    df['DayOfWeek'] = df['DayOfWeek'].str[2:].astype(int)
    df['is_weekend'] = df['DayOfWeek'].apply(lambda x: 1 if x in [5, 6] else 0)

    df['UniqueCarrier_Origin'] = df['UniqueCarrier'] + "_" + df['Origin']
    df['UniqueCarrier_Dest'] = df['UniqueCarrier'] + "_" + df['Dest']

    # divide distance into bins
    df['Distance_split'] = pd.cut(df['Distance'], bins=[1, 250, 500, 1000, 2500, 5000], labels=['very_short', 'short', 'medium', 'long', 'very_long'])

    # drop column Distance
    df.drop('Distance', axis=1, inplace=True)

    # Step 1: Handle categorical features
    categorical_cols = ['UniqueCarrier', 'Origin', 'Dest', 'Route', 'Time_of_day', 'Distance_split',
                        'UniqueCarrier_Origin', 'UniqueCarrier_Dest']

    # Label encode categorical columns
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Step 2: Convert target 'dep_delayed_15min' into numerical (1 for 'Y', 0 for 'N')
    if train:
        df['dep_delayed_15min'] = df['dep_delayed_15min'].apply(lambda x: 1 if x == 'Y' else 0)

    # Step 3: Split features and target
    if train:
        y = df['dep_delayed_15min']
        X = df.drop('dep_delayed_15min', axis=1)
        # split into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        return X_train, X_val, y_train, y_val, X, y
    else:
        return df
