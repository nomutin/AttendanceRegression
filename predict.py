from datetime import date
import math
import pickle

import numpy as np
import pandas as pd

from utils import B4_students, date_range, students


def get_regression_output():
    start_date = date(2022, 9, 1)
    end_date = date(2023, 3, 31)
    index_date = [d.strftime('%Y%m%d') for d in
                  date_range(start_date, end_date)]
    column_name = [n for n in students]
    all_data = []
    for today in date_range(start_date, end_date):
        day_data = []
        for name in students:
            data = {'is_b4': int(name in B4_students),
                    'is_m1': int(name not in B4_students),
                    }
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                        'Saturday', 'Sunday']
            weekday_data = {d: int(d == today.strftime('%A')) for d in weekdays}
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            month_data = {m: int(m == today.strftime('%b')) for m in months}
            data.update(weekday_data)
            data.update(month_data)
            input_df = pd.DataFrame(data=data, index=[today.strftime('%Y%m%d')])
            model_name = f'models/{name}_model.sav'
            model = pickle.load(open(model_name, 'rb'))
            res = model.predict_proba(input_df)[0][1]
            res = math.floor(sigmoid((res - 0.5) * 40) * 100)
            day_data.append(res)
        all_data.append(day_data)

    df = pd.DataFrame(data=all_data, index=index_date, columns=column_name)
    df.to_csv('outputs/model_output.csv')


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


if __name__ == '__main__':
    get_regression_output()
