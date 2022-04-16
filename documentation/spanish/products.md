# Desafío ClicOh

## Products

### Crear un producto
Enviar un POST a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/
```
En el cuerpo del mensaje enviar en formato JSON los siguientes campos:
```json
{
    "name": "Product 30",
    "description": "Product 30 description",
    "price": 300.00,
    "stock": 30
}
```
### Listar productos
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/
```
### Listar un producto
Enviar un GET a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
### Modificar un producto
Enviar un PUT a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
En el cuerpo del mensaje enviar en formato JSON los siguientes campos:
```json
{
    "name": "Product 30",
    "description": "Product 30 description",
    "price": 300.00,
    "stock": 30
}
```
### Borrar un producto
Enviar un DELETE a la URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
