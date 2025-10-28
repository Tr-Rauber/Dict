from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QMessageBox, 
    QStackedWidget
)
from connection import Database
from dict import DictionaryWindow

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Словарь пользователя - Авторизация")
        #self.resize(400, 300)
        
        self.db = Database()
        self.current_user_id = None
        self.init_ui()
        
    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_btn = QPushButton("Войти")
        self.register_btn = QPushButton("Зарегистрироваться")
        self.switch_to_register_btn = QPushButton("Регистрация")
        
        self.auth_page = QWidget()
        self.auth_layout = QVBoxLayout()
        
        self.auth_title = QLabel("Авторизация")
        self.auth_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        
        
        self.auth_layout.addWidget(self.auth_title)
        self.auth_layout.addWidget(self.login_label)
        self.auth_layout.addWidget(self.login_input)
        self.auth_layout.addWidget(self.password_label)
        self.auth_layout.addWidget(self.password_input)
        self.auth_layout.addWidget(self.login_btn)
        self.auth_layout.addWidget(self.switch_to_register_btn)
        self.auth_layout.addStretch()
        
        self.auth_page.setLayout(self.auth_layout)
        
        self.register_page = QWidget()
        self.register_layout = QVBoxLayout()
        
        self.register_title = QLabel("Регистрация")
        self.register_title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        self.new_login_label = QLabel("Логин:")
        self.new_login_input = QLineEdit()
        self.new_login_input.setPlaceholderText("Придумайте логин")
        
        self.new_password_label = QLabel("Пароль:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Придумайте пароль")
        
        self.confirm_password_label = QLabel("Подтвердите пароль:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Повторите пароль")
        
        self.register_confirm_btn = QPushButton("Зарегистрироваться")
        self.switch_to_auth_btn = QPushButton("Уже есть аккаунт? Войдите")
        
        self.register_layout.addWidget(self.register_title)
        self.register_layout.addWidget(self.new_login_label)
        self.register_layout.addWidget(self.new_login_input)
        self.register_layout.addWidget(self.new_password_label)
        self.register_layout.addWidget(self.new_password_input)
        self.register_layout.addWidget(self.confirm_password_label)
        self.register_layout.addWidget(self.confirm_password_input)
        self.register_layout.addWidget(self.register_confirm_btn)
        self.register_layout.addWidget(self.switch_to_auth_btn)
        self.register_layout.addStretch()
        
        self.register_page.setLayout(self.register_layout)
        
        self.stacked_widget.addWidget(self.auth_page)
        self.stacked_widget.addWidget(self.register_page)
        
        self.login_btn.clicked.connect(self.login)
        self.register_confirm_btn.clicked.connect(self.register)
        self.switch_to_register_btn.clicked.connect(self.show_register_form)
        self.switch_to_auth_btn.clicked.connect(self.show_login_form)

    def show_login_form(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_register_form(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        user_id = self.db.authenticate_user(login, password)
        if user_id:
            self.current_user_id = user_id
            self.open_dictionary()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            
    def register(self):
        login = self.new_login_input.text().strip()
        password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        
        success, message = self.db.register_user(login, password)
        if success:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.stacked_widget.setCurrentIndex(0)
            self.new_login_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.warning(self, "Ошибка", message)
            
    def open_dictionary(self):
        self.dictionary_window = DictionaryWindow(self.current_user_id, self.db)
        self.dictionary_window.show()
        self.hide()
        
        self.login_input.clear()
        self.password_input.clear()