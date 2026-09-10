def webpage():
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagina de prueba</title>
        </head>
        <body>
            <h1>Hola mundo!</h1>
        </body>
        </html>
        """
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
    response = webpage()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type text/html\n')
    conn.send('Conecction: close\n\n')
    conn.sendall(response)
    conn.close()