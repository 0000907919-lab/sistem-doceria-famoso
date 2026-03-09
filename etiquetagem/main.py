import argparse
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="🍌 Doceria Famoso — Etiquetagem")
sub = parser.add_subparsers(dest="comando")

p_gerar = sub.add_parser("gerar", help="Gera QR Code de um lote")
p_gerar.add_argument("--codigo",     required=True)
p_gerar.add_argument("--produto",    required=True)
p_gerar.add_argument("--quantidade", required=True, type=int)
p_gerar.add_argument("--validade",   required=True)

p_imprimir = sub.add_parser("imprimir", help="Imprime etiqueta já gerada")
p_imprimir.add_argument("--codigo", required=True)

p_gi = sub.add_parser("gerar-imprimir", help="Gera e imprime em um comando")
p_gi.add_argument("--codigo",     required=True)
p_gi.add_argument("--produto",    required=True)
p_gi.add_argument("--quantidade", required=True, type=int)
p_gi.add_argument("--validade",   required=True)

sub.add_parser("listener", help="Inicia listener MQTT para impressão automática")

args = parser.parse_args()

if args.comando == "gerar":
    from gerar_qrcode import gerar_qrcode
    gerar_qrcode(args.codigo, args.produto, args.quantidade, args.validade)

elif args.comando == "imprimir":
    from imprimir import imprimir_lote
    imprimir_lote(args.codigo)

elif args.comando == "gerar-imprimir":
    from gerar_qrcode import gerar_qrcode
    from imprimir import imprimir_etiqueta
    caminho = gerar_qrcode(args.codigo, args.produto, args.quantidade, args.validade)
    imprimir_etiqueta(caminho)

elif args.comando == "listener":
    from mqtt_listener import iniciar
    iniciar()

else:
    parser.print_help()
