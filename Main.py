import control.matlab as matlab
import matplotlib.pyplot as pyplot
import colorama


# Названия типовых звеньев
PROPORTIONAL_UNIT_NAME = "Безынерционное звено"
APERIODIC_UNIT_NAME = "Апериодическое звено"


def choose():  # Выбор звена и возврат его имени
    name = ""
    need_new_choice = True
    while need_new_choice:
        print(colorama.Style.RESET_ALL, end="")
        user_input = input("Введите номер команды: \n" +
                           "1 - " + PROPORTIONAL_UNIT_NAME + ";\n" +
                           "2 - " + APERIODIC_UNIT_NAME + ".\n")
        if user_input.isdigit():
            need_new_choice = False
            user_input = int(user_input)
            if user_input == 1:
                name = PROPORTIONAL_UNIT_NAME
            elif user_input == 2:
                name = APERIODIC_UNIT_NAME
            else:
                need_new_choice = True
                print(colorama.Fore.RED + "Недопустимое значение!")
        else:
            print(colorama.Fore.RED + "Пожалуйста, введите числовое значение!")
    return name


def get_unit(unit_name):  # Параметризация звена и возврат его передаточной функции
    unit = None
    t = "0"
    need_new_choice = True
    while need_new_choice:
        print(colorama.Style.RESET_ALL, end="")
        k = input("Введите коэффициент передачи звена (k): ")
        if unit_name == APERIODIC_UNIT_NAME:
            t = input("Введите постоянную времени звена (T): ")
        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            need_new_choice = False
            if unit_name == PROPORTIONAL_UNIT_NAME:
                unit = matlab.tf([k], [1])
            elif unit_name == APERIODIC_UNIT_NAME:
                unit = matlab.tf([k], [t, 1])
        else:
            print(colorama.Fore.RED + "Пожалуйста, введите числовое значение!")
    return unit


def make_graph(title, y, x):  # Ввод значений для отображения на графиках
    x_label = "Время t, с"
    y_label = ""
    pyplot.subplot(1, 1, 1)  # Одна строка, один столбец при отображении графика
    pyplot.grid(True)  # Отобразить линии сетки
    if title == "Переходная характеристика":
        pyplot.plot(x, y, "red")
        y_label = "h, о. е."
    elif title == "Импульсная характеристика":
        pyplot.plot(x, y, "orange")
        y_label = "w, о. е."
    pyplot.title(title)  # Добавить заголовок
    pyplot.xlabel(x_label)  # Добавить подпись оси абсцисс
    pyplot.ylabel(y_label)  # Добавить подпись оси ординат


if __name__ == "__main__":
    my_unit_name = choose()
    my_unit = get_unit(my_unit_name)

    print(my_unit_name)
    print("Передаточная функция звена W(s):")
    print(my_unit.__str__()[72:-1])

    time_line = [i / 1000 for i in range(1, 16000)]  # t = 0 - 16 с с шагом 1 мс

    [h, time] = matlab.step(my_unit, time_line)
    make_graph("Переходная характеристика", h, time)
    pyplot.show()  # Отрисовка характеристики

    [w, time] = matlab.impulse(my_unit, time_line)
    make_graph("Импульсная характеристика", w, time)
    pyplot.show()

"""
1) W(p) = k = 2
2) W(p) = k / (Tp + 1) = 3 / (4p + 1)
"""
