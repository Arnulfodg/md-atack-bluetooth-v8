# md-attack-bluetooth

## Descripción

**md-attack-bluetooth** es una herramienta diseñada para realizar auditorías de seguridad en dispositivos Bluetooth. Su funcionalidad incluye la verificación e instalación de programas necesarios, activación de servicios Bluetooth, escaneo de dispositivos cercanos y la posibilidad de ejecutar un ataque de denegación de servicio (DoS). **Esta herramienta está creada con fines educativos y debe ser utilizada únicamente en entornos controlados y con el consentimiento de los propietarios de los dispositivos.**

## Características

- Verificación automática de la instalación de herramientas necesarias para la auditoría.
- Activación de servicios Bluetooth y SDP si no están activos.
- Escaneo de dispositivos Bluetooth cercanos.
- Posibilidad de enviar imágenes o audios antes de ejecutar el ataque.
- Ejecución de ataques de denegación de servicio (DoS) utilizando múltiples hilos.
- Registro detallado del proceso a través del módulo `logging`.

## Instalación

Para utilizar esta herramienta, primero necesitas clonar el repositorio y ejecutar el programa desde una terminal Linux con privilegios de administrador.

### Requisitos previos

Asegúrate de tener instalados los siguientes paquetes en tu sistema:

- `hcitool`
- `l2ping`
- `sdptool`
- `bluetoothctl`

Si no están instalados, la herramienta los verificará y te pedirá instalarlos de forma automática.

### Instalación del repositorio

```bash
git clone https://github.com/tu-usuario/md-attack-bluetooth.git
cd md-attack-bluetooth

Uso
1. Ejecución del programa

Para ejecutar la herramienta, simplemente corre el archivo main.py con permisos de superusuario:
sudo python3 main.py

2. Funcionalidades principales
Verificación de programas necesarios

El programa comprobará si tienes instalados los paquetes hcitool, l2ping, sdptool y bluetoothctl. Si no están presentes, intentará instalarlos automáticamente.
Activación de servicios Bluetooth y SDP

Se comprobará si el servicio Bluetooth está activado y, en caso contrario, se activará. También verificará la disponibilidad del servidor SDP y lo reiniciará si es necesario.
Escaneo de dispositivos Bluetooth

La herramienta escaneará los dispositivos Bluetooth cercanos y mostrará una lista de ellos, incluyendo la dirección MAC y el nombre del dispositivo.
Ejecución de ataque DoS

El usuario puede seleccionar un dispositivo objetivo y configurar un ataque DoS basado en l2ping. Es posible configurar el tamaño del paquete y la cantidad de hilos utilizados para realizar el ataque.

    Advertencia: El uso indebido de esta herramienta en dispositivos sin autorización es ilegal y va en contra de las buenas prácticas de ciberseguridad.

3. Opcional: Enviar archivo de imagen o audio

Antes de ejecutar el ataque DoS, puedes optar por enviar un archivo de imagen o audio a través de Bluetooth al dispositivo objetivo. Esto es meramente ilustrativo para mostrar cómo la conexión puede ser utilizada con propósitos legítimos antes de un ataque.
Ejemplo de uso

    Ejecuta el programa.
    Permite que verifique e instale los programas necesarios.
    Escanea los dispositivos Bluetooth cercanos.
    Selecciona un dispositivo objetivo.
    (Opcional) Envía un archivo al dispositivo.
    Configura el ataque DoS seleccionando el tamaño del paquete y la cantidad de hilos.
    El ataque DoS se iniciará.

Sistemas Operativos Soportados

Esta herramienta ha sido probada y está diseñada para sistemas operativos de ciberseguridad basados en Linux. Algunos de los sistemas operativos recomendados para su uso incluyen:

    Kali Linux: Una distribución popular para pruebas de penetración y auditorías de seguridad.
    Parrot OS: Otro sistema operativo orientado a ciberseguridad y forense digital.
    BlackArch Linux: Distribución basada en Arch, con un enfoque en pruebas de penetración y seguridad de redes.
    Ubuntu/Debian: También puede ser utilizada en sistemas generales basados en Ubuntu o Debian, siempre que se tenga instalada la suite Bluetooth y herramientas de red adecuadas.

    Nota: Esta herramienta requiere acceso a hardware Bluetooth en el equipo donde se ejecute y privilegios de superusuario para realizar los cambios necesarios en los servicios de Bluetooth y SDP.

Advertencia Legal

El uso de esta herramienta debe ser realizado únicamente en entornos controlados y con el consentimiento explícito de los propietarios de los dispositivos. El mal uso de esta herramienta puede violar leyes locales, nacionales e internacionales, y es responsabilidad del usuario garantizar que se siga un comportamiento ético y legal en todo momento.
Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta herramienta, siéntete libre de hacer un fork del repositorio y enviar tus pull requests. Asegúrate de seguir las buenas prácticas de desarrollo seguro.
Licencia

Este proyecto está bajo la licencia MIT.

¡Gracias por utilizar md-attack-bluetooth!
