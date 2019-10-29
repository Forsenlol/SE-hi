import pandas as pd
import ast


def get_alumni_stat(alumni_id):
    df = pd.read_csv('data/dataset.csv')

    place = df.place[alumni_id]

    if place == 'au':
        info_dict = ast.literal_eval(df.iloc[alumni_id]['info'])
        output = (f'Вы выглядите, как выпускник Академического Университета '
                  f'*{df.name[alumni_id]}*. Почитайте про его успехи: \n')
        for k, v in info_dict.items():
            output += f'*{k}:* {v}\n'
    elif place == 'csc':
        info = df.iloc[alumni_id].info
        output = (f'Вы выглядите, как выпускник Computer Science Center '
                  f'*{df.name[alumni_id]}*. \n')
        if not pd.isnull(info):
            output += f'Почитайте его отзыв про CSC: _{info}_'
    elif place == 'itmo':
        info = df.iloc[alumni_id].info.split(':')[-1]
        output = (f'Вы выглядите, как выпускник магистерской программы ИТМО '
                  f'Software Engineering *{df.name[alumni_id]}*. \n')
        output += f'Его тема диплома:{info}'

    return output
