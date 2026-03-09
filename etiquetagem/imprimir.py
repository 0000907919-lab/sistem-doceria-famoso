import os
from dotenv import load_dotenv

load_dotenv()

PRINTER_TYPE   = os.getenv("PRINTER_TYPE", "usb")
PRINTER_TARGET = os.getenv("PRINTER_TARGET", "")

def imprimir_etiqueta(caminho_imagem: str) -> bool:
    try:
        from escpos.printer import Usb, Serial, Network

        if PRINTER_TYPE == "usb":
            partes = PRINTER_TARGET.replace("usb://", "").split(":")
            printer = Usb(int(partes[0], 16), int(partes[1], 16))
        elif PRINTER_TYPE == "serial":
            printer = Serial(PRINTER_TARGET)
        elif PRINTER_TYPE == "network":
            printer = Network(PRINTER_TARGET)
        else:
            raise ValueError(f"Tipo desconhecido: {PRINTER_TYPE}")

        printer.set(align="center")
        printer.image(caminho_imagem)
        printer.ln(3)
        printer.cut()
        print(f"🖨️ Etiqueta impressa: {caminho_imagem}")
        return True

    except ImportError:
        print(f"🖨️ [SIMULADO] Imprimiria: {caminho_imagem}")
        return True

    except Exception as e:
        print(f"❌ Erro ao imprimir: {e}")
        return False

def imprimir_lote(codigo: str) -> bool:
    caminho = os.path.join(os.getenv("OUTPUT_DIR", "./qrcodes"), f"{codigo}.png")
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return False
    return imprimir_etiqueta(caminho)
