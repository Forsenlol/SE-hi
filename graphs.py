# import matplotlib.pyplot as plt
# import matplotlib as mp
# import numpy as np
#
# def graphs(name, user_answers = [2,3,4,5,1,3,4],
#             subjects = ['Матанализ', 'Линейка', 'Комбинаторика', 'Теорвер', 'Python', 'C++', 'Алгоритмы']):
#
#     """В функцию передавать количество правильных ответов и названия предметов сответственно"""
#
#     number_of_questions = 5
#
#     fig, ax = plt.subplots(figsize=(15,15))
#
#     # set width of bar
#     barWidth = 0.8
#
#     data_normalizer = mp.colors.Normalize()
#     color_map = mp.colors.LinearSegmentedColormap(
#         "my_map",
#         {
#             "red": [(0, 1.0, 1.0),
#                     (1.0, .5, .5)],
#             "green": [(0, 0.5, 0.5),
#                       (1.0, 0, 0)],
#             "blue": [(0, 0.50, 0.5),
#                      (1.0, 0.5, 0)]
#         }
#     )
#
#     # Plot a bar graph:
#     ax.bar(
#         subjects,
#         user_answers,
#         width = barWidth,
#         align="center",
#         color=color_map(data_normalizer(user_answers))
#     )
#
#     ax.set_xticklabels(subjects, fontsize = 15)
#     ax.set_ylim([0, 5])
#     ax.set_yticklabels(list(range(number_of_questions + 1)), fontsize = 20)
#
#     ax.set_title("Ваши результаты", fontsize = 20)
#
#
#     # СОХРАНЕНИЕ КАРТИНКИ
#     plt.savefig(name, dpi = 300)

import chart_studio
def graphs(name, user_answers = [2,3,4,5,1,3,4],
           subjects = ['Матанализ', 'Линейка', 'Комбинаторика', 'Теорвер', 'Python', 'C++', 'Алгоритмы']):
    trace1 = {
              "x": user_answers,
              "y": subjects,
              "orientation": "h",
              "type": "bar",
            }
    layout = {"title": "Результаты тестирования",
              "font": {"color": "#757575", "family": "Roboto","size": 36},
                "autosize": False,
                "height": 754,
                "width": 1350,
                "margin": {
                    "r": 50,
                    "t": 100,
                    "b": 50,
                    "l": 250,
                    "pad": 15
                },

                "bargap": 0.5,
                "showlegend": False,

                "xaxis": {
                    "showgrid": True,
                    "showline": False,
                    "showticklabels": True,
                    "zeroline": False,
                    "tickfont": {"color": "#757575", "family": "Roboto","size": 24},
                    "domain": [0, 1],
                    "range": [0,5]
                },

                "yaxis": {
                    "showline": True,
                    "tickfont": {
                        "size": 24,
                        "family": "Roboto",
                        "color": "#757575"
                    },
                    "type": "category",
                    "zeroline": False,
                    }
                }

    data = [trace1]
    chart_studio.plotly.image.save_as(dict(data=data, layout=layout),
                                filename = name, scale=3)
