import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if hasattr(Image, "Resampling"):
    FILTRO_REDIMENSIONAMENTO = Image.Resampling.LANCZOS
else:
    FILTRO_REDIMENSIONAMENTO = getattr(Image, "LANCZOS", 1)


def descobrir_executavel_godot():
    godot_dir = os.path.join(BASE_DIR, "godot")
    if not os.path.isdir(godot_dir):
        return None

    for nome in sorted(os.listdir(godot_dir)):
        if nome.startswith("."):
            continue
        caminho = os.path.join(godot_dir, nome)
        if os.path.isfile(caminho):
            return caminho
    return None


GODOT_EXECUTAVEL = descobrir_executavel_godot()


# Descobre automaticamente até 7 jogos a partir das subpastas de 'jogos/'
def descobrir_jogos():
    jogos_dir = os.path.join(BASE_DIR, "jogos")
    imagens_dir = os.path.join(BASE_DIR, "imagens")
    if not os.path.isdir(jogos_dir):
        print(f"Diretório '{jogos_dir}' não encontrado.")
        return []
    subpastas = [nome for nome in os.listdir(jogos_dir)
                 if os.path.isdir(os.path.join(jogos_dir, nome))]
    subpastas.sort()
    if len(subpastas) > 7:
        print("Aviso: Mais de 7 jogos encontrados. Apenas os 7 primeiros (ordem alfabética) serão exibidos.")
    jogos = []
    for nome in subpastas[:7]:
        caminho = os.path.join(jogos_dir, nome)
        imgfile = os.path.join(imagens_dir, f"{nome}.png")
        jogos.append((nome, caminho, imgfile))
    return jogos

jogos = descobrir_jogos()

# Imagem do evento (para a posição 8 do grid)
evento_img = os.path.join(BASE_DIR, "imagens", "evento.png")

def fechar_greenfoot():
    try:
        # mata qualquer processo chamado "greenfoot"
        subprocess.run(["pkill", "-f", "greenfoot"], check=False)
    except Exception as e:
        print("Erro ao fechar Greenfoot:", e)
    if GODOT_EXECUTAVEL:
        try:
            # mata processos com o nome do executável encontrado em godot/
            subprocess.run(["pkill", "-f", os.path.basename(GODOT_EXECUTAVEL)], check=False)
        except Exception as e:
            print("Erro ao fechar Godot:", e)


def abrir_jogo(caminho):
    fechar_greenfoot()
    if "godot" in caminho:
        if not GODOT_EXECUTAVEL:
            messagebox.showerror(
                "Executável da Godot não encontrado",
                "Nenhum arquivo foi encontrado na pasta 'godot/'.\n"
                "Baixe o executável da Godot e coloque-o nessa pasta."
            )
            return
        subprocess.Popen([GODOT_EXECUTAVEL, "--path", caminho])
    else:
        subprocess.Popen(["greenfoot", caminho])

def restaurar_jogos():

    try:
        for nome, caminho, _ in jogos:
            if os.path.isdir(caminho):
                    subprocess.run(["git", "-C", caminho, "checkout", "."], check=True)        
        # informa, na interface gráfica, que os jogos foram restaurados
        messagebox.showinfo(None, "Versões base dos jogos foram restauradas!")
    except Exception as e:
        messagebox.showinfo(None, "Ops... algo de errado não está certo!", icon="warning")
    

# --- Janela principal
root = tk.Tk()
root.title("Oficina de Programação de Jogos")

# Fundo preto na janela principal
root.configure(bg="black")

# Forçar fullscreen
root.attributes("-fullscreen", True)

# Detecta resolução da tela
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Divide o espaço em 2 linhas x 4 colunas
cell_w = screen_w // 4 - 40   # margem
cell_h = (screen_h - 100) // 2 - 40   # desconta título
IMG_SIZE = (min(cell_w, cell_h), min(cell_w, cell_h))

# Frame para título e botão no topo
top_frame = tk.Frame(root, bg="black")
top_frame.pack(fill="x", pady=(20, 0))

# Título alinhado à esquerda
titulo = tk.Label(
    top_frame,
    text="Oficina de Programação de Jogos",
    font=("Arial", 36, "bold"),
    bg="black",
    fg="white"
)
titulo.pack(side="top", padx=(20, 0))

# Botão restaurar alinhado à direita
btn_restaurar = tk.Button(
    top_frame,
    text="Restaurar Jogos",
    font=("Arial", 12, "bold"),
    bg="#222",
    fg="white",
    command=restaurar_jogos
)
btn_restaurar.pack(side="right", padx=(0, 20), ipadx=10, ipady=4)

# Frame principal para os botões (fundo preto)
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill="both")

# Lista para segurar referências às imagens
imagens_tk = []

# Criar os 7 jogos
for i, (nome, caminho, imgfile) in enumerate(jogos):
    try:
        img = Image.open(imgfile).resize(IMG_SIZE, FILTRO_REDIMENSIONAMENTO)
        tk_img = ImageTk.PhotoImage(img)
        imagens_tk.append(tk_img)
        btn = tk.Button(
            frame,
            image=tk_img,
            compound="top",
            font=("Arial", 14),
            command=lambda c=caminho: abrir_jogo(c)
        )
    except Exception as e:
        print(
            f"Aviso: não foi possível carregar a imagem do jogo '{nome}' ({imgfile}). "
            f"Erro: {e}. Será exibido apenas o nome do jogo."
        )
        btn = tk.Button(
            frame,
            text=nome,
            font=("Arial", 16, "bold"),
            bg="#333",
            fg="white",
            command=lambda c=caminho: abrir_jogo(c)
        )
    btn.grid(row=i//4, column=i%4, padx=20, pady=20, sticky="nsew")

# Adiciona o "cartaz do evento" na posição 8 (linha 1, col 3)
try:
    img = Image.open(evento_img).resize(IMG_SIZE, FILTRO_REDIMENSIONAMENTO)
    tk_img = ImageTk.PhotoImage(img)
    imagens_tk.append(tk_img)
    lbl = tk.Label(frame, image=tk_img, compound="top", font=("Arial", 14, "bold"))
    lbl.grid(row=1, column=3, padx=20, pady=20, sticky="nsew")
except Exception as e:
    print(f"Erro carregando {evento_img}: {e}")

# Ajusta o grid para expandir
for r in range(2):
    frame.rowconfigure(r, weight=1)
for c in range(4):
    frame.columnconfigure(c, weight=1)

# Atalho para sair com ESC
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()