from pytube import YouTube


def baixar_audio_youtube(url):
    # Cria um objeto YouTube
    yt = YouTube(url)

    # Seleciona o stream com o melhor áudio
    video = yt.streams.filter(only_audio=True).first()

    # Baixa o arquivo
    out_file = video.download()

    print(f"Áudio baixado: {out_file}")


# Substitua com a URL do vídeo do YouTube que você deseja baixar
url_do_video = "https://www.youtube.com/watch?v=t3qniJDJSY8&ab_channel=1%25aCadadiaAudiobookeDesenvolvimento"
baixar_audio_youtube(url_do_video)
