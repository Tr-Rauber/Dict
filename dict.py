from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout, 
    QHBoxLayout,
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QListWidget, 
    QMessageBox,
    QComboBox
)

from repit_words import RepititionWindow 

class DictionaryWindow(QMainWindow):
    def __init__(self, user_id, database):
        super().__init__()
        self.user_id = user_id
        self.db = database
        
        self.setWindowTitle("Мой словарь")
        self.resize(600, 400)
        
        self.init_ui()
        self.load_words()
        self.load_categories()
        
    def init_ui(self):

        self.add_btn = QPushButton('Добавить слово')
        self.delete_btn = QPushButton('Удалить выбранное слово')
        self.quit_btn = QPushButton('Выйти')
        self.repit_btn = QPushButton('Повторить слова')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        self.word_list = QListWidget()
        main_layout.addWidget(self.word_list)
        form_layout = QVBoxLayout()
        
        word_label = QLabel('Введите слово:')
        self.word_input = QLineEdit()
        form_layout.addWidget(word_label)
        form_layout.addWidget(self.word_input)
        
        definition_label = QLabel('Введите значение:')
        self.definition_input = QLineEdit()
        form_layout.addWidget(definition_label)
        form_layout.addWidget(self.definition_input)
        
        category_label = QLabel('Выберите или введите категорию:')
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.setPlaceholderText("Выберите или введите новую категорию")
        form_layout.addWidget(category_label)
        form_layout.addWidget(self.category_combo)
        
        form_layout.addWidget(self.add_btn)
        form_layout.addWidget(self.delete_btn)
        form_layout.addWidget(self.repit_btn)
        form_layout.addWidget(self.quit_btn)
        form_layout.addStretch()
        
        main_layout.addLayout(form_layout)
        central_widget.setLayout(main_layout)
        
        self.add_btn.clicked.connect(self.add_word)
        self.delete_btn.clicked.connect(self.delete_word)
        self.quit_btn.clicked.connect(self.quit)
        self.repit_btn.clicked.connect(self.open_repitition)
        
    def add_word(self):
        word = self.word_input.text().strip()
        definition = self.definition_input.text().strip()
        category = self.category_combo.currentText().strip()
        
        if not word or not definition or not category:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return
            
        success = self.db.add_word(self.user_id, word, definition, category)
        if success:
            self.load_words()
            self.load_categories()
            self.word_input.clear()
            self.definition_input.clear()
            self.category_combo.setCurrentText("")
            QMessageBox.information(self, "Успех", "Слово успешно добавлено!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить слово")
            
    def delete_word(self):
        current_item = self.word_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите слово для удаления")
            return
            
        item_text = current_item.text()
        word_to_delete = item_text.split(' | ')[0]
        
        success = self.db.delete_word(self.user_id, word_to_delete)
        if success:
            self.word_list.takeItem(self.word_list.currentRow())
            QMessageBox.information(self, "Успех", "Слово успешно удалено!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить слово")
            
    def load_words(self):
        words = self.db.get_user_words(self.user_id)
        self.word_list.clear()
        for word, definition, category in words:
            dict_record = f"{word} | {definition} | {category}"
            self.word_list.addItem(dict_record)
            
    def load_categories(self):
        categories = self.db.get_user_categories(self.user_id)
        self.category_combo.clear()
        self.category_combo.addItems(categories)

    def quit(self):
        from entrance import AuthWindow
        self.entrance = AuthWindow()
        self.entrance.show()
        self.close()

    def open_repitition(self):
        self.repitition_window = RepititionWindow(self.user_id, self.db)
        self.repitition_window.show()