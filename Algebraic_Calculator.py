import re

allowed_chars = r'^[0-9xyz\+\-\*\(\)\s]+$'
ans = ''
def processing_vars(count: int) -> str:
    global ans
    if count != 0:
        if len(ans) > 0 and count > 0:
            ans += '+'
        if count == 1:
            ans += 'z'
        elif count == -1:
            ans += '-z'
        else:
            ans += f"{count}*z"
    return ans


def calc(inp):
    # Проверка корректности входных данных
    if not re.match(allowed_chars, inp):
        return "Недопустимое выражение"
    if inp.count('(') != inp.count(')'):
        return "Недопустимое выражение"

    try:
        inp = inp.replace(' ', '')  # Удаление пробелов
        x, y, z = 0, 0, 0  # Начальные значения переменных

        # Вычисление константы (без переменных)
        remain = eval(inp, {'x': x, 'y': y, 'z': z})

        # Вычисление коэффициентов для x, y, z
        x, y, z = 1, 0, 0
        x_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain

        x, y, z = 0, 1, 0
        y_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain

        x, y, z = 0, 0, 1
        z_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain

        # Обработка коэффициента для x
        processing_vars(x)
        processing_vars(y)
        processing_vars(z)
        # if x_count != 0:
        #     if x_count == 1:
        #         ans += 'x'
        #     elif x_count == -1:
        #         ans += '-x'
        #     else:
        #         ans += f"{x_count}*x"
        #
        # # Обработка коэффициента для y
        # if y_count != 0:
        #     if len(ans) > 0 and y_count > 0:
        #         ans += '+'
        #     if y_count == 1:
        #         ans += 'y'
        #     elif y_count == -1:
        #         ans += '-y'
        #     else:
        #         ans += f"{y_count}*y"
        #
        # # Обработка коэффициента для z
        # if z_count != 0:
        #     if len(ans) > 0 and z_count > 0:
        #         ans += '+'
        #     if z_count == 1:
        #         ans += 'z'
        #     elif z_count == -1:
        #         ans += '-z'
        #     else:
        #         ans += f"{z_count}*z"

        # Добавление оставшейся константы
        if remain != 0:
            if len(ans) > 0 and remain > 0:
                ans += '+'
            ans += str(remain)

        # Если выражение пустое, выводим просто "0"
        return ans if ans else "0"

    except Exception as ex:
        return "Недопустимое выражение"


# Пример использования
print(calc(input("Введите выражение:")))
