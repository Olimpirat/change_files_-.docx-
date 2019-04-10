"""программа должна открывать файлы в директории, находить в них значение и изменять его на указаное.
Порядок замен не важен.
При этом должен быть список директорий и возможность ввода новой.
Файлы ищются с указанным расширением .docx.
Для отладки использовать файлы MS .docx
запуск с консольным интерфейсом"""

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
from find_and_replace_text import find_and_replace_text

FLAG_YES = (1, "1", "YES", "yes", "Yes", "Y", "ДА", "Да", "да")
FLAG_NO = (0, 2, "2", "0", "NO", "no", "No", "N", "НЕТ", "Нет", "нет")

def choose_dir(): #функция окончательного выбора директрории, с возможностью "копать" в субдиректории.
    list_dir = {0:"другой путь (ввод)", 1:r"H:\работа\копия\Некрасовка съем", 2:r"H:\работа\копия\Документы",
                3:r'H:\работа\АВКПРОФ\Некрасовка съем', 4:r'H:\работа\копия\Некрасовка съем\Справки январь 2018\Справки январь 2018\ОДС-1\test'}
    print_for_chose(list_dir)
    try:
        choose_dir_inp = int(input("Выберите директорию: ")) #при вводе не цифр выдает ошибку, можно "поймать" ошибку но это еще не сделано
        if choose_dir_inp > len(list_dir)-1:
            print("Вы ввели неподходящее значение!")
            choose_dir()
        if choose_dir_inp == 0:
            choosen_dir = input("Введите директорию (например 'H:\работа\Документы': ")
        else:
            choosen_dir = list_dir[choose_dir_inp]
    except ValueError:
        print("Не допускается вводить другие значения")
        return choose_dir()

    while 1: #пока не введено значение 0 будет предлагаться выбрать поддиректорию. Выход после ввода
        dict_sub_dir = getting_dict_or_list(choosen_dir, files=False, folder=True)
        print_for_chose(dict_sub_dir)
        sub_dir_inp = input("Выбирите поддиректорию или введите 0 для потверждения директории '{0}' ".format(choosen_dir))
        if sub_dir_inp == '0' or sub_dir_inp == "":
            break
        choosen_dir += dict_sub_dir[int(sub_dir_inp)]
    return choosen_dir

def find_files(directory): #находим список файлов с поддиректорией, если стоит флаг. Основною директорию всегда можно подставить чтобы обратиться к файлу.
    frozen_dir = directory
    files_list=[]
    flag_circus = True
    while flag_circus: #флаг зацикливания
        flag_subdir = input("Искать файлы в поддиректориях? (1-ДА, 2-НЕТ) ")
        if flag_subdir in FLAG_NO:
            files_list.extend(get_list_files_in_folder(directory, frozen_dir=frozen_dir)) #добавляем список файлов в директории в общий список файлов
            flag_circus = False
        elif flag_subdir in FLAG_YES:
            files_list.extend((recruiting_list(directory, list_for_extend=files_list))) #получаем длинный список всех файлов включая поддиректории
            flag_circus = False
        else:
            print("Вы ввели что-то неправильно, попробуйте еще раз")
            flag_circus = True
    return files_list

def get_list_files_in_folder(directory, frozen_dir=''): #получения списка файлов в одной папке, подставляя frozen_dir спереди имени файла.
    files_list=[]
    for file in getting_dict_or_list(directory, folder=False, type_return='list'):  #тут получаем окончательный путь к файлу, типа string. 'H:\\работа\\копия\\Некрасовка съем\\Некрасовка Адреса 2018год.xlsx'
        if not "~$ " in file:  #проверка на временные файлы, временные файлы надо убрать
            files_list.append(frozen_dir + file)
    return files_list

def print_for_chose(dict_dir): #простенькая функция для вывода списка для интерактивного выбора варианта
    for path in dict_dir.items():
        print(str(path[0]) + " -- " + path[1])

def recruiting_list(directory, list_for_extend=[]): #list_for_extend это список для добавления в него, по умолчанию новый список. Функция возвращает список файлов в поддиректориях
    list_directory = []
    for root, dirs, files in os.walk(directory):
        list_directory.append(root)
    #print(list_directory)
    for subdirect in list_directory:    #обходим все директории и получаем из них файлы.
        #print(subdirect)
        list_for_extend.extend(get_list_files_in_folder(subdirect, frozen_dir=subdirect))
    return list_for_extend


def file_name_check(objs, end_file = "ALL"): #функция проверяет есть ли в списке objs файлы с заданным окончанием и возвращает новый список с отсортированными файлами
    number_of_files = 0 #чтобы прописать сколько файлов найдено
    if end_file == "ALL":
        number_of_files = len(objs)
        print("Найдено {0} файлов".format(number_of_files))
        return objs
    else:
        objs_sort = []
        for obj in objs:
            obj = str(obj)
            if end_file == obj[-len(end_file):]:
                objs_sort.append(obj)
                number_of_files += 1
        if objs_sort != []:
            print("Найдено {0} файлов".format(number_of_files))
            return objs_sort
        else:
            sys.exit("Подходящих файлов не найдено.") #завершение программы когда не найдено файлов

