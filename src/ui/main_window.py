import flet as ft
from .components import create_preview_container, create_video_info
from services.downloader import YouTubeDownloader
from services.validator import URLValidator
from utils.helpers import get_default_download_path

class MainWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.downloader = YouTubeDownloader()
        self.current_download_path = get_default_download_path()
        self.setup_ui()
        
    def setup_page(self):
        self.page.title = "YouTube Audio Downloader"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.padding = 30
        self.page.theme_mode = "light"
        
    def setup_ui(self):
        # Componentes principais
        self.url_input = ft.TextField(
            label="URL do YouTube",
            hint_text="Cole aqui a URL do vídeo",
            width=400,
            autofocus=True
        )
        
        self.status_text = ft.Text(value="", color="blue")
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        
        self.preview_container = create_preview_container()
        self.video_info = create_video_info()
        
        # Botões
        self.preview_button = ft.ElevatedButton(
            "Visualizar",
            icon=ft.icons.PREVIEW,
            on_click=self.load_preview,
            width=150
        )
        
        self.download_button = ft.ElevatedButton(
            "Baixar Áudio",
            icon=ft.icons.DOWNLOAD,
            on_click=self.start_download,
            width=150
        )
        
        self.choose_folder_button = ft.ElevatedButton(
            "Escolher Pasta",
            icon=ft.icons.FOLDER,
            on_click=self.choose_directory,
            width=150
        )
        
        self.download_path_text = ft.Text(
            f"Pasta: {self.current_download_path}",
            size=12,
            color="grey"
        )
        
        self.create_layout()
    
    def create_layout(self):
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("YouTube Audio Downloader", size=30, weight="bold"),
                    ft.Text("Baixe áudios do YouTube em MP3", size=16, color="grey"),
                    ft.Divider(),
                    self.url_input,
                    ft.Row(
                        controls=[
                            self.preview_button,
                            self.choose_folder_button,
                            self.download_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.download_path_text,
                    self.progress_bar,
                    self.status_text,
                    self.video_info,
                    self.preview_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
    
    async def load_preview(self, e):
        url = self.url_input.value
        if not URLValidator.is_valid_youtube_url(url):
            self.show_error("URL inválida")
            return
            
        try:
            self.status_text.value = "Carregando informações..."
            self.page.update()
            
            video_info = await self.downloader.get_video_info(url)
            self.update_preview(video_info)
            
        except Exception as e:
            self.show_error(f"Erro ao carregar preview: {str(e)}")
    
    def start_download(self, e):
        url = self.url_input.value
        if not URLValidator.is_valid_youtube_url(url):
            self.show_error("URL inválida")
            return
            
        self.downloader.download(
            url,
            self.current_download_path,
            self.update_progress,
            self.download_complete,
            self.show_error
        )
    
    def update_progress(self, progress):
        self.progress_bar.visible = True
        self.progress_bar.value = progress
        self.status_text.value = f"Baixando... {progress:.1f}%"
        self.page.update()
    
    def download_complete(self, file_path):
        self.status_text.value = "Download concluído com sucesso!"
        self.status_text.color = "green"
        self.progress_bar.visible = False
        self.page.update()
    
    def show_error(self, message):
        self.status_text.value = message
        self.status_text.color = "red"
        self.progress_bar.visible = False
        self.page.update()

    def choose_directory(self, e):
        """Abre diálogo para escolher pasta de destino"""
        pick_folder_dialog = ft.FilePicker(
            on_result=lambda e: self.update_download_path(e.path) if e.path else None
        )
        self.page.overlay.append(pick_folder_dialog)
        self.page.update()
        pick_folder_dialog.get_directory_path()
        
    def update_download_path(self, new_path):
        """Atualiza o caminho de download"""
        if new_path:
            self.current_download_path = new_path
            self.download_path_text.value = f"Pasta: {new_path}"
            self.page.update()

    def update_preview(self, video_info: dict):
        """Atualiza o preview do vídeo"""
        try:
            # Atualiza título e duração
            self.video_info.controls[0].value = video_info['title']
            duration_min = video_info['duration'] // 60
            duration_sec = video_info['duration'] % 60
            self.video_info.controls[1].value = f"Duração: {duration_min}:{duration_sec:02d}"
            
            # Atualiza thumbnail
            self.preview_container.content = ft.Image(
                src=video_info['thumbnail_url'],
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            )
            
            self.preview_container.visible = True
            self.video_info.visible = True
            self.status_text.value = ""
            self.page.update()
            
        except Exception as e:
            self.show_error(f"Erro ao atualizar preview: {str(e)}") 