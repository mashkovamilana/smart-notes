from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGroupBox, QVBoxLayout, QListWidget, QTextEdit, \
    QHBoxLayout, QLineEdit, QMessageBox
import os
import json

FILENAME = 'notes.json'

# dictionary to store notes in runtime
notes = {
    'Приветствие':
        {
            'текст': 'Добро пожаловать в умные заметки!',
            'теги': ['привет']
        },
    'Туториал':
        {
            'текст': 'Нажмите кнопку: "удалить заметку", чтобы удалить заметку, Нажмите кнопку: "Создать заметку", чтобы создать заметку, Нажмите кнопку: \
            "Почистить заметки", чтобы почистить заметки',
            'теги': ['чайник']
        }

}

app = QApplication([])
main_win = QWidget()
main_win.setFixedSize(800, 600)

main_win.setWindowTitle('Умные заметки')
notes_list_widget = QListWidget()
tags_list_widget = QListWidget()
text_edit = QTextEdit()
text_edit.setPlaceholderText('Введите текст заметки...')
notes_list_label = QLabel('Список заметок')
create_note_button = QPushButton('Создать заметку')
note_name_edit = QLineEdit()
note_name_edit.setPlaceholderText('Название заметки...')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметку')
tags_list_label = QLabel('Список тегов')
tag_line_edit = QLineEdit()
tag_line_edit.setPlaceholderText('Введите тег...')
add_tag_button = QPushButton('Добавить к заметке')
remove_tag_button = QPushButton('Открепить от заметки')
search_button = QPushButton('Искать заметки по тегу')
reset_button = QPushButton('Сбросить поиск')

layout_main = QHBoxLayout()
layout_sub = QHBoxLayout()
layout_sub2 = QHBoxLayout()
layout_sub3 = QHBoxLayout()
layout_sub4 = QHBoxLayout()

layuot2 = QVBoxLayout()
layout_main.addWidget(text_edit)
layuot2.addWidget(notes_list_label, alignment=Qt.AlignLeft)
layuot2.addWidget(notes_list_widget)
layout_sub.addWidget(delete_note_button)
layout_sub.addWidget(save_note_button)
layuot2.addLayout(layout_sub)
layout_sub3.addWidget(note_name_edit)
layout_sub3.addWidget(create_note_button, alignment=Qt.AlignCenter)
layuot2.addLayout(layout_sub3)
layuot2.addWidget(tags_list_label, alignment=Qt.AlignLeft)
layuot2.addWidget(tags_list_widget)
layuot2.addWidget(tag_line_edit)
layout_sub2.addWidget(add_tag_button)
layout_sub2.addWidget(remove_tag_button)
layuot2.addLayout(layout_sub2)
layout_sub4.addWidget(search_button, alignment=Qt.AlignCenter)
layout_sub4.addWidget(reset_button)
layuot2.addLayout(layout_sub4)

layout_main.addLayout(layuot2)
main_win.setLayout(layout_main)

if os.path.exists(FILENAME) and os.path.isfile(FILENAME):
    with open(FILENAME, 'r') as file:
        notes = json.load(file)
else:
    with open(FILENAME, 'w') as file:
        json.dump(notes, file)

notes_list_widget.addItems(notes)

def save_data():
    with open(FILENAME, 'w') as file:
        json.dump(notes, file)

def show_note():
    name = notes_list_widget.selectedItems()[0].text()
    text = notes[name]['текст']
    tags = notes[name]['теги']
    text_edit.setText(text)
    tags_list_widget.clear()
    tags_list_widget.addItems(tags)

def save_note():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Выберите заметку, чтобы ее сохранить')
        error_popup.exec_()
        return

    text = text_edit.toPlainText()
    name = notes_list_widget.selectedItems()[0].text()
    notes[name]['текст'] = text
    save_data()

def delete_note():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Выберите заметку, чтобы ее удалить')
        error_popup.exec_()
        return
    name = notes_list_widget.selectedItems()[0].text()
    del notes[name]
    notes_list_widget.clear()
    tags_list_widget.clear()
    notes_list_widget.addItems(notes)
    text_edit.clear()
    save_data()

def create_note():
    name = note_name_edit.text()
    temp = name.replace(' ', '')
    if temp == '':
        error_popup = QMessageBox()
        error_popup.setText('Название не может быть пустым')
        error_popup.exec_()
        return
    if name in notes:
        error_popup = QMessageBox()
        error_popup.setText('Такая заметка уже существует')
        error_popup.exec_()
        return
    notes[name] = {
        'текст': '',
        'теги': []
    }
    notes_list_widget.clear()
    notes_list_widget.addItems(notes)
    note_name_edit.clear()
    tags_list_widget.clear()
    save_data()

def add_tag():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Выберите заметку, чтобы  добавить к ней тег')
        error_popup.exec_()
        return
    tag = tag_line_edit.text()
    temp = tag.replace(' ', '')
    if temp == '':
        error_popup = QMessageBox()
        error_popup.setText('Название тега не может быть пустым')
        error_popup.exec_()
        return
    name = notes_list_widget.selectedItems()[0].text()
    if tag in notes[name]['теги']:
        error_popup = QMessageBox()
        error_popup.setText('Такой тег уже существует')
        error_popup.exec_()
        return
    notes[name]['теги'].append(tag)
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['теги'])
    save_data()

def delete_tag():
    if len(tags_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Выберите тег, чтобы его открепить от заметки')
        error_popup.exec_()
        return
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Выберите заметку, чтобы удалить ее тег')
        error_popup.exec_()
        return
    name = notes_list_widget.selectedItems()[0].text()
    tag = tags_list_widget.selectedItems()[0].text()
    notes[name]['теги'].remove(tag)
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['теги'])
    save_data()

def search():
    tag = tag_line_edit.text()
    filtered_notes = []
    for note in notes:
        if tag in notes[note]['теги']:
            filtered_notes.append(note)
    if len(filtered_notes) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Ничего не найдено')
        error_popup.exec_()
    else:
        notes_list_widget.clear()
        notes_list_widget.addItems(filtered_notes)

def reset_search():
    notes_list_widget.clear()
    notes_list_widget.addItems(notes)


reset_button.clicked.connect(reset_search)
search_button.clicked.connect(search)
remove_tag_button.clicked.connect(delete_tag)
add_tag_button.clicked.connect(add_tag)
create_note_button.clicked.connect(create_note)
delete_note_button.clicked.connect(delete_note)
save_note_button.clicked.connect(save_note)
notes_list_widget.itemClicked.connect(show_note)


main_win.show()
app.exec()
