import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import *


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

# Executa a aplicação
root.mainloop()
