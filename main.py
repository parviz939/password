import json # сохранить данные
import string # получение Констант все заглавной буквы Все буквы
import random #Для случайного выбора пароля

symbols = string.ascii_letters + string.digits + "!_?" #symbols Все символы При генерации пароля
g = "aivoe" #Все гласный
s = "bjhfdkoqmnxcgewutyls" # Все согласные буквы


# print(random.choice(sumbols))
#Сохранять все списки из словари
def load_db(filename):
    with open(filename) as file:
        db = json.load(file)

    return db


def save_db(filename, db):
    with open(filename, "w") as file:
        json.dump(db, file, indent=2)

#Добавляет пароль Спрашиваю с клавиатуры
def add_pass(db):
    site = input("Введите название сайта: ")
    login = input("Введите Логен: ")
    password = input("Введите пароль: ")

    db.append(
        {
            "login": login,
            "password": password,
            "site": site
        }
    )

#Взаимодействовать с пользователю
def change(subject, prev):
    t = input(f"Видите {subject} ({prev}):")
    if t == "":
        return prev
    else:
        return t

#Изменять запись сы пароль
def change_pass(info):
    info["site"] = change("Название сайта", info["site"])
    info["login"] = change("логин", info["login"])
    info["password"] = change("пароль", info["password"])

#Берет две строки и проверяйтесь есть ли общее символ С помощью множества
def compare(s1, s2):
    s1_set = set(s1)
    s2_set = set(s2)

    inter = s1_set.intersection(s2_set)

    return len(inter) > 0


#    for sym1 in s1:
#        for sym2 in s2:
#            if sym1 == sym2:
#                return True
#генирировыет случайная пароль
def gen_pass(L):
    while True:
        res = ""
        for i in range(L):
            res += random.choice(sumbols)

        bools = [
            compare(res, string.ascii_lowercase),
            compare(res, string.ascii_uppercase),
            compare(res, string.digits),
            compare(res, "!_?"),
            res[0] not in string.ascii_uppercase
        ]

        if all(bools):
            return res

#Создает пароль который легко Запомнить
def gen_easy_pass(L):
    res = ""
    for i in range(L - 3):
        if i % 2 == 0:
            res += random.choice(s)
        else:
            res += random.choice(g)

    for i in range(3):
        res += random.choice(string.digits)

    return res

#Добавлять пароль для какого-то сайта  При этом генирировыет Пароль самостоятельно
def add_and_gen(db):
    site = input("Введите название сайта: ")
    login = input("Введите Логен: ")
    L = int(input("Видите длину парола: "))
    t = input("Генерировать сложный пароль (y/n)?")
    if "y" in t.lower():
        password = gen_pass(L)
    else:
        password = gen_easy_pass(L)

    db.append(
        {
            "login": login,
            "password": password,
            "site": site
        }
    )
    
    
#Красиво вводит пароль с полоской
def show(info, num):
    print(f"{num:3} | {info['site']:15} | {info['login']:15} | {info['password']:15}")

#Вводит пароль привязана к сайта
def seaech(db):
    site = input("Введите название сайта: ")
    results = []
    for info in db:
        if site in info["site"]:
            results.append(info)

        for num, info in enumerate(results):
            show(info, num)

    m = pass_mode()
    if m == "2":
        num = int(input("Введите номер:"))
        db.remove(results[num])
    elif m == "3":
        num = int(input("Введите номер:"))
        info = results[num]
        change_pass(info)

#Спрашивает что делать
def pass_mode():
    print("Список действий:")
    print("1. Выйти из поиска")
    print("2. Удалить пароль")
    print("3. Изменить пароль")
    m = input("Введите номер Действия: ")
    return m

#Ищет Слабые места
def check(db):
    cnt = {}
    for info in db:
        if info["password"] in cnt:
            cnt[info["password"]] += 1
        else:
            cnt[info["password"]] = 1

    for password, num in cnt.items():
        if num > 1:
            print(f'Пароль "{password}" Не безопасно! Он используется на сайтах:')
            for info in db:
                if info["password"] == password:
                    print(f"сайт: {info['site']:15}, логин:{info['login']:15}")



#Повышает о режимах
def mode():
    print("Список режимов: ")
    print("1. Добавить пароль ")
    print("2. Сгенерировать пароль")
#    print("3. Изменить пароль")
#    print("4. Удалить пароль")
    print("3.Найти пароль")
    print("4. Найти уязвимости")
    print("5. Выйти из программы ")
    m = input("Введите номер режима: ")
    return m


#Основной цикл проверки режим Какой режим выбрать пользователь
def loop(filename):
    db = load_db(filename)
    while True:
        m = mode()
        if m == "1":
            add_pass(db)
        elif m == "2":
            add_and_gen(db)
        elif m == "3":
            seaech(db)
        elif m == "4":
            check(db)
        elif m == "5":
            break
        else:
            print("Нет такого режима!")

    save_db(filename, db)

loop("user.json")



db = load_db("user,json")

check(db)
# add_pass(db)
# change_pass(db[0])
# db = load_db("user.json")
# print(db)
