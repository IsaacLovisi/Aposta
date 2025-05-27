
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from models.usuario import Usuario


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.usuario = None 

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.bem_vindo_label = Label(text="Bem-vindo, Admin", font_size=24)
        self.layout.add_widget(self.bem_vindo_label)


        self.saldo_label = Label(text="Painel Administrativo", font_size=18)
        self.layout.add_widget(self.saldo_label)

        self.btn_ver_usuarios = Button(text="Gerenciar Usuários", size_hint_y=None, height=40, on_press=self.gerenciar_usuarios)
        self.layout.add_widget(self.btn_ver_usuarios)

        self.btn_tornar_admin = Button(text="Tornar Usuário Admin", size_hint_y=None, height=40, on_press=self.tornar_usuario_admin_popup)
        self.layout.add_widget(self.btn_tornar_admin)

        self.btn_logout = Button(text="Logout", size_hint_y=None, height=40, on_press=self.logout)
        self.layout.add_widget(self.btn_logout)

        self.add_widget(self.layout)

    def set_usuario(self, usuario): 
        self.usuario = usuario
        self.bem_vindo_label.text = f"Admin: {usuario.nome}"

    def gerenciar_usuarios(self, instance):
        self.popup_info("Gerenciar Usuários", "Funcionalidade ainda não implementada.")

    def tornar_usuario_admin_popup(self, instance):
        content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        nome_input = TextInput(hint_text="Nome do usuário a tornar admin", multiline=False)
        content_layout.add_widget(nome_input)
        popup = Popup(title="Tornar Usuário Admin", content=content_layout,
                      size_hint=(None, None), size=(350, 200))

        def confirmar(button_instance):
            nome_alvo = nome_input.text.strip()
            if not nome_alvo:
                self.popup_info("Erro", "Nome do usuário não pode ser vazio.")
                return

            user_alvo = Usuario.buscar_por_nome(nome_alvo)
            if user_alvo:
                if user_alvo.admin:
                    self.popup_info("Informação", f"Usuário '{nome_alvo}' já é administrador.")
                elif user_alvo.definir_como_admin(True):
                    self.popup_info("Sucesso", f"Usuário '{nome_alvo}' agora é administrador.")
                else:
                    self.popup_info("Falha", f"Não foi possível tornar '{nome_alvo}' administrador. Verifique os logs.")
            else:
                self.popup_info("Erro", f"Usuário '{nome_alvo}' não encontrado.")
            popup.dismiss()

        confirm_btn = Button(text="Confirmar")
        confirm_btn.bind(on_press=confirmar)
        content_layout.add_widget(confirm_btn)
        
        popup.open()

    def logout(self, instance):
        self.manager.current = 'login'

    def popup_info(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()