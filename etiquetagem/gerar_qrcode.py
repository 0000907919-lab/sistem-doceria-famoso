import qrcode, os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./qrcodes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def gerar_qrcode(codigo, produto, quantidade, validade):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )
    qr.add_data(codigo)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((180, 180))

    etiqueta = Image.new("RGB", (400, 220), "white")
    draw = ImageDraw.Draw(etiqueta)
    etiqueta.paste(qr_img, (10, 20))

    try:
        font_title  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_small  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font_title = font_normal = font_small = ImageFont.load_default()

    x = 205
    draw.text((x, 20),  "DOCERIA FAMOSO",      fill="black",   font=font_title)
    draw.line([(x, 42), (390, 42)],             fill="#cccccc", width=1)
    draw.text((x, 52),  "Produto:",             fill="#888888", font=font_small)
    draw.text((x, 65),  produto,                fill="black",   font=font_normal)
    draw.text((x, 90),  "Lote:",                fill="#888888", font=font_small)
    draw.text((x, 103), codigo,                 fill="black",   font=font_normal)
    draw.text((x, 128), "Qtd:",                 fill="#888888", font=font_small)
    draw.text((x, 141), f"{quantidade} cx",     fill="black",   font=font_normal)
    draw.text((x, 166), "Validade:",            fill="#888888", font=font_small)
    draw.text((x, 179), validade,               fill="black",   font=font_normal)
    draw.text((x,
