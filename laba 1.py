import math


def calculator(items):
    while '(' in items:
        start = 0

        for i in range(len(items)):
            if items[i] == '(':
                start = i
            elif items[i] == ')':
                end = i
                break
        else:
            print('Не хватает закрывающих скобок')
            return None

        result = calculator(items[start + 1:end])

        if result is None:
            return None

        if start > 0 and items[start - 1] == 'exp':
            try:
                result = math.exp(result)
            except OverflowError:
                print('Слишком большое значение для exp')
                return None
            start -= 1

        items[start:end + 1] = [result]

    if ')' in items:
        print('Лишняя закрывающая скобка')
        return None

    for i in range(len(items)):
        if isinstance(items[i], str):
            try:
                items[i] = int(items[i])
            except ValueError:
                try:
                    items[i] = float(items[i])
                except ValueError:
                    if items[i] not in ('+', '-', '*', '/', '^'):
                        print('Неизвестный элемент: ' + items[i])
                        return None

    ready = []
    i = 0
    num_needed = True

    while i < len(items):
        if num_needed:
            sign = 1

            while i < len(items) and items[i] in ('+', '-'):
                if items[i] == '-':
                    sign *= -1
                i += 1

            if i >= len(items) or not isinstance(items[i], (int, float)):
                print('Ожидалось число')
                return None

            ready.append(sign * items[i])
        else:
            if items[i] not in ('+', '-', '*', '/', '^'):
                print('Ожидался оператор')
                return None

            ready.append(items[i])

        num_needed = not num_needed
        i += 1

    if num_needed:
        print('Выражение пустое или заканчивается оператором')
        return None

    items = ready

    for operators in ('*/', '+-', '^'):
        i = 1

        while i < len(items):
            operator = items[i]

            if operator not in operators:
                i += 2
                continue

            a = items[i - 1]
            b = items[i + 1]

            if operator == '*':
                result = a * b
            elif operator == '/':
                if b == 0:
                    print('На ноль делить нельзя')
                    return None
                result = a / b
            elif operator == '+':
                result = a + b
            elif operator == '-':
                result = a - b
            elif operator == '^':
                if not math.isfinite(a) or not math.isfinite(b):
                    print('Для ^ нужны конечные целые числа')
                    return None

                if a == int(a) and b == int(b):
                    result = int(a) ^ int(b)
                else:
                    print('Для ^ нужны целые числа')
                    return None

            items[i - 1:i + 2] = [result]

    return items[0]


while True:
    equation = input('Введите выражение: ').replace(',', '.')

    if equation == 'exit':
        print('Завершение...')
        break

    if '_' in equation:
        print('Подчёркивания нельзя использовать')
        continue

    for sign in '+-*/()^':
        equation = equation.replace(sign, f' {sign} ')

    items = equation.split()
    answer = calculator(items)

    if answer is not None:
        print('Ответ:', answer)