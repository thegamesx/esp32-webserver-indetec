leds = {
    "led1": Pin(12, Pin.OUT),
    "led2": Pin(14, Pin.OUT),
    "led3": Pin(27, Pin.OUT),
}

def webpage():
    html = '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Webserver</title>
    <style>
        html {
            text-align: center;
            font-family: Helvetica;
            background-color: darkgray;
        }
        h1 {
            color: blue;
            padding: 1vh;
        }
        label {
            display: block;
        }
        #boton-enviar {
            background-color: blue;
            border: none;
            color: white;
            padding: 12px 28px;
            text-decoration: none;
            font-size: 18px;
            margin: 2px;
            cursor: pointer;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>ESP32 Webserver</h1>
    <label>
        <input type="checkbox" value="led1" class="led-checkbox" 
        ''' + "checked" if leds['led1'].value() else "" '''>
        LED 1
    </label>
    <br />
    <label>
        <input type="checkbox" value="led2" class="led-checkbox" 
        ''' + "checked" if leds['led2'].value() else "" '''>
        LED 2
    </label>
    <br />
    <label>
        <input type="checkbox" value="led3" class="led-checkbox" 
        ''' + "checked" if leds['led3'].value() else "" '''>
        LED 3
    </label>
    <br />
    <input id="boton-enviar" type="submit" value="Enviar">
    <script>
        document.getElementById('boton-enviar').onclick = (event) => {
            event.preventDefault();

            const checkboxes = document.querySelectorAll('.led-checkbox');
            let ledsSeleccionados= ''

            checkboxes.forEach((checkbox) => {
                if (checkbox.checked) {
                    ledsSeleccionados += checkbox.value + '=1&'
                } else {
                    ledsSeleccionados += checkbox.value + '=0&'
                };
            });
            ledsSeleccionados = ledsSeleccionados.slice(0, -1);

            const url = window.location.href.split('/update?')[0];
            document.location.href = url + '/update?' + ledsSeleccionados;
        }

    </script>
</body>
</html>
        '''
    return html

def obtener_parametros(request):
    try:
        request = request.decode('utf-8')
    except:
        pass

    lineas = request.split(' ')
    linea_correcta = None
    for linea in lineas:
        if '/update?' in linea:
            linea_correcta = linea
            break

    if not linea_correcta:
        return {}
    
    query = linea_correcta.split('/update?', 1)[1]
    parametros = {}
    for par in query.split('&'):
        if '=' in par:
            clave, valor = par.split('=', 1)
            parametros[clave] = valor
    
    return parametros

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f'Entro una conexion desde {str(addr)}')
    request = conn.recv(1024)
    request = str(request)
    print(f'Contenido = {request}')

    parametros = obtener_parametros(request)
    print (parametros)

    for nombre, valor in parametros.items():
        if nombre in leds:
            estado = int(valor)
            leds[nombre].value(estado)
            print(f"{"Prendiendo" if estado else "Apagando"} {nombre}")

    response = webpage()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type text/html\n')
    conn.send('Conecction: close\n\n')
    conn.sendall(response)
    conn.close()