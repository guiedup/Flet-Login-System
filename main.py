import flet as ft
import sqlite3
from datetime import datetime
import hashlib

# Função para inicializar/criar o banco de dados
def init_db():
    conn = sqlite3.connect('login_db.sqlite')
    c = conn.cursor()
    # Cria tabela de usuários se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  full_name TEXT,
                  email TEXT,
                  birth_date TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

init_db()

def main(page: ft.Page):
    # Configuração inicial da página
    page.title = "Sistema de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # Tema escuro padrão
    
    # Variável para armazenar a data selecionada
    selected_date = datetime.now()
    
    # ========== FUNÇÕES AUXILIARES ========== #

    def hash_password(password):
        """Cria hash SHA-256 da senha (para segurança básica)"""
        return hashlib.sha256(password.encode()).hexdigest()

    def show_error(message):
        """Exibe mensagem de erro na interface"""
        status_message.value = message
        status_message.color = ft.colors.RED
        page.update()

    def show_success(message):
        """Exibe mensagem de sucesso na interface"""
        status_message.value = message
        status_message.color = ft.colors.GREEN
        page.update()

    def birthday_changed(e):
        date_display.value = e.control.value.strftime("%Y-%m-%d")
        page.update()
    # ========== COMPONENTES DE DATA ========== #

    # Campo para exibir a data selecionada
    date_display = ft.TextField(
        label="Data de Nascimento",
        width=300,
        read_only=True,
        suffix_icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime(year=1925, month=10, day=1),
                    last_date=datetime.now(),
                    on_change=birthday_changed,
                )
        )
    )


    # ========== COMPONENTES DA INTERFACE ========== #
    # Ícone do aplicativo
    app_icon = ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=100)
    
    # Campo de usuário
    username = ft.TextField(
        label="Nome de usuário",
        width=300,
        prefix_icon=ft.icons.PERSON
    )
    
    # Campo de senha
    password = ft.TextField(
        label="Senha",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK
    )
    
    # Mensagem de status
    status_message = ft.Text()

    # ========== FUNCIONALIDADE DE LOGIN ========== #
    def validate_login(e):
        """Valida as credenciais do usuário"""
        try:
            conn = sqlite3.connect('login_db.sqlite')
            c = conn.cursor() 
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                (username.value, hash_password(password.value)))
            user = c.fetchone()
            conn.close()
            
            if user:
                show_success("Login realizado com sucesso!")
            else:
                show_error("Login ou senha não encontrados!")
        except Exception as e:
            show_error(f"Erro no banco de dados: {str(e)}")

    # ========== TELA DE CADASTRO ========== #
    def create_register_view():
        """Cria a tela de cadastro de novos usuários"""
        return ft.Column(
            [
                ft.Text("Criar Nova Conta", size=20, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Nome Completo", width=300),
                ft.TextField(label="E-mail", width=300),
                ft.Row([date_display], alignment=ft.MainAxisAlignment.CENTER),
                ft.TextField(label="Nome de Usuário", width=300),
                ft.TextField(label="Senha", password=True, width=300),
                ft.TextField(label="Confirmar Senha", password=True, width=300),
                ft.ElevatedButton("Cadastrar", on_click=register_user),
                ft.TextButton("Voltar para Login", on_click=lambda e: show_login_view())
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def register_user(e):
        """Registra novo usuário no banco de dados"""
        try:
            controls = page.controls[0].controls
            fields = {
                'full_name': controls[1].value.strip(),
                'email': controls[2].value.strip(),
                'birth_date': selected_date.strftime("%Y-%m-%d"),
                'username': controls[4].value.strip(),
                'password': controls[5].value,
                'confirm_password': controls[6].value
            }

            # Validação dos campos
            if not all(fields.values()):
                show_error("Todos os campos são obrigatórios!")
                return
                
            if fields['password'] != fields['confirm_password']:
                show_error("As senhas não coincidem!")
                return

            conn = sqlite3.connect('login_db.sqlite')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, full_name, email, birth_date, password) VALUES (?, ?, ?, ?, ?)",
                    (fields['username'],
                    fields['full_name'],
                    fields['email'],
                    fields['birth_date'],
                    hash_password(fields['password'])))
            conn.commit()
            conn.close()
            
            show_login_view()
            show_success("Conta criada com sucesso!")

        except sqlite3.IntegrityError:
            show_error("Nome de usuário já existe!")
        except Exception as e:
            show_error(f"Erro no cadastro: {str(e)}")

    # ========== NAVEGAÇÃO ENTRE TELAS ========== #
    def show_register_view(e):
        page.controls[0] = create_register_view()
        page.update()

    def show_login_view():
        page.controls[0] = login_view
        page.update()

    # ========== LAYOUT PRINCIPAL ========== #
    login_view = ft.Column(
        [
            app_icon,
            username,
            password,
            ft.ElevatedButton("Login", on_click=validate_login),
            ft.Row(
                [
                    ft.TextButton("Esqueci minha senha", 
                        on_click=lambda e: show_success("Funcionalidade em desenvolvimento!")),
                    ft.TextButton("Criar conta", on_click=show_register_view)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            status_message
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(login_view)

if __name__ == "__main__":
    ft.app(target=main)