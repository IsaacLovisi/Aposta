
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from models.usuario import Usuario

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.title_label = Label(text="[b]Sistema de Apostas[/b]", font_size=32, markup=True)
        layout.add_widget(self.title_label)

        self.nome_input = TextInput(hint_text="Nome do Perfil", multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.nome_input)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        entrar_btn = Button(text="Entrar", on_press=self.efetuar_login_com_nome_digitado)
        criar_btn = Button(text="Criar Novo Perfil", on_press=self.criar_perfil_com_nome_digitado)

        btn_layout.add_widget(entrar_btn)
        btn_layout.add_widget(criar_btn)
        layout.add_widget(btn_layout)

        admin_btn = Button(text="Login como Administrador", on_press=self.prompt_admin_login, size_hint_y=None, height=50)
        layout.add_widget(admin_btn)

        self.add_widget(layout)

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def efetuar_login_com_nome_digitado(self, instance):
        nome = self.nome_input.text.strip()
        if not nome:
            self.show_popup("Erro de Login", "Por favor, digite um nome de perfil.")
            return

        usuario = Usuario.buscar_por_nome(nome)
        if usuario:
            self.manager.current = 'menu'
            self.manager.get_screen('menu').set_usuario(usuario)
        else:
            self.show_popup("Erro de Login", f"Perfil '{nome}' não encontrado.")

    def criar_perfil_com_nome_digitado(self, instance):
        nome = self.nome_input.text.strip()
        if not nome:
            self.show_popup("Erro", "Por favor, digite um nome para criar o perfil.")
            return

        if Usuario.buscar_por_nome(nome):
            self.show_popup("Erro", f"O nome de perfil '{nome}' já está em uso.")
            return

        try:
            Usuario.criar(nome)
            novo_usuario = Usuario.buscar_por_nome(nome)
            if novo_usuario:
                self.show_popup("Sucesso", f"Perfil '{novo_usuario.nome}' criado com sucesso!")
                self.manager.current = 'menu'
                self.manager.get_screen('menu').set_usuario(novo_usuario)
            else:
                self.show_popup("Erro", "Falha ao criar ou encontrar o perfil.")
        except Exception as e:
            self.show_popup("Erro", str(e))

    def prompt_admin_login(self, instance):
        from kivy.uix.textinput import TextInput
        content = BoxLayout(orientation='vertical')
        nome_admin = TextInput(hint_text='Nome do administrador', multiline=False)
        content.add_widget(nome_admin)

        def on_confirm(instance):
            nome = nome_admin.text.strip()
            usuario = Usuario.buscar_por_nome(nome)
            if usuario and usuario.admin:
                self.manager.current = 'admin'
                self.manager.get_screen('admin').set_usuario(usuario)
            elif usuario:
                self.show_popup("Acesso Negado", f"'{nome}' não é um administrador.")
            else:
                self.show_popup("Erro", f"Administrador '{nome}' não encontrado.")
            popup.dismiss()

        confirm_btn = Button(text='Entrar', size_hint_y=None, height=40, on_press=on_confirm)
        content.add_widget(confirm_btn)

        popup = Popup(title="Login Administrador", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
