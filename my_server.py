import json
from wsgiref.simple_server import make_server

tasks = { # Diccionario de 'tasks'
    1: {"id": 1, "title": "Cocinar budín", "done": False},
    2: {"id": 2, "title": "Realizar servidor", "done": True},
}
next_id = 3 # Llevar recuento de tareas

    # environ = diccionario con la info del request
    # start_response = función para mandar el status y los headers
def app(environ, start_response):

    method = environ.get('REQUEST_METHOD') # qué VERBO llegó
    path = environ.get('PATH_INFO') # qué RUTA llegó


    if method == "GET":

        headers = [("Content-Type", "application/json")] # Linea obligatoria

        if path == "/tasks":
        
            status = "200 OK" # Defino el estado de la respuesta

                    # 'dumps' = función json para responder
            body = json.dumps(list(tasks.values())).encode("utf-8") # Creación de la respuesta
                                                # 'encode' = convierte string en bytes
            start_response(status, headers) # Arma la respuesta
            return [body] # Retorna las tareas

        elif path.startswith("/tasks/"): # Compara si empieza con ese string y hay 'algo' después
            
            id_string = path[len("/tasks/"):] # Toma el carácter después de la posición 7
            task_id = int(id_string) # Convierte el número string en int

            # Si la tarea existe:
            if task_id in tasks:
                status = "200 OK" # Defino el estado de la respuesta

                            # 'dumps' = función json para responder
                body = json.dumps(tasks[task_id]).encode("utf-8") # Creación de la respuesta
                                                        # 'encode' = convierte string en bytes
                start_response(status, headers) # Arma la respuesta
                return [body] # Retorna la tarea

            # Si la tarea NO existe:
            else:
                status = "404 Not Found" # Defino el estado de la respuesta

                start_response(status, headers) # Arma la respuesta
                        # "body"
                return [json.dumps({"ERROR": "Task not found"}).encode("utf-8")]

    elif method == "POST" and path == "/tasks":

        status = "201 Created" # Defino el estado de la respuesta
        headers = [("Content-Type", "application/json")] # Linea obligatoria

        global next_id

        # Toma la longitud del request
        content_length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        # Lee el cuerpo del request del stream
        body = environ['wsgi.input'].read(content_length)
        data = json.loads(body)

        # Crea la nueva tarea
        new_task = {"id": next_id, "title": data.get("title", ""), "done": data.get("done", False)}
        tasks[next_id] = new_task
        next_id += 1

        response = json.dumps(new_task).encode("utf-8") # Creación de la respuesta
        start_response(status, headers) # Arma la respuesta
        return [response] # Retorna la tarea creada

    elif method == "PATCH" and path.startswith("/tasks/"):

        headers = [("Content-Type", "application/json")] # Linea obligatoria

        id_string = path[len("/tasks/"):] # Toma el carácter después de la posición 7
        task_id = int(id_string) # Convierte el número string en int

        # Si la tarea existe:
        if task_id in tasks:
            status = "200 OK" # Defino el estado de la respuesta

            # Toma la longitud del request
            content_length = int(environ.get('CONTENT_LENGTH', 0) or 0)
            # Lee el cuerpo del request del stream
            body = environ['wsgi.input'].read(content_length)
            data = json.loads(body)

            # Actualiza el campo
            tasks[task_id].update(data)

            response = json.dumps(tasks[task_id]).encode("utf-8") # Creación de la respuesta
            start_response(status, headers) # Arma la respuesta
            return [response] # Retorna la tarea creada

        # Si la tarea NO existe:
        else:
            status = "404 Not Found" # Defino el estado de la respuesta
        
            start_response(status, headers) # Arma la respuesta
                    # "body"
            return [json.dumps({"ERROR": "Task not found"}).encode("utf-8")]

    elif method == "DELETE" and path.startswith("/tasks/"):

        headers = [("Content-Type", "application/json")] # Linea obligatoria
        
        id_string = path[len("/tasks/"):] # Toma el carácter después de la posición 7
        task_id = int(id_string) # Convierte el número string en int

        # Si la tarea existe:
        if task_id in tasks:
                tasks.pop(task_id) # Elimino la tarea

                status = "204 No Content" # Defino el estado de la respuesta
                start_response(status, headers) # Arma la respuesta
                        # "body"
                return [json.dumps({"SUCCESS": "Task deleted"}).encode("utf-8")]

        # Si la tarea NO existe:
        else:
            status = "404 Not Found" # Defino el estado de la respuesta
                    
            start_response(status, headers) # Arma la respuesta
                    # "body"
            return [json.dumps({"ERROR": "Task not found"}).encode("utf-8")]

    else:

        headers = [("Content-Type", "application/json")] # Linea obligatoria

        # Si la ruta existe:
        if path == "/tasks" or path.startswith("/tasks/"):
            status = "405 Method Not Allowed" # Defino el estado de la respuesta

            start_response(status, headers) # Arma la respuesta
                    # "body"
            return [json.dumps({"ERROR": "Wrong method"}).encode("utf-8")]

        # Si la ruta NO existe:
        else:
            status = "404 Not Found" # Defino el estado de la respuesta
                                
            start_response(status, headers) # Arma la respuesta
                    # "body"
            return [json.dumps({"ERROR": "Wrong request"}).encode("utf-8")]


with make_server("", 9292, app) as server: # Guarda el servidor en la variable 'server'
# "with" = manejo seguro de archivos
 
    print("Listening on http://localhost:9292")
    server.serve_forever() # Deja el servidor corriendo indefinidamente