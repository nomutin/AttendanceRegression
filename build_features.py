import os
from datetime import date, timedelta
from typing import Tuple

import pandas as pd
from DBtools import DataBaseConnection, english_names

B4_students = ['Igarashi', 'Ishizuka', 'Imano', 'Nomura', 'Fujii']


def get_data():
    os.makedirs('csvdata', exist_ok=True)
    dbc = DataBaseConnection(DB='dev')
    dbc.get_dataset()


def name_to_upper(input_file_name: str, output_file_name: str) -> None:
    df = pd.read_csv(input_file_name)
    for i, _ in df.iterrows():
        raw_name = df.at[i, 'name']
        processed_name = raw_name[0].upper() + raw_name[1:]
        df.at[i, 'name'] = processed_name
    df.to_csv(output_file_name)


def date_range(start: date, stop: date, step=timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step


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

    data = {
        'ymd': ymd_list,
        'attendance': attend_list,
        'is_b4': b4_list,
        'is_m1': m1_list
    }
    data.update({k: v for k, v in zip(weekdays, week_list)})
    df = pd.DataFrame(data=data)
    df.set_index('ymd', inplace=True)
    df.to_csv(f'csvdata/{name}_personal_data.csv')


if __name__ == '__main__':
    get_data()
    name_to_upper('csvdata/dataset.csv', 'csvdata/dataset.csv')
    for name in english_names:
        create_personal_data(name=name, path_to_raw_data='csvdata/dataset.csv')
