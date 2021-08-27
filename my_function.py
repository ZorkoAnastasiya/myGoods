import csv
import os
import pathlib
from enum import Enum
from fastapi import Request


class Key(str, Enum):
    user = "Пользователь"
    name = "Наименование товара"
    price = "Цена"
    quantity = "Количество"
    

fieldnames = [
    Key.user,
    Key.name,
    Key.price,
    Key.quantity
]


def get_random_name() -> hex:
    """Генерирует случайное число."""

    return os.urandom(16).hex()


def get_user(request: Request) -> str:
    """Возвращает значение 'user'  из 'cookies'."""

    return request.cookies.get("user")


def csv_writer(filename: str, list_args: list, user: str) -> dict:
    """Создает или обновляет csv_file для учета товаров."""

    list_goods = [
        {
            Key.user: user,
            Key.name: list_args[0],
            Key.price: list_args[1],
            Key.quantity: list_args[2]
        }
    ]

    file_path = pathlib.Path(filename)

    if file_path.is_file():
        with open(filename, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerows(list_goods)
    else:
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(list_goods)

    return {
        "Сообщение": "Данные обновлены",
        "Для пользователя": user,
        "Имя файла": filename
    }


def csv_reader(filename: str, user: str) -> dict:
    """Читает весь файл и выводит его на экран."""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        reader_user = [
            {
                Key.name: row[Key.name],
                Key.price: row[Key.price],
                Key.quantity: row[Key.quantity]
            }
            for row in reader
            if row[Key.user] == user
        ]

    return {
        "Для пользователя": user,
        "Данные": reader_user
    }
    

def deletion_goods(filename: str, name: str, user: str) -> dict:
    """Удаляет строку из файла по ключу 'Наименование товара'."""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        counter = 0
        for row in reader:
            if row[Key.user] != user:
                counter += 1
            else:
                if row[Key.name] != name:
                    counter += 1
                else:
                    del reader[counter]

        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)

    return {
        "Сообщение": "Данные удалены",
        "Для пользователя": user,
        "Удаленное наименование": name
    }


def sum_goods(filename: str, user: str) -> dict:
    """Возвращает сумму стоимости всех товаров."""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        sum_list = [
            float(row[Key.price]) * float(row[Key.quantity])
            for row in reader if row[Key.user] == user
        ]
        result = sum(sum_list)

    return {
        "Для пользователя": user,
        "Сумма стоимости товаров": result
    }


def max_price(filename: str, user: str) -> dict:
    """Осуществляет поиск самых дорогих товаров в файле."""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        max_num = 0
        for row in reader:
            if row[Key.user] == user and float(row[Key.price]) >= max_num:
                max_num = float(row[Key.price])

        list_goods = {
            row[Key.name]: max_num
            for row in reader
            if row[Key.user] == user and float(row[Key.price]) == max_num
        }

    return {
        "Сообщение": "Товары с максимальной ценой",
        "Для пользователя": user,
        "Данные": list_goods
    }


def min_price(filename: str, user: str) -> dict:
    """Осуществляет поиск самых дешевых товаров в файле."""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        min_num = float(reader[1][Key.price])
        for row in reader:
            if row[Key.user] == user and float(row[Key.price]) <= min_num:
                min_num = float(row[Key.price])

        list_goods = {
            row[Key.name]: min_num
            for row in reader
            if row[Key.user] == user and float(row[Key.price]) == min_num
        }

    return {
        "Сообщение": "Товары с минимальной ценой",
        "Для пользователя": user,
        "Данные": list_goods
    }


def change_quantity(
        filename: str,
        name: str,
        quantity: int,
        effect: str,
        user: str
) -> dict:
    """Изменяет количество товара по заданному наименованию"""

    with open(filename, 'r', newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))

        for row in reader:
            answer = 0
            if row[Key.user] == user and row[Key.name] == name:
                result = int(row[Key.quantity])
                if effect == '+':
                    result += quantity
                    row[Key.quantity] = result
                    answer = 1
                else:
                    result -= quantity
                    row[Key.quantity] = result

                with open(filename, 'w', newline = '') as file:
                    writer = csv.DictWriter(file, fieldnames = fieldnames)
                    writer.writeheader()
                    writer.writerows(reader)

                message_add = {
                    "Для пользователя": user,
                    "Данные": {
                        Key.name: name,
                        "Увеличено на": quantity,
                        Key.quantity: result
                    }
                }

                message_del = {
                    "Для пользователя": user,
                    "Данные": {
                        Key.name: name,
                        "Уменьшено на": quantity,
                        Key.quantity: result
                    }
                }

                return message_add if answer else message_del

        else:
            return {
                "Для пользователя": user,
                Key.name: name,
                "Сообщение": "Данные не найдены"
            }
