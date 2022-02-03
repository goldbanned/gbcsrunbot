import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            if result is None:
                return False
            return True

    def add_user(self, user_id, words):
        with self.connection:
            return self.cursor.execute("INSERT INTO users ('user_id', 'word_list') VALUES (?, ?)", (user_id, words,))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET 'active' = ? WHERE 'user_id' = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def get_user_by_id(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def get_change_menu_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT change_menu FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def update_change_menu(self, menu, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET change_menu = ? WHERE user_id = ?", (menu, user_id))
            self.connection.commit()

    def update_status_setting(self, number_setting, user_id, status):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET {number_setting} = ? WHERE user_id = ?", (status, user_id,))
            self.connection.commit()

    def get_status_setting(self, number_setting, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT {number_setting} FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def get_open_menu_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT open_menu FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def update_open_menu(self, menu, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET open_menu = ? WHERE user_id = ?", (menu, user_id))
            self.connection.commit()

    def get_change_text_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT change_text FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def update_change_text(self, menu, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET change_text = ? WHERE user_id = ?", (menu, user_id))
            self.connection.commit()

    def get_status_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def update_status_by_id(self, user_id, status):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
            self.connection.commit()

    def update_words_by_id(self, user_id, words, number, message):
        words[number] = message
        with self.connection:
            self.cursor.execute(f"UPDATE users SET word_list = ? WHERE user_id = ?", ('\n'.join(words), user_id))
            self.connection.commit()

    def get_all_words_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT word_list FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()[0]


