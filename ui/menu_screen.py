
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.usuario = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.bem_vindo_label = Label(text="Bem-vindo!", font_size=24)
        self.layout.add_widget(self.bem_vindo_label)

        self.saldo_label = Label(text="Saldo: R$0.00", font_size=18)
        self.layout.add_widget(self.saldo_label)

        self.btn_apostas_ativas = Button(text="Ver Apostas Ativas", size_hint_y=None, height=40, on_press=self.ver_apostas)
        self.layout.add_widget(self.btn_apostas_ativas)

        self.btn_criar_aposta = Button(text="Criar Nova Aposta", size_hint_y=None, height=40, on_press=self.criar_aposta)
        self.layout.add_widget(self.btn_criar_aposta)

        self.btn_historico = Button(text="Histórico de Apostas", size_hint_y=None, height=40, on_press=self.ver_historico)
        self.layout.add_widget(self.btn_historico)

        self.btn_adicionar_saldo = Button(text="Adicionar Saldo", size_hint_y=None, height=40, on_press=self.adicionar_saldo_popup)
        self.layout.add_widget(self.btn_adicionar_saldo)

        self.btn_logout = Button(text="Logout", size_hint_y=None, height=40, on_press=self.logout)
        self.layout.add_widget(self.btn_logout)

        self.add_widget(self.layout)

    def set_usuario(self, usuario):
        self.usuario = usuario
        self.bem_vindo_label.text = f"Menu Principal - Bem-vindo, {usuario.nome}!"
        self.atualizar_saldo()

    def atualizar_saldo(self):
        if self.usuario:
            self.saldo_label.text = f"Seu saldo: R${self.usuario.saldo:.2f}"

    def ver_apostas(self, instance):

        if self.manager.has_screen('aposta_screen'):
            aposta_screen = self.manager.get_screen('aposta_screen')
            aposta_screen.set_usuario(self.usuario, criando=False)
            self.manager.current = 'aposta_screen'
        else:
            self.popup_info("Erro", "Tela de apostas não encontrada.")

    def criar_aposta(self, instance):
        if self.usuario and self.usuario.saldo <= 0: 
            self.popup_info("Saldo Insuficiente", "Você não tem saldo para criar apostas.")
            return

        if self.manager.has_screen('aposta_screen'):
            aposta_screen = self.manager.get_screen('aposta_screen')
            aposta_screen.set_usuario(self.usuario, criando=True)
            self.manager.current = 'aposta_screen'
        else:
            self.popup_info("Erro", "Tela de apostas não encontrada.")


    def ver_historico(self, instance):
        self.popup_info("Histórico", "Histórico de apostas ainda não implementado.")

    def adicionar_saldo_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        valor_input = TextInput(hint_text="Valor a adicionar", multiline=False, input_filter='float')
        popup_layout.add_widget(valor_input)

        popup = Popup(title="Adicionar Saldo", content=popup_layout,
                      size_hint=(None, None), size=(300, 200))

        def confirmar(button_instance):
            try:
                valor_str = valor_input.text.strip()
                if not valor_str:
                    self.popup_info("Erro", "Por favor, digite um valor.")
                    return
                valor = float(valor_str)
                if valor <= 0:
                    raise ValueError("Valor deve ser positivo.")
                self.usuario.adicionar_saldo(valor) 
                self.atualizar_saldo() 
                popup.dismiss()
                self.popup_info("Sucesso", f"R${valor:.2f} adicionados ao saldo!")
            except ValueError:
                self.popup_info("Erro", "Digite um valor numérico positivo válido.")
            except Exception as e:
                self.popup_info("Erro Inesperado", f"Ocorreu um erro: {str(e)}")


        confirmar_btn = Button(text="Adicionar")
        confirmar_btn.bind(on_press=confirmar)
        popup_layout.add_widget(confirmar_btn)
        
        popup.open()

    def logout(self, instance):
        self.manager.current = 'login'
        self.usuario = None 


    def popup_info(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()