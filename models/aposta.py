from database.db import conectar

class Aposta:
    def __init__(self, id, criador_id, descricao, ativa=True, vencedora_id=None):
        self.id = id
        self.criador_id = criador_id
        self.descricao = descricao
        self.ativa = ativa
        self.vencedora_id = vencedora_id

    @staticmethod
    def criar(criador_id, descricao, opcoes):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO aposta (criador_id, descricao) VALUES (?, ?)", (criador_id, descricao))
        aposta_id = cursor.lastrowid
        for opcao in opcoes:
            cursor.execute("INSERT INTO opcao_aposta (aposta_id, texto) VALUES (?, ?)", (aposta_id, opcao))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_ativas():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, criador_id, descricao, ativa, vencedora_id FROM aposta WHERE ativa = 1")
        apostas = [Aposta(*row) for row in cursor.fetchall()]
        conn.close()
        return apostas

    def cancelar(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE aposta SET ativa = 0 WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    def encerrar(self, vencedora_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE aposta SET ativa = 0, vencedora_id = ? WHERE id = ?", (vencedora_id, self.id))
        conn.commit()
        conn.close()
