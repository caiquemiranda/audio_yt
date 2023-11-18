from pytube import YouTube
from moviepy.editor import *


def baixar_e_converter_para_mp3(url, destino='audio.mp3'):
    # Cria um objeto YouTube
    yt = YouTube(url)

    # Seleciona o stream com o melhor áudio
    video = yt.streams.filter(only_audio=True).first()

    # Baixa o arquivo
    out_file = video.download()

    print(f"Áudio baixado: {out_file}")

    # Carrega o arquivo baixado com moviepy
    audio_clip = AudioFileClip(out_file)

    # Converte e salva como MP3
    audio_clip.write_audiofile(destino)

    # Fecha o clip para liberar recursos
    audio_clip.close()

    print(f"Áudio convertido para MP3 e salvo como: {destino}")


# Substitua com a URL do vídeo do YouTube que você deseja baixar
url_do_video = "https://www.youtube.com/watch?v=-Ysp2zQmUqE&list=PL3a0BI4HY_TBdln-tdYZnJSDKWH_Lcyv_&index=1&t=425s&ab_channel=ProjetoVentura"
baixar_e_converter_para_mp3(url_do_video, 'meu_audio.mp3')
