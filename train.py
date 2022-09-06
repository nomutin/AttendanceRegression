import os
import pickle

import pandas as pd
from DBtools import english_names
from sklearn.ensemble import AdaBoostClassifier


def train_model(name: str):
    os.makedirs('models', exist_ok=True)
    df = pd.read_csv(f'csvdata/{name}_personal_data.csv').set_index('ymd')
    target_column = 'attendance'
    input_df = df[[c for c in df.columns if not c == target_column]]
    target_df = df[target_column]

    model = AdaBoostClassifier(n_estimators=10, learning_rate=1)
    model.fit(input_df, target_df)
    pickle.dump(model, open(f'models/{name}_model.sav', 'wb'))


if __name__ == '__main__':
    for name in english_names:
        train_model(name)
