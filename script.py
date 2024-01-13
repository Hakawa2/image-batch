from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

categorias = {}
categoria_atual = None
frases = None

tamanho_da_fonte = 72
fonte = ImageFont.truetype("./font/roboto.ttf", tamanho_da_fonte)

bloco_tamanho = (777.1, 300)  # Tamanho do bloco retangular

def adicionar_texto(imagem, texto, bloco_tamanho, fonte, bloco_retangular=True):
    desenho = ImageDraw.Draw(imagem)

    # Quebra o texto em linhas usando textwrap
    linhas_quebradas = textwrap.wrap(texto, width=20)  # Ajuste a largura conforme necessário

    # Calcula a altura total do bloco retangular com base no número de linhas de texto
    altura_total = sum(desenho.textbbox((0, 0), linha, font=fonte)[3] + 5 for linha in linhas_quebradas)  # Espaço entre as linhas: 5 pixels

    # Posição inicial fixa para o bloco retangular no topo da imagem
    x1 = (imagem.width - bloco_tamanho[0]) // 2
    y1 = 480  # Ajuste conforme necessário
    x2 = x1 + bloco_tamanho[0]
    y2 = y1 + altura_total + 10  # Adiciona espaço extra abaixo do bloco (10 pixels no exemplo)

    # Adiciona o bloco retangular (somente para teste)
    if bloco_retangular:
        cor_bloco = "blue"
        desenho.rectangle([x1, y1, x2, y2], outline=cor_bloco)

    # Adiciona o texto à imagem
    y_atual = y1
    for linha in linhas_quebradas:
        largura_texto, altura_texto = desenho.textbbox((0, 0), linha, font=fonte)[2:4]
        x_texto = x1 + (bloco_tamanho[0] - largura_texto) // 2
        desenho.text((x_texto, y_atual), linha, font=fonte, fill="black")
        y_atual += altura_texto + 5  # Espaço entre as linhas: 5 pixels

    return x1, y1, x2, y2

def gerar_imagem_com_frase(frase, fonte, bloco_tamanho, nome_imagem, pasta_destino, image_model):
    print(image_model)
    modelo = Image.open(f"models/{image_model}.png")
    imagem = modelo.copy()

    adicionar_texto(imagem, frase, bloco_tamanho, fonte, False)
      # Cria o diretório de destino se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Salva a imagem no diretório especificado
    caminho_completo = os.path.join(pasta_destino, f"{nome_imagem}.png")
    imagem.save(caminho_completo)


# Leitura do arquivo de texto com frases
with open("novas-frases.txt", "r", encoding="utf-8") as file:
    for line in file:

        line = line.strip()

        if line.startswith("Categoria"):
            categoria_atual = line
            categorias[categoria_atual] = {}
            categorias[categoria_atual]["Frases"] = []
        elif line.startswith("Modelo"):
            categorias[categoria_atual]["Modelo"] = line.split(":")[1].strip()
        elif line.startswith("Pasta"):
            categorias[categoria_atual]["Pasta"] = line.split(":")[1].strip()
        elif line:
            categorias[categoria_atual]["Frases"].append(line)


# # Gera imagens para cada frase no arquivo
for idx in categorias:
    model = categorias[idx]["Modelo"]
    frases = categorias[idx]["Frases"]
    pasta_destino = f"results/{model}"

    for idx, frase in enumerate(frases):
        nome_imagem = f"imagem_{idx + 1}"
        gerar_imagem_com_frase(frase, fonte, bloco_tamanho, nome_imagem, pasta_destino, model)