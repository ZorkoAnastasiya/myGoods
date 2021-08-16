import csv
import pathlib
from enum import Enum


class Key(str, Enum):
    name = "Наименование товара"
    price = "Цена"
    quantity = "Количество"


fieldnames = [Key.name, Key.price, Key.quantity]


def csv_writer(filename: str, list_args: list):
    """Создает или обновляет csv_file для учета товаров."""
    list_goods = [{Key.name: list_args[0], Key.price: list_args[1], Key.quantity: list_args[2]}]
    file_path = pathlib.Path(filename)
    if file_path.is_file():
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(list_goods)
    else:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(list_goods)
    return {"Сообщение": "Данные обновлены", "Имя файла": filename}


def csv_reader(filename: str):
    """Читает весь файл и выводит его на экран."""
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    return {"Данные": reader}
    

def deletion_goods(filename: str, name: str):
    """Удаляет строку из файла по ключу 'Наименование товара'."""
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        counter = 0
        for row in reader:
            if row[Key.name] != name:
                counter += 1
            else:
                del reader[counter]
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)
    return {"Сообщение": "Данные удалены", "Удаленное наименование": name}


def sum_goods(filename: str) -> int:
    """Возвращает сумму стоимости всех товаров."""
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        sum_list = [float(row[Key.price]) * float(row[Key.quantity]) for row in reader]
    return sum(sum_list)


def max_price(filename: str):
    """Осуществляет поиск самых дорогих товаров в файле."""
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        max_num = 0
        for row in reader:
            if float(row[Key.price]) >= max_num:
                max_num = float(row[Key.price])
        list_goods = {row[Key.name]: max_num for row in reader if float(row[Key.price]) == max_num}
    return {
        "Сообщение": "Товары с максимальной ценой",
        "Данные": list_goods
    }


def min_price(filename: str):
    """Осуществляет поиск самых дешевых товаров в файле."""
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        min_num = float(reader[1][Key.price])
        for row in reader:
            if float(row[Key.price]) <= min_num:
                min_num = float(row[Key.price])
        list_goods = {row[Key.name]: min_num for row in reader if float(row[Key.price]) == min_num}
    return {
        "Сообщение": "Товары с минимальной ценой",
        "Данные": list_goods
    }


def change_quantity(filename: str, name: str, quantity: int, effect: str):
    """Изменяет количество товара по заданному наименованию"""
    result = 0
    answer = 0
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            if row[Key.name] == name:
                result = int(row[Key.quantity])
                if effect == '+':
                    result += quantity
                    row[Key.quantity] = result
                    answer = 1
                else:
                    result -= quantity
                    row[Key.quantity] = result
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)
    message_add = {"Данные": {Key.name: name, "Увеличено на": quantity, Key.quantity: result}}
    message_del = {"Данные": {Key.name: name, "Уменьшено на": quantity, Key.quantity: result}}
    return message_add if answer else message_del
