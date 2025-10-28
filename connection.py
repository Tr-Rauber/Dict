import sqlite3

class Database:
    def __init__(self):
        self.db_name = 'user_dictionary.db'
        self.create_tables()
        
    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                definition TEXT NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_categories_with_stats(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
            
        cursor.execute('''
            SELECT category, COUNT(*) as word_count 
            FROM words 
            WHERE user_id = ? 
            GROUP BY category 
            ORDER BY category
            ''', (user_id,))
            
        categories = cursor.fetchall()
        conn.close()
        return categories
        
    def get_random_word_from_category(self, user_id, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
            
        cursor.execute('''
            SELECT word, definition 
            FROM words 
            WHERE user_id = ? AND category = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (user_id, category))
        result = cursor.fetchone()
        conn.close()
        return result
        
    def register_user(self, login, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (login, password) VALUES (?, ?)',
                (login, password)
            )
            conn.commit()
            conn.close()
            return True, "Регистрация успешна"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Логин уже занят"
        except Exception as e:
            conn.close()
            return False, f"Ошибка: {str(e)}"
            
    def authenticate_user(self, login, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id FROM users WHERE login = ? AND password = ?',
            (login, password)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            return None
            
    def get_user_words(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT word, definition, category FROM words WHERE user_id = ?',
            (user_id,)
        )
        
        words = cursor.fetchall()
        conn.close()
        return words
            
    def add_word(self, user_id, word, definition, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO words (user_id, word, definition, category) VALUES (?, ?, ?, ?)',
            (user_id, word, definition, category)
        )
        
        conn.commit()
        conn.close()
        return True
            
    def delete_word(self, user_id, word):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'DELETE FROM words WHERE user_id = ? AND word = ?',
            (user_id, word)
        )
        
        conn.commit()
        conn.close()
        return True
    def get_user_categories(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT DISTINCT category FROM words WHERE user_id = ? ORDER BY category',
            (user_id,)
        )
        
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    def get_all_words_from_category(self, user_id, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT word, definition 
            FROM words 
            WHERE user_id = ? AND category = ?
        ''', (user_id, category))
        
        words = cursor.fetchall()
        conn.close()
        return words  # [(word, definition), ...]

    def add_category(self, user_id, category):
        return True