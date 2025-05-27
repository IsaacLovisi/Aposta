import sqlite3
from database.db import conectar

class Usuario:
    def __init__(self, id, nome, saldo=1000, admin=False):
        self.id = id
        self.nome = nome
        self.saldo = saldo
        self.admin = bool(admin) 

    @staticmethod
    def criar(nome, admin=False):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuario (nome, admin) VALUES (?, ?)", (nome, 1 if admin else 0))
            conn.commit()
            print(f"[INFO] Usuário '{nome}' criado com admin_status={admin}.")
        except sqlite3.Error as e:
            print(f"[DB ERRO ao criar usuário '{nome}']: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, saldo, admin FROM usuario")
        usuarios = [Usuario(*row) for row in cursor.fetchall()]
        conn.close()
        return usuarios

    @staticmethod
    def buscar_por_nome(nome):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, saldo, admin FROM usuario WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(*row) 
        return None

    def adicionar_saldo(self, valor):
        self.saldo += valor
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuario SET saldo = ? WHERE id = ?", (self.saldo, self.id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[DB ERRO ao adicionar saldo para ID {self.id}]: {e}")
            self.saldo -= valor 
        finally:
            conn.close()

    def remover(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuario WHERE id = ?", (self.id,))
            conn.commit()
            print(f"[INFO] Usuário ID {self.id} removido.")
        except sqlite3.Error as e:
            print(f"[DB ERRO ao remover usuário ID {self.id}]: {e}")
        finally:
            conn.close()


    def definir_como_admin(self, admin_status=True):
        conn = conectar()
        cursor = conn.cursor()
        try:
            novo_status_db = 1 if admin_status else 0
            cursor.execute("UPDATE usuario SET admin = ? WHERE id = ?", (novo_status_db, self.id))
            conn.commit()
            if cursor.rowcount > 0:
                self.admin = admin_status 
                print(f"[INFO] Usuário '{self.nome}' (ID: {self.id}) atualizado para admin: {admin_status}")
                return True
            else:
                print(f"[AVISO] Nenhuma linha afetada. Usuário '{self.nome}' (ID: {self.id}) não atualizado para admin: {admin_status}.")
                cursor.execute("SELECT admin FROM usuario WHERE id = ?", (self.id,))
                current_db_status_row = cursor.fetchone()
                if current_db_status_row and current_db_status_row[0] == novo_status_db:
                    self.admin = admin_status 
                    return True 
                return False
        except sqlite3.Error as e:
            print(f"[DB ERRO ao definir admin para '{self.nome}']: {e}")
            return False
        finally:
            conn.close()