def getting_dict_or_list(directory, files=True, folder=True, type_return='dict'): #получение пронумерованного словаря или списка файлов и директорий по флагам
    from pathlib import Path
    p = Path(directory)
    finish_list = []
    if folder:
        folder_list = list(x for x in p.iterdir() if x.is_dir())
    if files:
        files_list = list(x for x in p.iterdir() if not x.is_dir())
    if files and folder:
        finish_list = folder_list + files_list
    elif files:
        finish_list = files_list
    elif folder:
        finish_list = folder_list
    else:
        print("нужно выбрать что искать, файлы или папки")
    key = 0
    if type_return == "list" or type_return == 'lst':  #вывод словаря и списка специально по форме \\имя. чтобы всегда можно было подставить основной путь
        list_return = []
        for x in finish_list:
            x = str(x)
            if key == 0:
                number_cut = x.rfind("\\")
                key += 1
            x = x[number_cut:]
            list_return.append(x)
        return (list_return)

    dict_finish = {}
    for x in finish_list:
        x = str(x)
        if key == 0:
            number_cut = x.rfind("\\")
        x = x[number_cut:]
        key += 1
        dict_finish[key] = x
    return dict_finish

"""ДАЛЕЕ ДОЛЖНЫ СОЗДАТЬ СЛОВАРЬ, КЛЮЧ=ИСКОМЫЙ ТЕКСТ, ЗНАЧЕНИЕ=ЗАМЕНЯЕМЫЙ"""

def get_dict(template=None): #создать словарь, ключ=искомый текст, значение=заменяемый. template это шаблон, который надо как то сохранять, чтобы их использовать (ПОКА НЕ РЕАЛИЗОВАНО)
    dict_find_refind = {}
    flag = 1 #флаг сколько надо искать значений под замену
    while flag:
        find_text = get_find_text(dict_find_refind)

        rfind_text = input("введите новый текст: ")
        dict_find_refind[find_text] = rfind_text
        more = input("Добавить еще значение? 1-ДА, 2-НЕТ ")
        if more in FLAG_NO:
            flag = 0

    print_dict(dict_find_refind)
    if input("Все верно? 1-ДА, 2-НЕТ ") in FLAG_NO:
        dictionary_error_handler(dict_find_refind)

    return dict_find_refind

def get_find_text(dict_find_refind): #Получения строки с искомым текстом для замены без ошибок (повторов)
    find_text = input("введите искомый текст: ")
    if not find_text in dict_find_refind.keys():  # Проверка значений чтобы небыло одинаковых замен
        return find_text
    else:
        print("Одинаковый текст для замены указан два раза! Введите другой искомый текст")
        get_find_text(dict_find_refind)

def print_dict(dict_print): #вывести словарь в удобочитаемом виде
    for x, y in dict_print.items():
        print("{0} {1} {2}".format(x, u'\u2192' , y))

def dictionary_error_handler(dict_with_error): #Обработчик ошибок в словаре поиск-замена
    print("1 - проблема в искомом тексте \n2 - проблема в заменяемом тексте")
    mistake_from = input("Выберете в чем проблема: ")
    if int(mistake_from) == 2: #предполагаем, что если пользователь введет чушь, то завершится fatal error
        dict_with_error = handler_error_2(dict_with_error)
    elif int(mistake_from) == 1: #предполагаем, что если пользователь введет чушь, то завершится fatal error
        dict_with_error = handler_error_1(dict_with_error)
    print_dict(dict_with_error)
    if input("Все исправлено? 1-ДА, 2-НЕТ ") in FLAG_NO:
        return dictionary_error_handler(dict_with_error)

def handler_error_1(dict_with_error):  #обработчик ошибки 1, проблема в ключе
    mistake = input("введите неправильный искомый текст: ")
    if dict_with_error.get(mistake) == None:
        print("Искомое значение '{0}' не обнаружено!".format(mistake))
        return handler_error_1(dict_with_error)
    else:
        mistake_corrected = input("введите новое значение искомого текста: ")
        dict_with_error[mistake_corrected] = dict_with_error.pop(mistake)
    return dict_with_error

def handler_error_2(dict_with_error): #обработчик ошибки 2, проблема в значении
    mistake = input("введите искомый текст, у которого указана неправильная замена: ")
    if dict_with_error.get(mistake) == None:
        print("Искомое значение '{0}' не обнаружено!".format(mistake))
        return handler_error_2(dict_with_error)
    else:
        dict_with_error[mistake] = input("введите новое значение заменямого текста: ")
    return dict_with_error

if __name__ == "__main__":
    path_all = file_name_check(find_files(choose_dir()), end_file='.docx') #список файлов
    dict_test = get_dict()
    list_of_changes = list()  # создаем список, куда будем помещать кортежи с уже измененными данными
    for path in path_all: #path_all это все пути к файлам
        find_and_replace_text(path, dict_test, list_of_changes, copy=True)