import re

allowed_chars = r'^[0-9xyz\+\-\*\(\)\s]+$'
ans = ''


def processing_vars(count: int, var: str) -> str:
    global ans
    if count != 0:
        if len(ans) > 0 and count > 0:
            ans += '+'
        if count == 1:
            ans += var
        elif count == -1:
            ans += '-'+var
        else:
            ans += f"{count}*{var}"
    return ans


def calc(inp):
    global ans
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

        x, y, z = 1, 1, 0
        xy_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain - x_count - y_count

        x, y, z = 1, 0, 1
        xz_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain - x_count - z_count

        x, y, z = 0, 1, 1
        yz_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain - y_count - z_count

        x, y, z = 1, 1, 1
        xyz_count = eval(inp, {'x': x, 'y': y, 'z': z}) - remain - x_count - y_count - z_count - xy_count - yz_count - xz_count

        # Обработка коэффициента для x
        processing_vars(x_count, 'x')
        processing_vars(y_count, 'y')
        processing_vars(z_count, 'z')
        processing_vars(xy_count, 'xy')
        processing_vars(xz_count, 'xz')
        processing_vars(yz_count, 'yz')
        processing_vars(xyz_count, 'xyz')

        # Добавление оставшейся константы
        if remain != 0:
            if len(ans) > 0 and remain > 0:
                ans += '+'
            ans += str(remain)

        # Если выражение пустое, выводим просто "0"
        return ans if ans else "0"

    except Exception as ex:
        return "Недопустимое выражение"

def main():
    print(calc(input("Введите выражение:")))
# Пример использования
if __name__ == "__main__":
    main()
