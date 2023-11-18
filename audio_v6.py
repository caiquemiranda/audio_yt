import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from moviepy.editor import *
from PIL import Image, ImageTk
import requests
from io import BytesIO


def mostrar_preview():
    url = url_entry.get()
    try:
        yt = YouTube(url)
        image_url = yt.thumbnail_url
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 200), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        preview_label.configure(image=img)
        preview_label.image = img  # Mantém uma referência
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def baixar_e_converter_para_mp3(url, destino='audio.mp3'):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        audio_clip = AudioFileClip(out_file)
        audio_clip.write_audiofile(destino)
        audio_clip.close()

        messagebox.showinfo(
            "Sucesso", f"Áudio baixado e convertido para MP3: {destino}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def iniciar_download():
    url = url_entry.get()
    baixar_e_converter_para_mp3(url, 'meu_audio.mp3')


root = tk.Tk()
root.title("Baixador de Áudio do YouTube")
root.geometry("500x300")  # Ajusta o tamanho da janela

style = ttk.Style()
style.theme_use('clam')  # Usa um tema moderno

# Configuração de estilo para os botões
style.configure('TButton', font=('Arial', 10), borderwidth='4')
style.map('TButton', foreground=[('!active', 'black'), ('active', 'white')],
          background=[('!active', 'white'), ('active', 'blue')])

# Frame para os botões
buttons_frame = tk.Frame(root)
buttons_frame.pack(side='left', padx=10, pady=10)

preview_button = ttk.Button(buttons_frame, text="Mostrar Preview", command=mostrar_preview)
preview_button.pack(pady=10)

download_button = ttk.Button(buttons_frame, text="Baixar Áudio", command=iniciar_download_thread)
download_button.pack(pady=10)

# Frame para o preview
preview_frame = tk.Frame(root)
preview_frame.pack(side='right', padx=10, pady=10)

preview_label = tk.Label(preview_frame)  # Label para o preview
preview_label.pack()

progress_bar = ttk.Progressbar(preview_frame, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=10)

# Executa a aplicação
root.mainloop()