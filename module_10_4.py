# Домашнее задание по теме
# "Очереди для обмена данными между потоками."

# Задача "Потоки гостей в кафе":

import threading
from random import randint
from queue import Queue

"""Создаётся объект стола через конструктор Table(номер_стола)
 У каждого стола есть два атрибута:
 number (номер стола) и guest (гость, сидящий за столом).
 Изначально guest равен None"""

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

"""Guest Наследуется от Thread, каждый гость будет работать в отдельном потоке.
 Конструктор принимает имя гостя (name) и сохраняет его в качестве атрибута.
 Метод run() - время приёма пищи гостем. Время случайно от 3 до 10 секунд."""

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        t_delay = randint(3, 10)
        threading.Event().wait(t_delay)

"""В конструкторе Cafe создаются атрибуты
 queue (очередь гостей) и tables (список столов в кафе)."""

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    """Метод guest_arrival() обрабатывает прибытие новых гостей.
    Если есть свободные столы, гости занимают их .
    Если все столы заняты, гости добавляются в очередь."""

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                free_table = next(table for table in self.tables if table.guest is None)
                free_table.guest = guest
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
                guest.start()

            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    """Метод discuss_guests() обслуживает гостей, 
    проверяет, закончился ли прием пищи, и если да,
    выводит сообщения об освобождении стола.
    Затем, если есть гости в очереди и свободные столы, 
    гости выходят из очереди и занимают столы."""

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

            if not self.queue.empty() and any(table.guest is None for table in self.tables):
                free_table = next(table for table in self.tables if table.guest is None)
                new_guest = self.queue.get()
                free_table.guest = new_guest
                print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {free_table.number}")
                new_guest.start()

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()


