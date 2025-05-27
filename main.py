# main_kivy_app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager 
from database.db import conectar, criar_tabelas
from models.usuario import Usuario
from ui.login_screen import LoginScreen
from ui.menu_screen import MenuScreen
from ui.admin_screen import AdminScreen
from ui.aposta_screen import ApostaScreen

import sqlite3


class SistemaApostasApp(App):
    def build(self):
        criar_tabelas()
        self.criar_admin_padrao_se_nao_existir()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu')) 
        sm.add_widget(AdminScreen(name='admin')) 
        sm.add_widget(ApostaScreen(name='aposta_screen'))

        return sm

    def criar_admin_padrao_se_nao_existir(self):
        nome_admin_padrao = "root"
        try:
            usuario_obj = Usuario.buscar_por_nome(nome_admin_padrao)
            if not usuario_obj:
                Usuario.criar(nome_admin_padrao, admin=True) 
                print(f"[INFO] Admin padrão '{nome_admin_padrao}' criado.")
            elif not usuario_obj.admin:
                print(f"[INFO] Usuário '{nome_admin_padrao}' encontrado, definindo como admin.")
                self.tornar_usuario_admin(nome_admin_padrao)
            else:
                print(f"[INFO] Admin padrão '{nome_admin_padrao}' já existe e é admin.")
        except Exception as e:
            print(f"[ERRO ao criar admin padrão]: {e}")

    def tornar_usuario_admin(self, nome_usuario):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, admin FROM usuario WHERE nome = ?", (nome_usuario,))
            resultado_usuario = cursor.fetchone()

            if resultado_usuario:
                user_id, admin_status_atual = resultado_usuario
                if not admin_status_atual: 
                    cursor.execute("UPDATE usuario SET admin = 1 WHERE nome = ?", (nome_usuario,))
                    conn.commit()
                    if cursor.rowcount > 0:
                        print(f"[INFO]: Usuário '{nome_usuario}' agora é administrador.")
                    else:
                        print(f"[AVISO]: Nenhuma linha afetada ao tentar tornar '{nome_usuario}' admin.")
                else:
                    print(f"[INFO]: Usuário '{nome_usuario}' já é administrador.")
            else:
                print(f"[ERRO]: Usuário '{nome_usuario}' não encontrado para ser admin.")
        except sqlite3.Error as e:
            print(f"[ERRO DB]: {e} (usuário: '{nome_usuario}')")
        except Exception as e:
            print(f"[ERRO Inesperado]: {e} (usuário: '{nome_usuario}')")
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    SistemaApostasApp().run()