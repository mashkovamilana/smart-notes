from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGroupBox, QVBoxLayout, QListWidget, QTextEdit, \
    QHBoxLayout, QLineEdit, QMessageBox
import os
import json

FILENAME = 'notes.json'

# dictionary to store notes in runtime
notes = {
    'Greetings':
        {
            'text': 'Welcome to Smart notes!',
            'tags': ['Hello']
        },
    'Tutorial':
        {
            'text': 'Click: “delete note” to delete a note, Click: “create note” to create a note, Click: \
            “Clear Notes” button to clear notes',
            'tags': ['Kettle']
        }

}

app = QApplication([])
main_win = QWidget()
main_win.setFixedSize(800, 600)

main_win.setWindowTitle('Smart notes')
notes_list_widget = QListWidget()
tags_list_widget = QListWidget()
text_edit = QTextEdit()
text_edit.setPlaceholderText('Enter the text of the note...')
notes_list_label = QLabel('List of notes')
create_note_button = QPushButton('Create a note')
note_name_edit = QLineEdit()
note_name_edit.setPlaceholderText('Note title...')
delete_note_button = QPushButton('Delete note')
save_note_button = QPushButton('Save note')
tags_list_label = QLabel('List of tags')
tag_line_edit = QLineEdit()
tag_line_edit.setPlaceholderText('Enter tag...')
add_tag_button = QPushButton('Add to note')
remove_tag_button = QPushButton('Unpin from note')
search_button = QPushButton('Search notes by tag')
reset_button = QPushButton('Reset search')

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
    text = notes[name]['text']
    tags = notes[name]['tags']
    text_edit.setText(text)
    tags_list_widget.clear()
    tags_list_widget.addItems(tags)

def save_note():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Select a note to save it')
        error_popup.exec_()
        return

    text = text_edit.toPlainText()
    name = notes_list_widget.selectedItems()[0].text()
    notes[name]['text'] = text
    save_data()

def delete_note():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Select a note to delete it')
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
        error_popup.setText('Name cannot be empty')
        error_popup.exec_()
        return
    if name in notes:
        error_popup = QMessageBox()
        error_popup.setText('Such a note already exists')
        error_popup.exec_()
        return
    notes[name] = {
        'text': '',
        'tags': []
    }
    notes_list_widget.clear()
    notes_list_widget.addItems(notes)
    note_name_edit.clear()
    tags_list_widget.clear()
    save_data()

def add_tag():
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Select a note to add a tag to it')
        error_popup.exec_()
        return
    tag = tag_line_edit.text()
    temp = tag.replace(' ', '')
    if temp == '':
        error_popup = QMessageBox()
        error_popup.setText('Tag name cannot be empty')
        error_popup.exec_()
        return
    name = notes_list_widget.selectedItems()[0].text()
    if tag in notes[name]['tags']:
        error_popup = QMessageBox()
        error_popup.setText('Such tag already exists')
        error_popup.exec_()
        return
    notes[name]['tags'].append(tag)
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['tags'])
    save_data()

def delete_tag():
    if len(tags_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Select a tag to unpin from a note')
        error_popup.exec_()
        return
    if len(notes_list_widget.selectedItems()) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Select a note to remove a tag')
        error_popup.exec_()
        return
    name = notes_list_widget.selectedItems()[0].text()
    tag = tags_list_widget.selectedItems()[0].text()
    notes[name]['tags'].remove(tag)
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['tags'])
    save_data()

def search():
    tag = tag_line_edit.text()
    filtered_notes = []
    for note in notes:
        if tag in notes[note]['tags']:
            filtered_notes.append(note)
    if len(filtered_notes) == 0:
        error_popup = QMessageBox()
        error_popup.setText('Nothing found')
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
