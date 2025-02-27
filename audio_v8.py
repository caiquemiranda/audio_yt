import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - Básico")
        self.root.geometry("400x200")
        
        # Criar interface básica
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # URL entrada
        ttk.Label(frame, text="URL do YouTube:").grid(row=0, column=0, sticky="w")
        self.url_entry = ttk.Entry(frame, width=40)
        self.url_entry.grid(row=1, column=0, pady=5)
        
        # Botão de download
        ttk.Button(frame, text="Baixar Áudio", command=self.download_audio).grid(row=2, column=0, pady=10)
        
        # Label de status
        self.status_label = ttk.Label(frame, text="")
        self.status_label.grid(row=3, column=0, pady=5)
        
    def download_audio(self):
        try:
            url = self.url_entry.get()
            if not url:
                messagebox.showwarning("Aviso", "Por favor, insira uma URL")
                return
                
            self.status_label.config(text="Baixando...")
            self.root.update()
            
            # Download do áudio
            yt = YouTube(url)
            audio = yt.streams.filter(only_audio=True).first()
            out_file = audio.download()
            
            # Renomeia para .mp3
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            
            self.status_label.config(text="Download concluído!")
            messagebox.showinfo("Sucesso", f"Arquivo salvo como:\n{new_file}")
            
        except Exception as e:
            self.status_label.config(text="Erro no download")
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
