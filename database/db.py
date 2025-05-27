import sqlite3

DB_NAME = 'apostas.db'

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        saldo INTEGER DEFAULT 1000,
        admin BOOLEAN DEFAULT 0
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aposta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        criador_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        ativa BOOLEAN DEFAULT 1,
        vencedora_id INTEGER,
        FOREIGN KEY (criador_id) REFERENCES usuario(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS opcao_aposta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aposta_id INTEGER NOT NULL,
        texto TEXT NOT NULL,
        FOREIGN KEY (aposta_id) REFERENCES aposta(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aposta_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        aposta_id INTEGER NOT NULL,
        opcao_id INTEGER NOT NULL,
        valor INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id),
        FOREIGN KEY (aposta_id) REFERENCES aposta(id),
        FOREIGN KEY (opcao_id) REFERENCES opcao_aposta(id)
    )''')

    conn.commit()
    conn.close()