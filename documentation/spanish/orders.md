# Desafío ClicOh

## Orders

### Crear un pedido
Enviar un POST a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/
```
En en cuerpo del mensaje enviar un order detail de la forma:
```json
{
    "order_detail": [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 1}
    ]
}
```
### Listar pedidos
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/
```
### Listar un pedido
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
### Modificar un pedido
Enviar un PUT a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
En en cuerpo del mensaje enviar un order detail de la forma:
```json
{
    "order_detail": [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 1}
    ]
}
```
### Borrar un pedido
Enviar un DELETE a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
### Obtener el total en pesos
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/get_total/
```
### Obtener el total en USD
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/get_total_usd/
```
Debido a que la URL de la API externa no está en la whitelist de pythonanywhere, 
al hacer esta petición desde una cuenta gratuita se obtiene un error de que no se puede acceder a la URL.
Dicho error dispara la excepción OS Error, la cual es capturada y devuelta al cliente.
```json
{
    "message": "OS Error"
}
```
Ver en [https://www.pythonanywhere.com/forums/topic/14326/](https://www.pythonanywhere.com/forums/topic/14326/)
