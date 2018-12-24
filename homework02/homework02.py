from time import perf_counter


class callstat:
    """
    Декоратор, подсчитывающий количество вызовов и
    среднюю длительность вызова задекорированной функции.

    Пример использования:

    @callstat
    def add(a, b):
        return a + b

    >>> add.call_count
    0
    >>> add(1, 2)
    3
    >>> add.call_count
    1

    Подсказки по реализации: функторы, @property
    Для измерения времени выполнения - perf_counter, см. импорт.

    """
    def __init__(self, fn):
        self.fn = fn
        self.__count = 0
        self.__time = 0.0

    def __call__(self, *args, **kwargs):
        self.__count += 1
        start = perf_counter()
        res = self.fn(*args, **kwargs)
        self.__time += perf_counter() - start
        return res

    @property
    def call_count(self):
        return self.__count

    @property
    def avg_time(self):
        return self.__time / self.__count

