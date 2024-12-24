from threading import Thread


from queue import Queue                 # модуля queue
from random import randint, random      # randint из модуля random
import time                             # модуль time



class Table:
    def __init__(self, number):
        self.number = number                                               # номер стола
        self.guest = None                                                  # гость



class Guest(Thread):
    def __init__(self, name):
        super().__init__()                                                  # наследование
        self.name = name                                                    # имя гостя
    def run(self):
        random_result = randint(3, 10)                               # ожидание случайным образом от 3 до 10 секунд
        time.sleep(random_result)

class Cafe():
    def __init__(self, *tables):
        super().__init__()
        self.queue = Queue()                                                # очередь
        self.tables = list(tables)  # Коллекция столов


    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")         # в случае свободного стола
                    table.guest.start()                                                 # запуск потока
                    break                                                               # прерывание цикла
            else:                                                                       # Если свободных столов для посадки не осталось
                self.queue.put(guest)                                                   # добавление в поток
                print(f"{guest.name} в очереди")


    def discuss_guests(self):                                                           # процесс обслуживания гостей
        while not self.queue.empty() or any(table.guest for table in self.tables):      # пока очередь не пустая
            for table in self.tables:                                                   # (метод empty) или хотя бы один стол занят
                if not table.guest is None and table.guest.is_alive:                    # за столом есть гость и закончил приём пищи
                    table.guest.join()
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    table.guest = None                                                  # стол освободился
                    print(f'Стол номер {table.number} свободен')
                elif not self.queue.empty() and table.guest is None:                    # очередь не пуста и стол освободился
                    table.guest = self.queue.get()                                      # присваивается гость взятый из очереди
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.start()                                                 # запуск потока




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








