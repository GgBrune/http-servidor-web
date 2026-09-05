# importa de la librería la función 'make_server'
from wsgiref.simple_server import make_server # Servidor HTTP incluído en py

    # environ (embiente del pedido) = diccionario con la info de la request
    # start_response = llamada a función con la respuesta
def app(environ, start_response):
    status = "200 OK" # código de estado a retornar
    
    # 'headers' es una colección de elementos - tipo tupla (inumtable)
    headers = [("Content-Type", "text/plain")] # headers de la respuesta
    
    # toma una función como parámetro y la utiliza:
    start_response(status, headers) # Confirmación de status y headers ante el servidor

            # 'b' por bytes
    return [b"Hola"] # cuerpo de la respuesta

    # "app" función que responde cada request 
with make_server("", 9292, app) as server: # guarda el servidor en la variable 'server'
# "with" = manejo seguro de arcivhos    
    print("Listening on http://localhost:9292")
    server.serve_forever() # deja el servidor corriendo indefinidamente