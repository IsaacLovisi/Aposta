# 🎲 Sistema de Apostas em Kivy

Bem-vindo ao Sistema de Apostas em Kivy! Este é um aplicativo de desktop desenvolvido em Python com a biblioteca Kivy, permitindo que usuários criem perfis, gerenciem saldos, criem e participem de apostas. Administradores também possuem um painel dedicado para gerenciar usuários e o sistema.

![Kivy](https://img.shields.io/badge/Kivy-Python%20GUI-informational?style=flat&logo=kivy&logoColor=white&color=black)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-SQL%20Database-blue?style=flat&logo=sqlite&logoColor=white)

## 📝 Descrição

Este projeto é uma plataforma simples para simular um ambiente de apostas. Usuários podem se registrar, adicionar saldo à sua conta, visualizar apostas disponíveis e criar novas apostas. Administradores têm a capacidade de gerenciar o sistema, incluindo a promoção de usuários a administradores. Os dados são armazenados localmente usando SQLite.

## ✨ Funcionalidades Principais

* **Autenticação de Usuários:**
    * Login para usuários existentes.
    * Criação de novos perfis de usuário.
    * Login dedicado para administradores (usuário padrão 'root' criado na primeira execução).
* **Gerenciamento de Saldo:**
    * Usuários iniciam com um saldo padrão.
    * Funcionalidade para adicionar mais saldo à conta.
* **Sistema de Apostas:**
    * Criação de novas apostas com descrição e múltiplas opções.
    * Listagem de apostas ativas.
    * (Futuro: Mecanismo para usuários apostarem em opções específicas).
* **Painel Administrativo:**
    * Visualização do status de administrador.
    * Capacidade de promover outros usuários a administradores.
    * (Futuro: Gerenciamento completo de usuários e apostas).
* **Interface Gráfica:**
    * Interface de usuário intuitiva construída com Kivy.
    * Navegação baseada em telas (`ScreenManager`).
* **Persistência de Dados:**
    * Uso do SQLite para armazenar informações de usuários, apostas e saldos.


## 🛠️ Tecnologias Utilizadas

* **Python 3.x:** Linguagem principal de desenvolvimento.
* **Kivy:** Biblioteca open-source Python para criação de interfaces de usuário com NUI (Natural User Interface).
* **SQLite3:** Sistema de gerenciamento de banco de dados relacional embarcado.

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado em sua máquina:

* Python 3.7 ou superior.
* PIP (gerenciador de pacotes Python).

## 🚀 Instalação e Execução

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/IsaacLovisi/ApostaTwitch.git
    cd ApostaTwitch
    ```

2. **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3. **Instale as dependências (principalmente Kivy):**
    ```bash
    python -m pip install "kivy[base]" kivy_examples
    # Ou, se você criar um arquivo requirements.txt:
    # pip install -r requirements.txt
    ```

    *Nota: Pode haver dependências adicionais do Kivy dependendo do seu sistema operacional. Consulte a [documentação oficial do Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html) para mais detalhes.*

4. **Execute a aplicação:**
    ```bash
    python main_kivy_app.py
    ```

    Na primeira execução, um usuário administrador padrão chamado `root` será criado. Você pode usar este usuário para acessar o painel de administração e promover outros usuários.

## 📁 Estrutura do Projeto

```text
.
├── main_kivy_app.py         # Ponto de entrada principal da aplicação
├── database/
│   └── db.py                # Configuração do banco de dados e criação de tabelas
├── models/
│   ├── usuario.py           # Modelo de dados e lógica para Usuário
│   └── aposta.py            # Modelo de dados e lógica para Aposta
└── ui/
    ├── login_screen.py      # Lógica e layout da Tela de Login
    ├── menu_screen_kivy.py  # Lógica e layout da Tela Principal do Usuário
    ├── admin_screen_kivy.py # Lógica e layout da Tela do Administrador
    └── aposta_screen_kivy.py# Lógica e layout da Tela para criar/visualizar Apostas
```

## 🎯 Próximos Passos (To-Do)

* [ ] Implementar a funcionalidade de "fazer uma aposta" (usuário seleciona uma opção e investe um valor).
* [ ] Desenvolver o mecanismo de encerramento de apostas (definir opção vencedora).
* [ ] Calcular e distribuir os ganhos aos usuários vencedores.
* [ ] Completar o CRUD (Criar, Ler, Atualizar, Deletar) de usuários e apostas no painel administrativo.
* [ ] Adicionar um histórico de apostas para os usuários.
* [ ] Permitir que administradores cancelem apostas ou editem suas opções.
* [ ] Melhorar a interface do usuário (UI/UX) e adicionar mais feedback visual.
* [ ] Adicionar testes unitários e de integração.


