import json
from wsgiref.simple_server import make_server

tasks = { # diccionario de 'tasks'
    1: {"id": 1, "title": "Cocinar budín", "done": False},
    2: {"id": 2, "title": "Realizar servidor", "done": True},
}
next_id = 3 # llevar recuento de tareas

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

        elif path == "/tasks/{id}":
            
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

        global next_id # ???

        # Toma la longitud del request
        content_length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        # Lee el cuerpo del request del stream
        body = environ['wsgi.input'].read(content_length)
        data = json.loads(body)

        # Crea la nueva tarea
        new_task = {"is": next_id, "title": data.get("title", ""), "done": data.get("done", False)}
        tasks[next_id] = new_task
        next_id += 1

        response = json.dumps(new_task).encode("utf-8") # Creación de la respuesta
        start_response(status, headers) # Arma la respuesta
        return [response] # Retorna la tarea creada


    elif method == "PATCH" and path == "/tasks/{id}":

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


    elif method == "DELETE" and path == "/tasks/{id}":

        headers = [("Content-Type", "application/json")] # Linea obligatoria
        
        id_string = path[len("/tasks/"):] # Toma el carácter después de la posición 7
        task_id = int(id_string) # Convierte el número string en int

        # Si la tarea existe:
        if task_id in tasks:

            # Si la tarea tiene contenido:
            if tasks[task_id]:
                status = "200 OK" # Defino el estado de la respuesta

                # Elimino la tarea y la guardo en una variable
                task_del = tasks.pop(task_id)

                body = json.dumps(task_del).encode("utf-8") # Creación de la respuesta
                start_response(status, headers) # Arma la respuesta
                return [body] # Retorna la tarea creada

            # Si la tarea está "vacía":
            else:
                status = "204 No Content" # Defino el estado de la respuesta

                start_response(status, headers) # Arma la respuesta
                        # "body"
                return [json.dumps({"NO CONTENT": "Task already empty"}).encode("utf-8")]

        # Si la tarea NO existe:
        else:
            status = "404 Not Found" # Defino el estado de la respuesta
                    
            start_response(status, headers) # Arma la respuesta
                    # "body"
            return [json.dumps({"ERROR": "Task not found"}).encode("utf-8")]

    else:

        headers = [("Content-Type", "application/json")] # Linea obligatoria

        # Si la ruta existe:
        if path == "/tasks" or path == "/tasks/{id}":
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