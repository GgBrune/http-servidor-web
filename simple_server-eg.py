from wsgiref.simple_server import make_server # Servidor HTTP incluído en py

    # environ = diccionario con la info de la request
    # start_response = llamada a función con la respuesta
def app(environ, start_response):
    status = "200 OK" # Código de estado a retornar
    headers = [("Content-Type", "text/plain")] # Headers de la respuesta
    start_response(status, headers) # Confirmación de status y headers ante el servidor

            # 'b' por bytes
    return [b"Hola"] # Cuerpo de la respuesta

    # "app" función que maneja cada request 
with make_server("", 9292, app) as server: # Crea el servidor en el puerto '9292'
    print("Listening on http://localhost:9292")
    server.serve_forever() # Deja el servidor corriendo indefinidamente