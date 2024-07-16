import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            user_id INTEGER UNIQUE NOT NULL,
            referer_id  INTEGER,
            ref_balance REAL DEFAULT (0) 
            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bankcards(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    tinkoff VARCHAR,
                    sberbank VARCHAR,
                    qiwi VARCHAR,
                    sbp VARCHAR,
                    btc VARCHAR,
                    usdt VARCHAR,
                    eth VARCHAR,
                    trx VARCHAR,
                    xmr VARCHAR 
                    )''')
        line = 'Не указано. Уточняйте у @yvs99'
        self.cursor.execute('INSERT OR IGNORE INTO bankcards (id, tinkoff, sberbank, qiwi, sbp, btc, usdt, eth, trx, xmr) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', (1, line, line, line, line, line, line, line, line, line))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id = None):
        with self.connection:
            if referer_id != None:
                return self.cursor.execute("INSERT INTO 'users' ('user_id', 'referer_id') VALUES (?,?)", (user_id, referer_id))
            else:
                return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def get_refbalance(self, user_id):
        with self.connection:
            res = self.cursor.execute('SELECT ref_balance FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return int(res[0])

    def null_refbalance(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET ref_balance = 0 WHERE user_id = ?", (user_id,))

    def add_refbalance(self, user_id, bonus):
        with self.connection:
            referer_id = str(self.cursor.execute("SELECT referer_id FROM users WHERE user_id = ?", (user_id,)).fetchone()[0])
            if referer_id:
                referer_balance = int(self.cursor.execute("SELECT ref_balance FROM users WHERE user_id = ?", (referer_id,)).fetchone()[0])
                referer_balance += bonus
                return self.cursor.execute('UPDATE users SET ref_balance = ? WHERE user_id = ?', (referer_balance, referer_id))
            else:
                pass

    def check_referer(self, user_id):
        with self.connection:
            referer_id = self.cursor.execute("SELECT referer_id FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if referer_id:
                return int(referer_id)
            else:
                return 0

    def set_bankcard(self, bank, number):
        with self.connection:
            if bank == 'chng_tink':
                return self.cursor.execute('UPDATE bankcards SET tinkoff = ? WHERE id = ?', (number, 1))
            elif bank == 'chng_sber':
                return self.cursor.execute('UPDATE bankcards SET sberbank = ? WHERE id = ?', (number, 1))
            elif bank == 'chng_qiwi':
                return self.cursor.execute('UPDATE bankcards SET qiwi = ? WHERE id = ?', (number, 1))
            elif bank == 'chng_sbp':
                return self.cursor.execute('UPDATE bankcards SET sbp = ? WHERE id = ?', (number, 1))
            elif bank == 'chng_btc':
                return self.cursor.execute('UPDATE bankcards SET btc =? WHERE id =?', (number, 1))
            elif bank == 'chng_usdt':
                return self.cursor.execute('UPDATE bankcards SET usdt =? WHERE id =?', (number, 1))
            elif bank == 'chng_eth':
                return self.cursor.execute('UPDATE bankcards SET eth =? WHERE id =?', (number, 1))
            elif bank == 'chng_trx':
                return self.cursor.execute('UPDATE bankcards SET trx =? WHERE id =?', (number, 1))
            elif bank == 'chng_xmr':
                return self.cursor.execute('UPDATE bankcards SET xmr =? WHERE id =?', (number, 1))

    def get_bankcard(self, bank):
        if bank == 'chng_tink':
            return self.cursor.execute('SELECT tinkoff FROM bankcards').fetchone()[0]
        elif bank == 'chng_sber':
            return self.cursor.execute('SELECT sberbank FROM bankcards').fetchone()[0]
        elif bank == 'chng_qiwi':
            return self.cursor.execute('SELECT qiwi FROM bankcards').fetchone()[0]
        elif bank == 'chng_sbp':
            return self.cursor.execute('SELECT sbp FROM bankcards').fetchone()[0]
        elif bank == 'chng_btc':
            return self.cursor.execute('SELECT btc FROM bankcards').fetchone()[0]
        elif bank == 'chng_usdt':
            return self.cursor.execute('SELECT usdt FROM bankcards').fetchone()[0]
        elif bank == 'chng_eth':
            return self.cursor.execute('SELECT eth FROM bankcards').fetchone()[0]
        elif bank == 'chng_trx':
            return self.cursor.execute('SELECT trx FROM bankcards').fetchone()[0]
        elif bank == 'chng_xmr':
            return self.cursor.execute('SELECT xmr FROM bankcards').fetchone()[0]
