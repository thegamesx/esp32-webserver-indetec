led = Pin(12, Pin.OUT)

def webpage():
    if led.value():
        estado = "ON"
    else:
        estado = "OFF"

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagina de prueba</title>
        </head>
        <body>
            <h1>Prender un LED</h1>
            <p>Estado:<strong>{estado}</strong></p>
            <a href="/?led=on"><button>ON</button></a>
            <a href="/?led=off"><button>OFF</button></a>
        </body>
        </html>
        '''
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f'Entro una conexion desde {str(addr)}')
    request = conn.recv(1024)
    request = str(request)
    print(f'Contenido = {request}')

    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on != -1:
        print('Prendimos el LED')
        led.value(1)
    elif led_off != -1:
        print('Apagamos el LED')
        led.value(0)

    response = webpage()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type text/html\n')
    conn.send('Conecction: close\n\n')
    conn.sendall(response)
    conn.close()