from machine import Pin
from time import sleep
import network
import socket

ledv = Pin(2, Pin.OUT)#No cambio esto para no confundirme en las decoraciónes :P
ledv.off()
leda = Pin(4, Pin.OUT)
leda.off()
ledr = Pin(5, Pin.OUT)
ledr.off()
bomb = Pin(19, Pin.OUT)
bomb.off()

SSID = "Jacg20991"
PASSWORD = "12345678"

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
sleep(1)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
print("Conectando al Wifi...")

timeout = 10
while not wifi.isconnected() and timeout > 0:
    print("Conectando...")
    ledv.value(1)
    sleep(0.1)
    ledv.value(0)
    leda.value(1)
    sleep(0.1)
    leda.value(0)
    ledr.value(1)
    sleep(0.2)
    ledr.value(0)
    leda.value(1)
    sleep(0.2)
    leda.value(0)
    ledv.value(1)
    sleep(0.1)
    timeout -= 1



ip=wifi.ifconfig()[0]
if ip == "0.0.0.0":
    ledv.value(0)
    print("No conectado :(")
    while True:
        ledr.value(1)
        sleep(0.5)
        ledr.value(0)
        sleep(0.5)
print("Conectado!")
ledv.value(1)
sleep(0.1)
ledv.value(0)
sleep(0.1)
ledv.value(1)
sleep(0.1)
ledv.value(0)
sleep(0.1)
ledv.value(1)
sleep(0.1)
ledv.value(0)
sleep(0.1)
ledv.value(1)
sleep(0.1)
ledv.value(0)
print("IP de la ESP32: " + ip)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 80))

server.listen(5)

print("Servidor Iniciado")
print("Direccion en Web: ")
print("http://" + ip)

while True:
    try:
        conexion, direccion = server.accept()
        conexion.settimeout(2.0)
        print("Cliente conectada")
        print(direccion)
        try:
            solicitud = conexion.recv(1024).decode("utf-8")
        except Exception:
            solicitud = ""
        
        print("solicitud: ")
        print(solicitud)
        
        solicitud_lower = solicitud.lower()
        
        if "get /on" in solicitud_lower:
            bomb.value(1)
            ledv.value(1)
            ledr.value(0)
            print("bombillo encendido")
            respuesta = "Bombillo Encendido"
        elif "get /off" in solicitud_lower:
            bomb.value(0)
            ledv.value(0)
            ledr.value(1)
            print("bombillo apagado")
            respuesta = "Bombillo Apagado"
            
            """
        elif "get /ona" in solicitud_lower:
            leda.value(1)
            print("led amarillo encendido")
            respuesta = "LED Amarillo Encendido"
        elif "get /offa" in solicitud_lower:
            leda.value(0)
            print("led amarillo apagado")
            respuesta = "LED Amarillo Apagado"
        elif "get /onr" in solicitud_lower:
            ledr.value(1)
            print("led rojo encendido")
            respuesta = "LED Rojo Encendido"
        elif "get /offr" in solicitud_lower:
            ledr.value(0)
            print("led rojo apagado")
            respuesta = "LED Rojo Apagado"
            """
            
        else:
            print("Peticion genérica o raíz")
            respuesta = "Servidor ESP32 activo"
        
        
        
        encabezado = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Connection: close\r\n\r\n"
        )
        
        conexion.sendall((encabezado + respuesta).encode("utf-8"))
    except Exception as e:
        print("Error atendido cliente:", e)
    finally:
        conexion.close()
    
