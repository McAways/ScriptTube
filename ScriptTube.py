import yt_dlp
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import threading

# Função para atualizar a barra de progresso durante o download
def progresso_hook(d):
    if d['status'] == 'downloading':
        if 'downloaded_bytes' in d and 'total_bytes' in d and d['total_bytes'] is not None:
            progresso = (d['downloaded_bytes'] / d['total_bytes']) * 100
            barra_progresso["value"] = progresso
            janela.update_idletasks()

# Função para baixar o áudio do YouTube e converter para MP3
def baixar_audio():
    url = entrada_url.get()
    pasta_destino = entrada_pasta.get()
    formato = formato_var.get()
    cookies_file = entrada_cookies.get()

    if not url:
        messagebox.showerror("Erro", "Por favor, insira a URL do vídeo.")
        return

    if not pasta_destino:
        messagebox.showerror("Erro", "Por favor, selecione uma pasta para salvar o arquivo.")
        return

    botao_download.config(state=DISABLED)  # Desativa botão durante o download
    barra_progresso["value"] = 0  # Reseta progresso

    try:
        if formato == "MP3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
                'progress_hooks': [progresso_hook],  # Atualiza a barra de progresso
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:  # MP4
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
                'progress_hooks': [progresso_hook],  # Atualiza a barra de progresso
                'merge_output_format': 'mp4',
            }

        if cookies_file:
            ydl_opts['cookiefile'] = cookies_file
        else:
            ydl_opts['cookiesfrombrowser'] = ['chrome', 'firefox']

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Sucesso", f"Download concluído!\nArquivo salvo em: {pasta_destino}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o {formato.lower()}:\n{e}")

    botao_download.config(state=NORMAL)  # Reativa botão após o download

# Função para executar o download em uma thread separada
def iniciar_download():
    thread = threading.Thread(target=baixar_audio)
    thread.start()

# Função para escolher a pasta de destino
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    entrada_pasta.delete(0, ttk.END)
    entrada_pasta.insert(0, pasta)

# Criando a janela principal com tema escuro
janela = ttk.Window(themename="darkly")
janela.title("YouTube Downloader")
janela.geometry("500x450")
janela.iconbitmap("icons8-download-64.ico")
janela.resizable(False, False)

# Centralizar a janela
largura_janela = 500
altura_janela = 350
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Estilo de Fonte e Cores
fonte_padrao = ("Arial", 12)

# Título
titulo = ttk.Label(janela, text="YouTube Downloader", font=("Arial", 16, "bold"), bootstyle="primary")
titulo.pack(pady=10)

# Campo da URL
frame_url = ttk.Frame(janela)
frame_url.pack(pady=5)
ttk.Label(frame_url, text="URL do Vídeo:", font=fonte_padrao, bootstyle="light").pack(side=LEFT, padx=5)
entrada_url = ttk.Entry(frame_url, width=50)
entrada_url.pack(side=LEFT, padx=5)

# Seleção da pasta de destino
frame_pasta = ttk.Frame(janela)
frame_pasta.pack(pady=5)
ttk.Label(frame_pasta, text="Pasta de Salvamento:", font=fonte_padrao, bootstyle="light").pack(side=LEFT, padx=5)
entrada_pasta = ttk.Entry(frame_pasta, width=40)
entrada_pasta.pack(side=LEFT, padx=5)
botao_pasta = ttk.Button(frame_pasta, text="📁", command=selecionar_pasta, bootstyle="secondary")
botao_pasta.pack(side=LEFT, padx=5)

# Seleção do formato
frame_formato = ttk.Frame(janela)
frame_formato.pack(pady=5)
ttk.Label(frame_formato, text="Formato:", font=fonte_padrao, bootstyle="light").pack(side=LEFT, padx=5)
formato_var = ttk.StringVar(value="MP3")
combobox_formato = ttk.Combobox(frame_formato, textvariable=formato_var, values=["MP3", "MP4"], state="readonly", width=10)
combobox_formato.pack(side=LEFT, padx=5)

# Seleção do arquivo de cookies (opcional)
frame_cookies = ttk.Frame(janela)
frame_cookies.pack(pady=5)
ttk.Label(frame_cookies, text="Arquivo de Cookies (opcional):", font=fonte_padrao, bootstyle="light").pack(side=LEFT, padx=5)
entrada_cookies = ttk.Entry(frame_cookies, width=30)
entrada_cookies.pack(side=LEFT, padx=5)
botao_cookies = ttk.Button(frame_cookies, text="📁", command=lambda: entrada_cookies.delete(0, ttk.END) or entrada_cookies.insert(0, filedialog.askopenfilename()))
botao_cookies.pack(side=LEFT, padx=5)

# Barra de progresso
barra_progresso = ttk.Progressbar(janela, length=400, mode='determinate', bootstyle="success")
barra_progresso.pack(pady=10)

# Botão de Download
botao_download = ttk.Button(janela, text="Baixar", command=iniciar_download, bootstyle="success", width=20)
botao_download.pack(pady=10)

# Rodar a interface
janela.mainloop()
