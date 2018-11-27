# Задание 1. Встроенные типы данных, операторы, функции и генераторы
#
# Напишите реализации объявленных ниже функций. Для проверки
# корректности реализации ваших функций, запустите тесты:
#
# pytest test_homework01.py
#
# Если написанный вами код не содержит синтаксических ошибок,
# вы увидите результаты тестов ваших решений.

def fac(n):
    """
    Факториал

    Факториал числа N - произведение всех целых чисел от 1 до N
    включительно. Например, факториал числа 5 - произведение
    чисел 1, 2, 3, 4, 5.

    Функция должна вернуть факториал аргумента, числа n.
    """
    assert n >= 1
    result = 1
    while n:
        result *= n
        n -= 1
    return result


def gcd(a, b):
    """
    Наибольший общий делитель (НОД) для двух целых чисел.

    Предполагаем, что оба аргумента - положительные числа
    Один из самых простых способов вычесления НОД - метод Эвклида,
    согласно которому

    1. НОД(a, 0) = a
    2. НОД(a, b) = НОД(b, a mod b)

    (mod - операция взятия остатка от деления, в python - оператор '%')
    """
    if b == 0:
        return a
    return gcd(b, a % b)

def fib():
    """
    Генератор для ряда Фибоначчи

    Вам необходимо сгенерировать бесконечный ряд чисел Фибоначчи,
    в котором каждый последующий элемент ряда является суммой двух
    предыдущих. Начало последовательности: 1, 1, 2, 3, 5, 8, 13, ..

    Подсказка по реализации: для бесконечного цикла используйте идиому

    while True:
      ..

    """
    result = [1, 1]
    while True:
        result.append(result[-1] + result[-2])
        break
    return result

def flatten(seq):
    """
    Функция, преобразующая вложенные последовательности любого уровня
    вложенности в плоские, одноуровневые.

    flatten([])
    []
    flatten([1, 2])
    [1, 2]
    flatten([1, [2, [3]]])
    [1, 2, 3]
    flatten([(1, 2), (3, 4)])
    [1, 2, 3, 4]
    """
    result = []
    for item in seq:
        if type(item) not in (list, set, frozenset, tuple):
            result.append(item)
        else:
            result += flatten(item)
    return result

