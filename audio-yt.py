# importing packages
import flet as ft
from pytubefix import YouTube
import os
from urllib.parse import urlparse, parse_qs

def main(page: ft.Page):
    # Configurações da página
    page.title = "YouTube Audio Downloader"
    page.window_width = 600
    page.window_height = 400
    page.padding = 30
    page.theme_mode = "light"
    
    # Componentes da interface
    url_input = ft.TextField(
        label="URL do YouTube",
        hint_text="Cole aqui a URL do vídeo",
        width=400,
        autofocus=True
    )
    
    status_text = ft.Text(
        value="",
        color="blue"
    )
    
    progress_bar = ft.ProgressBar(
        width=400,
        visible=False
    )
    
    def validate_url(url):
        """Valida se a URL é do YouTube"""
        try:
            parsed_url = urlparse(url)
            if 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
                return True
        except:
            pass
        return False
    
    def download_audio(e):
        try:
            url = url_input.value
            if not url:
                status_text.value = "Por favor, insira uma URL"
                status_text.color = "red"
                page.update()
                return
                
            if not validate_url(url):
                status_text.value = "URL inválida. Insira uma URL do YouTube"
                status_text.color = "red"
                page.update()
                return
            
            # Mostrar progresso
            progress_bar.visible = True
            status_text.value = "Iniciando download..."
            status_text.color = "blue"
            page.update()
            
            # Download do áudio
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            
            # Definir pasta de downloads
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            
            # Download do arquivo
            out_file = video.download(output_path=downloads_path)
            
            # Converter para MP3
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            
            # Se já existir um arquivo com mesmo nome, remove
            if os.path.exists(new_file):
                os.remove(new_file)
            
            os.rename(out_file, new_file)
            
            # Atualizar status
            status_text.value = "Download concluído com sucesso!"
            status_text.color = "green"
            progress_bar.visible = False
            url_input.value = ""
            page.update()
            
        except Exception as e:
            status_text.value = f"Erro: {str(e)}"
            status_text.color = "red"
            progress_bar.visible = False
            page.update()
    
    # Botão de download
    download_button = ft.ElevatedButton(
        "Baixar Áudio",
        icon=ft.icons.DOWNLOAD,
        on_click=download_audio,
        width=200
    )
    
    # Layout da página
    page.add(
        ft.Column(
            controls=[
                ft.Text("YouTube Audio Downloader", size=30, weight="bold"),
                ft.Text("Baixe áudios do YouTube em MP3", size=16, color="grey"),
                ft.Divider(),
                url_input,
                download_button,
                progress_bar,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

# Iniciar aplicação
if __name__ == "__main__":
    ft.app(target=main)
