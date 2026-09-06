# Diferencias entre REQUEST-METHODS:

  * *GET*: Utilizado para solicitar leer datos, especificados o no en el request. No modifica el estado.

  * *POST*: Utilizado para crear y añadir, a la vez, nueva información/data.
    No es idempotente porque cada llamada crea un pedido nuevo y cambia valores.

  * *PATCH*: Utilizado para hacer una modificación parcial. Se modifican aquellos campos especificados en el request.

  * *DELETE*: Utilizado para eliminar datos, siempre y cuando existan.
