from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QComboBox
)

class RepititionWindow(QMainWindow):
    def __init__(self, user_id, db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.current_category = None
        self.used_words = set()  
        self.all_words = [] 
        self.current_word = None 
        self.current_definition = None
        
        self.setWindowTitle("Повторение слов")
        self.init_ui()
        self.load_categories()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        category_layout = QHBoxLayout()
        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()

        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        
        self.definition_label = QLabel("Выберите категорию")
        self.definition_label.setWordWrap(True)
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введите слово...")
        self.check_btn = QPushButton("Проверить")
        self.status_label = QLabel("")
        
        layout.addLayout(category_layout)
        layout.addWidget(self.definition_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
        
        self.category_combo.currentTextChanged.connect(self.category_changed)
        self.check_btn.clicked.connect(self.check_answer)
        self.answer_input.returnPressed.connect(self.check_answer)
        
    def load_categories(self):
        categories = self.db.get_categories_with_stats(self.user_id)  # ← ДОБАВЬ ЭТУ СТРОКУ
        self.category_combo.clear()
        
        for category, count in categories:
            self.category_combo.addItem(f"{category} ({count} слов)", category)
            
    def category_changed(self):
        if self.category_combo.currentData():
            self.current_category = self.category_combo.currentData()
            self.all_words = self.db.get_all_words_from_category(self.user_id, self.current_category)
            self.used_words.clear() 
            self.answer_input.setEnabled(True)
            self.check_btn.setEnabled(True)
            self.load_new_word()

    def load_new_word(self):
        if not self.current_category:
            return
            
        if len(self.used_words) >= len(self.all_words):
            self.definition_label.setText("Все слова в этой категории пройдены!")
            self.answer_input.setEnabled(False)
            self.check_btn.setEnabled(False)
            self.status_label.setText("Выберите другую категорию")
            return

        available_words = [word for word in self.all_words if word[0] not in self.used_words]
        if available_words:
            import random
            self.current_word, self.current_definition = random.choice(available_words)
            self.definition_label.setText(f"Определение: {self.current_definition}")
            self.answer_input.clear()
            self.answer_input.setFocus() 
            
    def check_answer(self):
        if not self.current_word:
            return
            
        user_answer = self.answer_input.text().strip().lower()
        correct_answer = self.current_word.lower()
        
        if user_answer == correct_answer:
            self.used_words.add(self.current_word)
            words_left = len(self.all_words) - len(self.used_words)
            self.status_label.setText("Правильно!")
            self.load_new_word()
        else:
            self.status_label.setText("Неправильно! Попробуйте еще раз.")
            self.answer_input.clear()
            self.answer_input.setFocus()
            
    def next_word(self):
        self.load_new_word()