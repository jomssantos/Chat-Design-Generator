import cairo
from PIL import Image, ImageDraw, ImageFont
import textwrap, math

mensagens = [
    {"remetente": "Você", "texto": "Acho que só vou descansar um pouco haha"},
    {"remetente": "Amigo", "texto": "Entendi! Eu tava pensando em sair, mas não sei pra onde"},
    {"remetente": "Você", "texto": "Podemos ir naquele restaurante novo que abriu no centro!"},
    {"remetente": "Você", "texto": "Acho que só vou descansar um pouco haha"},
    {"remetente": "Amigo", "texto": "Entendi! Eu tava pensando em sair, mas não sei pra onde"},
    {"remetente": "Você", "texto": "Podemos ir naquele restaurante novo que abriu no centro!"},
]

LARGURA = 1000
ALTURA_BASE = 100
MARGEM_LATERAL = 25
ESPACAMENTO = 40
MENSAGEM_MAX_LARGURA = 700
FONTE_TAMANHO = 36
COR_FUNDO = (0, 0, 0)
COR_ENVIADA = (92/255, 68/255, 212/255) 
COR_RECEBIDA = (38/255, 38/255, 38/255) 

def interpolar_cor(y, altura_total, cor_inicial, cor_final):
    fator = y / altura_total 
    r = cor_inicial[0] + fator * (cor_final[0] - cor_inicial[0])
    g = cor_inicial[1] + fator * (cor_final[1] - cor_inicial[1])
    b = cor_inicial[2] + fator * (cor_final[2] - cor_inicial[2])
    return (r, g, b)

def calcular_altura_mensagem(texto):
    linhas = textwrap.wrap(texto, width=30)
    return (len(linhas) * (FONTE_TAMANHO + 10)) + 30



y_atual = ALTURA_BASE
baloes = []

def desenhar_retangulo(context, x, y, largura, altura, cor, cantos):
    radius_top_left, radius_top_right, radius_bottom_left, radius_bottom_right = cantos
    
    context.set_source_rgb(*cor)
    context.new_sub_path()
    context.arc(x + radius_top_left, y + radius_top_left, radius_top_left, math.pi, 1.5 * math.pi)
    context.arc(x + largura - radius_top_right, y + radius_top_right, radius_top_right, 1.5 * math.pi, 0)
    context.arc(x + largura - radius_bottom_right, y + altura - radius_bottom_right, radius_bottom_right, 0, 0.5 * math.pi)
    context.arc(x + radius_bottom_left, y + altura - radius_bottom_left, radius_bottom_left, 0.5 * math.pi, math.pi)
    context.close_path()
    context.fill()

def desenhar_icone(context, img_path, x, y, tamanho):

    icon = Image.open(img_path).convert("RGBA")
    icon = icon.resize((tamanho, tamanho), Image.LANCZOS)

    temp_path = "temp_icon.png"
    icon.save(temp_path, "PNG")

    icon_surface = cairo.ImageSurface.create_from_png(temp_path)

    context.set_source_surface(icon_surface, x, y)
    context.paint()
    import os
    os.remove(temp_path)

dados_rect=[]
for i, msg in enumerate(mensagens):
    cor = COR_ENVIADA if msg["remetente"] == "Você" else COR_RECEBIDA
    x_texto = LARGURA - MARGEM_LATERAL - MENSAGEM_MAX_LARGURA if msg["remetente"] == "Você" else MARGEM_LATERAL
    altura_msg = calcular_altura_mensagem(msg["texto"])
    
    ultima_mensagem=mensagens[i-1] if i > 0 else {}
    proxima_mensagem=mensagens[i+1] if i < (len(mensagens)-1) else {}

    
    anterior= True if ultima_mensagem.get("remetente")==msg["remetente"] else False
    atual=True
    proxima = True if proxima_mensagem.get("remetente")==msg["remetente"] else False

    cantos = [40, 40, 40, 40]
    ESPACAMENTO = 40
    icon=True
    if(anterior and msg["remetente"] == "Amigo"):
        cantos[0] = 10
        icon=False
    if(proxima and msg["remetente"] == "Amigo"):
        cantos[2] = 10
        ESPACAMENTO=9
    if(anterior and msg["remetente"] == "Você"):
        cantos[1] = 10
    if(proxima and msg["remetente"] == "Você"):
        cantos[3] = 10
        ESPACAMENTO=9

    dados_rect.append(
        {
            "cantos":cantos,
            "texto":msg["texto"],
            "espaçamento": ESPACAMENTO,
            "altura_msg": altura_msg,
            "cor": cor,
            "max_largura": MENSAGEM_MAX_LARGURA,
            "x_texto": x_texto,
            "y_atual": y_atual,
            "icon":icon,
        }
    )
    
    y_atual += altura_msg + ESPACAMENTO



altura_total = ALTURA_BASE + sum(calcular_altura_mensagem(d["texto"]) + d["espaçamento"] for d in dados_rect)

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, LARGURA, altura_total)
context = cairo.Context(surface)
context.set_source_rgb(*COR_FUNDO)
context.paint()

COR_ENVIADA_INICIAL = (155/255, 13/255, 189/255)
COR_ENVIADA_FINAL = (16/255, 134/255, 239/255) 

ICON_PATH = "profile_icon.png" 
TAMANHO_ICONE = 70 
ESPACO_ICONE = TAMANHO_ICONE + 10 

for d in dados_rect:

    if d["cor"] == COR_ENVIADA:
        d["cor"] = interpolar_cor(d["y_atual"], altura_total, COR_ENVIADA_INICIAL, COR_ENVIADA_FINAL)
    
    if d["cor"] == COR_RECEBIDA:
        d["x_texto"] += ESPACO_ICONE

    desenhar_retangulo(context, d["x_texto"], d["y_atual"], d["max_largura"], d["altura_msg"], d["cor"], d["cantos"])

    if d["cor"] == COR_RECEBIDA:
        x_icone = d["x_texto"] - ESPACO_ICONE 
        y_icone = d["y_atual"] 
        if(d["icon"]):
            desenhar_icone(context, ICON_PATH, x_icone, y_icone, TAMANHO_ICONE)
    
    baloes.append((d["texto"], d["x_texto"]+ 20, d["y_atual"] + 20, d["max_largura"] - 40,  d["altura_msg"] - 40))

surface.write_to_png("baloes.png")
imagem = Image.open("baloes.png")
draw = ImageDraw.Draw(imagem)


fonte = ImageFont.truetype("Instagram Sans.ttf", FONTE_TAMANHO)
for texto, x, y, largura, altura in baloes:
    linhas = textwrap.wrap(texto, width=30)
    altura_texto = len(linhas) * (FONTE_TAMANHO + 10)
    y_texto = y + (altura - altura_texto) // 2 
    for i, linha in enumerate(linhas):
        draw.text((x, y_texto + i * (FONTE_TAMANHO + 10)), linha, font=fonte, fill=(238, 230, 255))


imagem.save("conversa_final.jpg")
imagem.show()
