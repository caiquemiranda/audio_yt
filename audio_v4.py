import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from moviepy.editor import *
from PIL import Image, ImageTk
import requests
from io import BytesIO


def mostrar_preview(url):
    try:
        yt = YouTube(url)
        image_url = yt.thumbnail_url
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        preview_label.configure(image=img)
        preview_label.image = img  # Mantém uma referência
        preview_label.pack()
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def baixar_e_converter_para_mp3(url, destino='audio.mp3'):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        # Configura o callback do progresso
        video.download(filename='temp_audio')

        audio_clip = AudioFileClip('temp_audio')
        audio_clip.write_audiofile(destino)
        audio_clip.close()

        messagebox.showinfo(
            "Sucesso", f"Áudio baixado e convertido para MP3: {destino}")
        progress_bar['value'] = 0
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        progress_bar['value'] = 0


def iniciar_download():
    url = url_entry.get()
    mostrar_preview(url)
    baixar_e_converter_para_mp3(url, 'meu_audio.mp3')


# Configuração da janela
root = tk.Tk()
root.title("Baixador de Áudio do YouTube")

# Criação dos widgets
url_label = tk.Label(root, text="Insira a URL do YouTube:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

download_button = tk.Button(
    root, text="Baixar Áudio", command=iniciar_download)
download_button.pack()

preview_label = tk.Label(root)  # Label para o preview
progress_bar = ttk.Progressbar(
    root, orient='horizontal', length=200, mode='determinate')
progress_bar.pack()

# Executa a aplicação
root.mainloop()
