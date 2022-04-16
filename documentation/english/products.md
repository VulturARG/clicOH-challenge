# DeClicOh challenge

## Products

### Create a product
Send POST to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/
```
In the body of the message send an order detail of the form:
```json
{
    "name": "Product 30",
    "description": "Product 30 description",
    "price": 300.00,
    "stock": 30
}
```
### List products
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/
```
### List a product
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
### Modify a product
Send PUT to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
In the body of the message send an order detail of the form:
```json
{
    "name": "Product 30",
    "description": "Product 30 description",
    "price": 300.00,
    "stock": 30
}
```
### Delete a product
Send DELETE to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/products/1/
```
