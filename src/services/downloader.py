from pytubefix import YouTube
import os
from typing import Callable
import asyncio

class YouTubeDownloader:
    async def get_video_info(self, url: str) -> dict:
        """Obtém informações do vídeo de forma assíncrona"""
        try:
            # Executa a operação bloqueante em uma thread separada
            loop = asyncio.get_event_loop()
            yt = await loop.run_in_executor(None, YouTube, url)
            
            return {
                'title': yt.title,
                'duration': yt.length,
                'thumbnail_url': yt.thumbnail_url
            }
        except Exception as e:
            raise Exception(f"Erro ao obter informações do vídeo: {str(e)}")
    
    def download(self, url: str, output_path: str,
                progress_callback: Callable,
                complete_callback: Callable,
                error_callback: Callable):
        try:
            yt = YouTube(url)
            # Registra callback de progresso
            yt.register_on_progress_callback(
                lambda stream, chunk, bytes_remaining: progress_callback(
                    (1 - bytes_remaining / stream.filesize) * 100
                )
            )
            
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=output_path)
            
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            
            if os.path.exists(new_file):
                os.remove(new_file)
            
            os.rename(out_file, new_file)
            complete_callback(new_file)
            
        except Exception as e:
            error_callback(str(e)) 