import flet as ft
from pytubefix import YouTube
import os
from urllib.parse import urlparse, parse_qs
import requests
from io import BytesIO
from PIL import Image

def main(page: ft.Page):

    page.title = "YouTube Audio Downloader"
    page.window_width = 800
    page.window_height = 600
    page.padding = 30
    page.theme_mode = "light"
    

    current_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    

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
    

    preview_container = ft.Container(
        width=300,
        height=200,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        padding=10,
        visible=False
    )
    
    # Informações do vídeo
    video_info = ft.Column(
        controls=[
            ft.Text("", size=16, weight="bold", width=300),  # Título
            ft.Text("", size=14, color="grey"),  # Duração
        ],
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
    
    def choose_directory(e):
        """Abre diálogo para escolher pasta de destino"""
        nonlocal current_download_path
        pick_folder_dialog = ft.FilePicker(
            on_result=lambda e: update_download_path(e.path) if e.path else None
        )
        page.overlay.append(pick_folder_dialog)
        page.update()
        pick_folder_dialog.get_directory_path()
        
    def update_download_path(new_path):
        """Atualiza o caminho de download"""
        nonlocal current_download_path
        current_download_path = new_path
        download_path_text.value = f"Pasta: {new_path}"
        page.update()
    
    async def load_preview(e):
        """Carrega preview do vídeo"""
        try:
            url = url_input.value
            if not url or not validate_url(url):
                return
                
            status_text.value = "Carregando informações..."
            status_text.color = "blue"
            page.update()
            
            # Carregar informações do vídeo
            yt = YouTube(url)
            

            video_info.controls[0].value = yt.title
            video_info.controls[1].value = f"Duração: {yt.length//60}:{yt.length%60:02d}"
            

            response = requests.get(yt.thumbnail_url)
            if response.status_code == 200:
                preview_container.content = ft.Image(
                    src=yt.thumbnail_url,
                    width=300,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                )
                
            preview_container.visible = True
            video_info.visible = True
            status_text.value = ""
            page.update()
            
        except Exception as e:
            status_text.value = f"Erro ao carregar preview: {str(e)}"
            status_text.color = "red"
            page.update()
    
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
            

            progress_bar.visible = True
            status_text.value = "Iniciando download..."
            status_text.color = "blue"
            page.update()
            
            # Download do áudio
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()

            out_file = video.download(output_path=current_download_path)
            
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            
            if os.path.exists(new_file):
                os.remove(new_file)
            
            os.rename(out_file, new_file)
            
            status_text.value = "Download concluído com sucesso!"
            status_text.color = "green"
            progress_bar.visible = False
            page.update()
            
        except Exception as e:
            status_text.value = f"Erro: {str(e)}"
            status_text.color = "red"
            progress_bar.visible = False
            page.update()
    
    preview_button = ft.ElevatedButton(
        "Visualizar",
        icon=ft.icons.PREVIEW,
        on_click=load_preview,
        width=150
    )
    
    download_button = ft.ElevatedButton(
        "Baixar Áudio",
        icon=ft.icons.DOWNLOAD,
        on_click=download_audio,
        width=150
    )
    
    choose_folder_button = ft.ElevatedButton(
        "Escolher Pasta",
        icon=ft.icons.FOLDER,
        on_click=choose_directory,
        width=150
    )
    
    download_path_text = ft.Text(f"Pasta: {current_download_path}", size=12, color="grey")
    
    page.add(
        ft.Column(
            controls=[
                ft.Text("YouTube Audio Downloader", size=30, weight="bold"),
                ft.Text("Baixe áudios do YouTube em MP3", size=16, color="grey"),
                ft.Divider(),
                url_input,
                ft.Row(
                    controls=[preview_button, choose_folder_button, download_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                download_path_text,
                progress_bar,
                status_text,
                video_info,
                preview_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
