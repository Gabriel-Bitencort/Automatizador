from loginWindow import LoginWindow
from mainWindow import MainWindow
from registerWindow import RegisterWindow
import tkinter as tk
import sqlite3

database = 'Automatizador.db'

def open_mainWindow():
    loginWindow.window.destroy()
    mainWindow = MainWindow(lambda: open_registerWindow(loginWindow))
    mainWindow.window.mainloop()


def open_registerWindow(login_window):
    registerWindow = RegisterWindow(lambda: userRegister(registerWindow))
    registerWindow.window.mainloop()


def clear_input_fields(input_fields):
    for entry in input_fields:
        entry.delete(0, tk.END)


def call_main_window(event=None):
    loginWindow.text_message.config(text='')
    user_name = loginWindow.input_name.get()
    password = loginWindow.input_passwd.get()
    if user_name and password:
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE name = ? AND passwd = ?', (user_name, password))
            user = cursor.fetchone()
            db.close()

            if user is not None:
                loginWindow.text_message.config(text='Login realizado com secesso')
                loginWindow.window.after(1000, open_mainWindow())
            else:
                loginWindow.text_message.config(text='Dados de login incorretos')
        except sqlite3.Error as error:
            print("Erro ao consultar o banco de dados: ", error)
    else:
        loginWindow.text_message.config(text='Preencha todos os campos.')


# Function to verify if name and email exists
def check_duplicate_user(name, email):
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        # Execute a cunsult to verify if exists a user with same name
        cursor.execute('SELECT * FROM users WHERE name = ? OR email = ?', (name, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Erro ao verificar duplicatas: ", error)
        return True
    finally:
        db.close()


# Function to register users
def userRegister(registerWindow):
    user_login = registerWindow.input_name.get()
    user_email = registerWindow.input_email.get()
    user_passwd = registerWindow.input_passwd.get()
    user_cpass = registerWindow.input_cpass.get()

    input_fields = [registerWindow.input_name, registerWindow.input_email, registerWindow.input_passwd,
                    registerWindow.input_cpass]

    if user_login and user_email and user_passwd and user_cpass:
        if user_passwd == user_cpass:
            if check_duplicate_user(user_login, user_email):
                registerWindow.text_message.config(text="Nome ou email já foram cadastrados.")
                # Clear input fields
                clear_input_fields(input_fields)
            else:
                try:
                    db = sqlite3.connect(database)
                    cursor = db.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   id INTEGER PRIMARY KEY,
                                   name TEXT, 
                                   email TEXT, 
                                   passwd TEXT
                                   )
                    ''')
                    cursor.execute('INSERT INTO users (name, email, passwd) VALUES (?, ?, ?)',
                                   (user_login, user_email, user_passwd))
                    db.commit()
                    db.close()
                    registerWindow.text_message.config(text="Usuário cadastrado com sucesso.")

                    # Clear input fields
                    clear_input_fields(input_fields)

                except sqlite3.Error as error:
                    registerWindow.text_message.config(text="Erro ao inserir os dados!")
                    print("Erro ao inserir os dados: ", error)
        else:
            registerWindow.text_message.config(text="As senhas digitadas estão diferentes!")
    else:
        registerWindow.text_message.config(text='Por favor, preencha todos os campos!')


loginWindow = LoginWindow(call_main_window)
loginWindow.window.mainloop()