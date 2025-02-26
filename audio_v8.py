import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from moviepy.editor import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
import re
import os


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    root.update_idletasks()


def mostrar_preview():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL válida")
        return
        
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
        messagebox.showerror("Erro", f"Erro ao carregar preview: {str(e)}")


def limpar_nome_arquivo(nome):
    # Remove caracteres inválidos e limita o comprimento do nome
    nome_limpo = re.sub(r'[\\/*?:"<>|]', '', nome)
    return nome_limpo[:200]  # Limita o tamanho do nome do arquivo


def baixar_e_converter_para_mp3(url):
    temp_file = 'temp_audio'
    try:
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida")
            return
            
        yt = YouTube(url)
        yt.register_on_progress_callback(on_progress)
        video = yt.streams.filter(only_audio=True).first()

        titulo_video = limpar_nome_arquivo(yt.title)
        destino = f"{titulo_video}.mp3"

        # Download do arquivo
        out_file = video.download(filename=temp_file)
        progress_bar['value'] = 100
        root.update_idletasks()

        # Conversão para MP3
        audio_clip = AudioFileClip(temp_file)
        audio_clip.write_audiofile(destino)
        audio_clip.close()

        # Limpa o arquivo temporário
        if os.path.exists(temp_file):
            os.remove(temp_file)

        messagebox.showinfo(
            "Sucesso", f"Áudio baixado e convertido para MP3: {destino}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante o download/conversão: {str(e)}")
    finally:
        # Garante que o arquivo temporário seja removido mesmo em caso de erro
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        progress_bar['value'] = 0  # Reseta a barra de progresso


def iniciar_download_thread():
    url = url_entry.get()
    download_thread = threading.Thread(
        target=baixar_e_converter_para_mp3, args=(url,))
    download_thread.start()


# Configuração da janela
root = tk.Tk()
root.title("Baixador de Áudio do YouTube")
root.geometry("500x300")  # tamanho da janela

style = ttk.Style()
style.theme_use('clam')  # tema

# estilo para os botões
style.configure('TButton', font=('Arial', 10), borderwidth='4')
style.map('TButton', foreground=[('!active', 'black'), ('active', 'white')],
          background=[('!active', 'white'), ('active', 'blue')])

# Frame botões
buttons_frame = tk.Frame(root)
buttons_frame.pack(side='left', padx=10, pady=10)

url_label = tk.Label(buttons_frame, text="Insira a URL do YouTube:")
url_label.pack()

url_entry = tk.Entry(buttons_frame, width=40)
url_entry.pack()

preview_button = ttk.Button(
    buttons_frame, text="Mostrar Preview", command=mostrar_preview)
preview_button.pack(pady=10)

download_button = ttk.Button(
    buttons_frame, text="Baixar Áudio", command=iniciar_download_thread)
download_button.pack(pady=10)

# Frame para o preview e barra de progresso
preview_frame = tk.Frame(root)
preview_frame.pack(side='right', padx=10, pady=10)

preview_label = tk.Label(preview_frame)  # Label para o preview
preview_label.pack()

progress_bar = ttk.Progressbar(
    preview_frame, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=10)

# Executa
root.mainloop()
