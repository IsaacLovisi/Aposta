
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView 
from models.aposta import Aposta

class ApostaScreen(Screen):
    def __init__(self, **kwargs):
        super(ApostaScreen, self).__init__(**kwargs)
        self.usuario = None
        self.criando = False 
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)

    def set_usuario(self, usuario, criando=False):
        self.usuario = usuario
        self.criando = criando
        self.main_layout.clear_widgets() 
        if self.criando:
            self.criar_aposta_ui()
        else:
            self.listar_apostas_ui()

    def criar_aposta_ui(self):
        self.main_layout.add_widget(Label(text="Criar Nova Aposta", font_size="22sp", size_hint_y=None, height=40))

        self.desc_input = TextInput(hint_text="Descrição da Aposta", multiline=False, size_hint_y=None, height=40)
        self.main_layout.add_widget(self.desc_input)

        self.opcao_inputs = []
        options_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        options_box.bind(minimum_height=options_box.setter('height')) 

        for i in range(2): 
            input_field = TextInput(hint_text=f"Opção {i+1}", multiline=False, size_hint_y=None, height=40)
            options_box.add_widget(input_field)
            self.opcao_inputs.append(input_field)
    

        self.main_layout.add_widget(options_box)
        
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_criar = Button(text="Criar Aposta", on_press=self.submeter_criacao_aposta)
        btn_voltar = Button(text="Voltar ao Menu", on_press=self.voltar_menu)
        button_layout.add_widget(btn_criar)
        button_layout.add_widget(btn_voltar)
        self.main_layout.add_widget(button_layout)

    def listar_apostas_ui(self):
        self.main_layout.add_widget(Label(text="Apostas Ativas", font_size="22sp", size_hint_y=None, height=40))

        scroll_view_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        scroll_view_content.bind(minimum_height=scroll_view_content.setter('height'))

        apostas = Aposta.listar_ativas()
        if not apostas:
            scroll_view_content.add_widget(Label(text="Nenhuma aposta ativa encontrada."))
        else:
            for aposta_obj in apostas:
                desc = aposta_obj.descricao[:60] + ("..." if len(aposta_obj.descricao) > 60 else "")
                btn_text = f"ID: {aposta_obj.id} - {desc}"
                btn = Button(text=btn_text, size_hint_y=None, height=40)
                btn.bind(on_press=lambda instance, current_aposta=aposta_obj: self.visualizar_aposta_detalhes(current_aposta))
                scroll_view_content.add_widget(btn)
        
        scroller = ScrollView(size_hint=(1, 1))
        scroller.add_widget(scroll_view_content)
        self.main_layout.add_widget(scroller)

        self.main_layout.add_widget(Button(text="Voltar ao Menu", on_press=self.voltar_menu, size_hint_y=None, height=40))

    def submeter_criacao_aposta(self, instance):
        desc = self.desc_input.text.strip()
        opcoes = [opt_input.text.strip() for opt_input in self.opcao_inputs if opt_input.text.strip()]

        if not desc or len(opcoes) < 2:
            self.mostrar_popup("Erro de Criação", "A descrição da aposta e pelo menos duas opções são obrigatórias.")
            return

        if self.usuario.saldo <= 0:
            self.mostrar_popup("Saldo Insuficiente", "Você não possui saldo suficiente para criar novas apostas.")
            return
        
        try:
            Aposta.criar(self.usuario.id, desc, opcoes)
            self.mostrar_popup("Sucesso", "Aposta criada com sucesso!")
            self.voltar_menu() 
        except Exception as e:
            self.mostrar_popup("Erro ao Criar", f"Falha ao criar aposta: {str(e)}")


    def visualizar_aposta_detalhes(self, aposta_obj):
        texto_popup = f"ID da Aposta: {aposta_obj.id}\n"
        texto_popup += f"Descrição: {aposta_obj.descricao}\n\n"
        texto_popup += "Opções de Aposta:\n"
        texto_popup += "(Funcionalidade de listar opções e apostar ainda não implementada.)"
        
        self.mostrar_popup(f"Detalhes da Aposta", texto_popup, size=(500,300))


    def voltar_menu(self, *args):
        if self.manager.has_screen('menu'):
            menu_screen = self.manager.get_screen('menu')
            if hasattr(menu_screen, 'set_usuario') and self.usuario:
                 menu_screen.set_usuario(self.usuario)
                 menu_screen.atualizar_saldo()
            self.manager.current = 'menu'
        else:
            self.mostrar_popup("Erro de Navegação", "Tela de menu não encontrada.")


    def mostrar_popup(self, title, text, size=(400, 200)):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=text, halign='center', valign='middle'))
        close_btn = Button(text="Fechar", size_hint_y=None, height=40)
        content.add_widget(close_btn)

        popup_widget = Popup(title=title, content=content,
                             size_hint=(None, None), size=size)
        close_btn.bind(on_press=popup_widget.dismiss)
        popup_widget.open()