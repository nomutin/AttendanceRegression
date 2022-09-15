from datetime import date, timedelta

import pandas as pd

B4_students = ['Igarashi', 'Ishizuka', 'Imano', 'Nomura', 'Fujii']
students = [
    'Orui', 'Kusumoto', 'Wu', 'Nishimura', 'Hiramatsu', 'Ishii',
    'Saito', 'Chonabayashi', 'Igarashi', 'Ishizuka', 'Imano',
    'Nomura', 'Fujii', 'Macarena', 'Julia', 'Valentin'
]


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
