"""программа должна открывать файлы .docx в директории, находить в них значение и изменять его на указаное.
Порядок замен не важен.
Файлы ищются с указанным расширением .docx.
запуск с графическим интерфейсом QT5"""

#РЕАЛИЗОВАТЬ:
# ДОПИСАТЬ КНОПКУ "ДОБАВИТЬ ПОЛЯ". КАК СОЗДАТЬ ГЕНЕРАТОР СТРОК ПО ВВОДОМОМУ ТЕКСТУ ? Попробовать: создать основное поле, в нем создавать поле-строку куда поместить все виджеты строки, далее отобразить поле-строку. Пока не ясно как в этом случае получать значения из этих полей...

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, time
from The_replacement_text_is_repeated import *
from close_file import *
from GUI import *
from progress_bar import *
from PyQt5 import QtCore, QtGui, QtWidgets
from find_and_replace_text import find_and_replace_text

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_find_and_replace_docx()
        self.ui.setupUi(self)
        self.statusBar().showMessage('Ready')

        #создаем список-матрицу далее С-М
        self.rows = 6
        self.cols = 2
        self.lines = [[None for i in range(self.cols)] for j in range(self.rows)] #создаем список с пустыми элементами
        #ЛОГИКУ НИЖЕ НУЖНО ПЕРЕПИСАТЬ В GUI.PY ДЛЯ ТОГО ЧТОБЫ СОЗДАТЬ ГЕНЕРАТОР И ПЕРЕПИСАТЬ ССЫЛКИ ЧЕРЕЗ self.ui.*** ЛИБО ВЕСЬ ГЕНЕРАТОР ПРОПИСАТЬ ТУТ
        #добавляем в С-М ссылки на объекты (которые созданы по умолчанию)
        self.lines[0][0] = self.ui.lineEdit_search_text_1
        self.lines[0][1] = self.ui.lineEdit_replaced_by_1
        self.lines[1][0] = self.ui.lineEdit_search_text_2
        self.lines[1][1] = self.ui.lineEdit_replaced_by_2
        self.lines[2][0] = self.ui.lineEdit_search_text_3
        self.lines[2][1] = self.ui.lineEdit_replaced_by_3
        self.lines[3][0] = self.ui.lineEdit_search_text_4
        self.lines[3][1] = self.ui.lineEdit_replaced_by_4
        self.lines[4][0] = self.ui.lineEdit_search_text_5
        self.lines[4][1] = self.ui.lineEdit_replaced_by_5
        self.lines[5][0] = self.ui.lineEdit_search_text_6
        self.lines[5][1] = self.ui.lineEdit_replaced_by_6


        self.ui.checkBox_subdir.setChecked(True)  # Флаг по умолчанию активный
        self.flag_copy = 0 #Флаг копии по умолчанию отключен и соответственно значение равно 0
        self.files_list_sort = list()  # создаем пустой список чтобы не выдавал ошибку если просто нажать конверт

        self.ui.pushButton_browse.clicked.connect(self.BrowseDirectory) #Здесь прописываем событие нажатия на кнопку Browse
        self.ui.lineEdit_dir.textChanged.connect(self.onChanged_dir) #событие при изменение полоски с директрорией
        self.ui.checkBox_subdir.stateChanged.connect(self.onChanged_dir) #изменения флага субдиректорий
        self.ui.checkBox_changes.stateChanged.connect(self.copy_flag)  # изменения флага субдиректорий

        self.ui.pushButton_convert.clicked.connect(self.ConvertBotton) #Здесь прописываем событие нажатия на кнопку Convert

        self.ui.about.triggered.connect(self.AboutBotton)  #Действие при начанитии About в меню баре

    def BrowseDirectory(self): #открывает окно выбора директории и работает с ним
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "выберите папку").replace("/","\\") #записывает выбранный путь в переменную, получаем str и изменяем слеши
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.ui.lineEdit_dir.setText(directory) #прописать путь в строку ввода

    def onChanged_dir(self): #изменения списка файлов и вывод информации об этом
        #print(self.ui.checkBox_subdir.checkState())
        frozen_dir = self.ui.lineEdit_dir.text()
        #files_list = []
        self.mythread = MyThread_onChangel_dir(flag=self.ui.checkBox_subdir.checkState(), dir=frozen_dir)  # Создаем экземпляр класса потока для поиска файлов
        self.mythread.finished.connect(self.on_finished_thread_dir) #выполняем действие когда  завершится поток
        self.mythread.mysignal.connect(self.on_change_dir, QtCore.Qt.QueuedConnection) #сигнал для передачи в основной поток данных
        if len(frozen_dir)<3: #если введено менее 3х символов - ничего не делать
            return True
        if os.path.isdir(frozen_dir):
            self.mythread.start()  # Запускаем поток
        else:
            pass

    def on_finished_thread_dir(self): #выполняем действие когда завершится поток
        self.ui.label_count_files.setText("Found {0} files".format(self.number_of_files))

    def on_change_dir(self, attr_tuple): #передача в основной поток данных
        self.files_list_sort, self.number_of_files = attr_tuple
        #print("окончательный список ", self.files_list_sort)

    def copy_flag(self, state): #изменение флага создания копий
        self.flag_copy = state # 0 выключен флаг, 2 включен

    def ConvertBotton(self): #создание словаря для замен, и выполнить изменения
        try:
            if self.mythread.isRunning(): #проверка завершился ли поток поиска файлов
                #print("поток не завершился")
                self.error_The_replacement_text_is_repeated = The_replacement_text_is_repeated(
                    "File search not completed \n Please wait until the file search is complete.")
                self.error_The_replacement_text_is_repeated.show()
                return True
            if self.number_of_files == 0: #если подходящих файлов не найдено
                self.error_The_replacement_text_is_repeated = The_replacement_text_is_repeated(
                    "No matching files found \n Please check the specified directory.")
                self.error_The_replacement_text_is_repeated.show()
                return True
        except AttributeError as e: #если список файлов не производился (поток "сборки" списка файлов), то ничего не делать
            return True

        self.ui.pushButton_convert.setEnabled(False)
        #создаем словарь замен
        self.dict_find_refind = dict()  # создаем пустой словарь, ключ=искомый текст, значение=заменяемый
        for row in range(self.rows):
            if self.lines[row][0].text(): #если искомое текст заполнен, то выполнять иначе закончить цикл
                if not self.lines[row][0].text() in self.dict_find_refind.keys():  # Проверка значений чтобы небыло одинаковых замен
                    self.dict_find_refind[self.lines[row][0].text()]=self.lines[row][1].text()
                else:
                    self.error_The_replacement_text_is_repeated = The_replacement_text_is_repeated("The replacement text is repeated: \n {}".format(self.lines[row][0].text()))
                    self.error_The_replacement_text_is_repeated.show()
                    self.ui.pushButton_convert.setEnabled(True)
                    return

        #print(self.dict_find_refind) #словарь замен
        #print(self.files_list_sort) #список найденных файлов для замены
        #print(self.flag_copy) #состояние флага, делать ли копии или нет

        files_num = 0 #кол-во готовых файлов

        self.on_signal_start_return(files_num_self=files_num)
        #print("finish")

    def on_finished_thread_convert(self): #при завершении потока до 100% разблочить кнопку convert
        if self.ui.progressBar.value() == 100:
            self.ui.pushButton_convert.setEnabled(True)

    def on_progBar(self, attr_int): #функция изменения прогресс бара
        self.ui.progressBar.setValue(100 / self.number_of_files * attr_int)

    def on_errorOpenFile(self, attr_int): #обработка ошибки "открытого файла"
        self.files_num = attr_int
        path = self.files_list_sort[attr_int]
        #print("ошибка в файле: ", path)
        self.close_file_window = close_file(str(path), parent=self)
        self.close_file_window.show()
        self.close_file_window.mysignal_close_file.connect(self.on_signal_start_return)

    def on_errorBrokenFile(self, attr_int): #обработка ошибки битого файла
        path = self.files_list_sort[attr_int]
        self.error_The_replacement_text_is_repeated = The_replacement_text_is_repeated(
            "File: \n {} \n cannot be opened damaged or in a different format with the end of .docx, but it is not. \n file skipped".format(path))
        self.error_The_replacement_text_is_repeated.show()
        if (attr_int+1)==self.number_of_files:
            self.ui.progressBar.setValue(100)  # изменяем прогресс бар на последнем файле под 100%. Пропуск последнего битого файла
        else: #если файл не последний, то выводим сообщение какой файл пропушен и продолжаем работу
            self.files_num = attr_int+1
            self.on_signal_start_return(files_num_self=self.files_num)

    def on_signal_start_return(self, files_num_self): #через ****, но работает. Сигнал начала/продолжения основной работы
        self.mythread_convert = MyThread_convert(files_num_self, files_list=self.files_list_sort,
                                                 dict_find_refind=self.dict_find_refind,
                                                 flag_copy=self.flag_copy)
        self.mythread_convert.finished.connect(
            self.on_finished_thread_convert)  # выполняем действие когда  завершится поток
        self.mythread_convert.signal_progBar.connect(self.on_progBar,
                                                     QtCore.Qt.QueuedConnection)  # сигнал для передачи в основной поток данных
        self.mythread_convert.signal_errorOpenFile.connect(self.on_errorOpenFile,
                                                           QtCore.Qt.QueuedConnection)  # сигнал для передачи в основной поток данных сигнала о ошибки открытого файла
        self.mythread_convert.signal_errorBrokenFile.connect(self.on_errorBrokenFile,
                                                           QtCore.Qt.QueuedConnection)  # сигнал для передачи в основной поток данных сигнала о ошибки битого файла
        self.mythread_convert.start()  # Запускаем поток

    def AboutBotton(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()


class AboutWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("About the program")
        self.resize(500, 500) #размер окна
        self.horizontalLayout = QtWidgets.QHBoxLayout(self) #создаем слой, чтобы по нему растянуть виджет с текстом
        self.text_edit = QtWidgets.QTextBrowser(self)
        font = QtGui.QFont() #настроиваем шрифт
        font.setPointSize(12)
        self.text_edit.setFont(font)
        self.text_about = """  
<p>&nbsp;</p>
<p>Данная программа предназначена для поиска всех файлов, оканчивающихся на .docx (MS Word 2007+), в указанной директории и замена в них указанного текста. Работает только на Windows (тестирование проходило на 2х машинах Windows 10)</p>
<p>Если текст новый и заменяемый повторяются в разных частях исходного документа (01.01.2000&rarr;01.02.2000; 01.02.2000&rarr;01.03.2000), то порядок замены текста не важен. Повторная замена нового текста не производится.&nbsp;</p>
<p>Если установлен флаг&nbsp; &ldquo;Make changes to file copies&rdquo;, то создается в директории папка copy и туда помещаются исходные файлы.</p>
<p>Флаг "Search files in subdirectories" позволяет искать файлы не только в корневой директории, но и в поддиректориях.</p>
<p>Программа не закончена.</p>
<p>Не являюсь профессиональным программистом. Просьба присылать свои замечания и материалы как их исправить на почту <a href="mailto:Adorari@mail.ru">Adorari@mail.ru</a> или GitHub *****.</p>
<p>Требуется добавить функционал:</p>
<ul>
<li>Возможность установки более 6 пар текста</li>
<li>Возможность работы на различных ОС</li>
<li>Компиляция в исполняемый файл или как можно удобно переносить на другие машины. Через pyinstaller работала на Windows 10 (создавался на той же ОС) на машине без дополнительных программ. На Windows XP не запустился.</li>
<li>Оптимизация и исправление ошибок</li>
</ul>
<p>Программа написана на Python 3 + GUI PyQt5</p>
        """
        self.text_edit.setHtml(self.text_about) #засунуть подготовленный текст в виджет
        self.horizontalLayout.addWidget(self.text_edit) #установить виджет на слое и тем самым отобразить его.


class The_replacement_text_is_repeated(QtWidgets.QWidget): #класс с окном для вывода ошибки и кнопкой OK (используется в одинаковых поисках текста, незавершенном поиске файлов и битом файле
    def __init__(self, text, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.The_replacement_text_is_repeated = Ui_Dialog()
        width = len(text.split('\n')[-1])*6
        self.The_replacement_text_is_repeated.setupUi(self, width, 200)
        self.setWindowTitle('Window error')
        self.The_replacement_text_is_repeated.label.setText("{}".format(text))
        self.The_replacement_text_is_repeated.pushButton.clicked.connect(self.exit_)  # Здесь прописываем событие нажатия на кнопку OK
    def exit_(self):
        self.close()

class close_file(QtWidgets.QWidget): #класс с ошибкой об открытие файла
    mysignal_close_file = QtCore.pyqtSignal(bool)  # сигнал для передаче итоговых данных
    def __init__(self, text, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent, flags=QtCore.Qt.Dialog)
        self.close_file = close_file__()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        width = len(text)*6
        self.close_file.setupUi(self, width, 150)
        self.setWindowTitle('Window error')
        self.close_file.label_name_file.setText(text)
        self.close_file.pushButton.clicked.connect(self.exit_)  # Здесь прописываем событие нажатия на кнопку OK
    def exit_(self):
        self.mysignal_close_file.emit(True)
        self.close()

class MyThread_onChangel_dir(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(tuple) #сигнал для передаче итоговых данных
    def __init__(self, flag=False, dir=None, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.flag = flag
        self.frozen_dir = dir
        #поток инициализировался
    def run(self):
        #поток запустил выполнение
        files_list = []
        #print("файл лист: ", files_list)
        if self.flag:  # если флаг установлен
            #поток продолжил выполнение, флаг ON
            files_list.extend((recruiting_list(self.frozen_dir,
                                               list_for_extend=[])))  #получаем длинный список всех файлов включая поддиректории
        elif not self.flag:  # если флаг неустановлен
            #поток продолжил выполнение, флаг OFF
            files_list.extend(get_list_files_in_folder(self.frozen_dir,
                                                       self.frozen_dir))  #добавляем список файлов в директории в общий список файлов
        self.files_list_sort, self.number_of_files = file_name_check(files_list, end_file=".docx")
        self.mysignal.emit((self.files_list_sort, self.number_of_files))
        #поток завершился

class MyThread_convert(QtCore.QThread):
    signal_progBar = QtCore.pyqtSignal(int)  #сигнал для изменения прогресс бара
    signal_errorOpenFile = QtCore.pyqtSignal(int)  #сигнал для отработки открытого файла
    signal_errorBrokenFile = QtCore.pyqtSignal(int)  # сигнал для отработки открытого файла
    def __init__(self, num=0, files_list=None, dict_find_refind=None, flag_copy=False, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.flag_copy = flag_copy #получаем флаг необходимости создавать копии
        self.num=num #число откуда начать поиск и замену
        self.files_list = files_list #список файлов
        self.dict_find_refind = dict_find_refind #словарь с заменами
        #поток инициализировался
    def run(self):
        #поток запустил выполнение
        try:
            for path in self.files_list[self.num:]:  # files_list это все пути к файлам
                if not path:
                    return
                #print("path = ", path)
                #print("string 226 - ", self.num)
                #print("словарь замен - ", self.dict_find_refind)
                find_and_replace_text(path, self.dict_find_refind, copy=self.flag_copy)
                self.num += 1
                self.signal_progBar.emit(self.num) #изменяем прогресс бар
        except PermissionError: #ошибка открытого файла
            #ERROR!
            self.signal_errorOpenFile.emit(self.num)  #передаем сигнал о ошибки открытого файла
        except FileNotFoundError: #ошибка битого файла
            #ERROR!
            self.signal_errorBrokenFile.emit(self.num)




"""Ниже распалагаются функции для работы логики программы"""
def recruiting_list(directory, list_for_extend=[]):  # list_for_extend это список для добавления в него, по умолчанию новый список. Функция возвращает список файлов в поддиректориях
    list_directory = []
    for root, dirs, files in os.walk(directory):
        list_directory.append(root)
        #print(list_directory)
    for subdirect in list_directory:  # обходим все директории и получаем из них файлы.
        #print(subdirect)
        list_for_extend.extend(get_list_files_in_folder(subdirect, frozen_dir=subdirect))
    return list_for_extend

def get_list_files_in_folder(directory, frozen_dir=''): #получения списка файлов в одной папке, подставляя frozen_dir спереди имени файла.
    files_list=[]
    for file in getting_dict_or_list(directory, folder=False, type_return='list'):  #тут получаем окончательный путь к файлу, типа string. 'H:\\работа\\копия\\Некрасовка съем\\Некрасовка Адреса 2018год.xlsx'
        if not "~$ " in file:  #проверка на временные файлы, временные файлы надо убрать
            files_list.append(frozen_dir + file)
    return files_list

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
        return list_return
    else:
        dict_finish = {}
        for x in finish_list:
            x = str(x)
            if key == 0:
                number_cut = x.rfind("\\")
            x = x[number_cut:]
            key += 1
            dict_finish[key] = x
        return dict_finish

def file_name_check(objs,
                        end_file=".docx"):  # функция проверяет есть ли в списке objs файлы с заданным окончанием и возвращает новый список с отсортированными файлами
    number_of_files = 0  # чтобы прописать сколько файлов найдено
    objs_sort = []
    for obj in objs:
        obj = str(obj)
        if end_file == obj[-len(end_file):]:
            objs_sort.append(obj)
            number_of_files += 1
    if objs_sort != []:
        return objs_sort, number_of_files
    else:
        return None, 0

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
