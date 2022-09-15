import os
from datetime import date
from typing import Tuple

import pandas as pd
from DBtools import DataBaseConnection

from utils import B4_students, date_range, students


def get_data():
    os.makedirs('csvdata', exist_ok=True)
    dbc = DataBaseConnection(DB='dev')
    dbc.get_dataset()


def create_personal_data(name: str, path_to_raw_data: str,
                         initial_date: Tuple[int, ...] = (2021, 4, 4),
                         final_date: Tuple[int, ...] = (2022, 8, 1)) -> None:

    raw_df = pd.read_csv(path_to_raw_data)
    personal_df = raw_df[raw_df['name'] == name]

    # create attendance list(attend:1 ,not: 0)
    ymd_list = [int(d.strftime('%Y%m%d')) for d in
                date_range(date(*initial_date), date(*final_date))]
    attend_day_list = personal_df['ymd'].tolist()
    attend_list = [int(d in attend_day_list) for d in ymd_list]

    # create weekday list
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
    week_list = [[int(d.strftime('%A') == day) for d in
                  date_range(date(*initial_date), date(*final_date))]
                 for day in weekdays]

    # create degree list
    fix_d = 20220401
    if name in B4_students:
        b4_list = [int(int(d.strftime('%Y%m%d')) > fix_d) for d in
                   date_range(date(*initial_date), date(*final_date))]
        m1_list = [0 for _ in
                   date_range(date(*initial_date), date(*final_date))]
    else:
        b4_list = [int(int(d.strftime('%Y%m%d')) < fix_d) for d in
                   date_range(date(*initial_date), date(*final_date))]
        m1_list = [int(int(d.strftime('%Y%m%d')) > fix_d) for d in
                   date_range(date(*initial_date), date(*final_date))]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_list = []
    for month in months:
        month_list.append([int(d.strftime('%b') == month) for d in
                           date_range(date(*initial_date), date(*final_date))])

    data = {
        'ymd': ymd_list,
        'attendance': attend_list,
        'is_b4': b4_list,
        'is_m1': m1_list
    }
    data.update({k: v for k, v in zip(weekdays, week_list)})
    data.update({k: v for k, v in zip(months, month_list)})
    df = pd.DataFrame(data=data)
    df.set_index('ymd', inplace=True)
    df.to_csv(f'csvdata/{name}_personal_data.csv')


if __name__ == '__main__':
    # get_data()
    # name_to_upper('csvdata/dataset.csv', 'csvdata/dataset.csv')
    for student in students:
        create_personal_data(name=student,
                             path_to_raw_data='csvdata/dataset.csv')
