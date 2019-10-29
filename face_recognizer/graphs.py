def graphs(user_answers = [2,3,4,5,1,3,4],
            subjects = ['Матанализ', 'Линейка', 'Комбинаторика', 'Теорвер', 'Python', 'C++', 'Алгоритмы']):
        
    """В функцию передавать количество правильных ответов и названия предметов сответственно"""

    import matplotlib.pyplot as plt
    import matplotlib as mp
    import numpy as np 
    
    number_of_questions = 5
    
    fig, ax = plt.subplots(figsize=(15,15))

    # set width of bar
    barWidth = 0.8

    data_normalizer = mp.colors.Normalize()
    color_map = mp.colors.LinearSegmentedColormap(
        "my_map",
        {
            "red": [(0, 1.0, 1.0),
                    (1.0, .5, .5)],
            "green": [(0, 0.5, 0.5),
                      (1.0, 0, 0)],
            "blue": [(0, 0.50, 0.5),
                     (1.0, 0.5, 0)]
        }
    )

    # Plot a bar graph:
    ax.bar(
        subjects,
        user_answers,
        width = barWidth,
        align="center",
        color=color_map(data_normalizer(user_answers))
    )

    ax.set_xticklabels(subjects, fontsize = 15)
    ax.set_yticklabels(labels = list(range(number_of_questions + 1)), fontsize = 20)

    ax.set_title("Ваши результаты", fontsize = 20)
    
    
    # СОХРАНЕНИЕ КАРТИНКИ
    plt.savefig("user_test_results.jpg", dpi = 300)