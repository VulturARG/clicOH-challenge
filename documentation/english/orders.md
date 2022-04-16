# ClicOh challenge

## Orders

### Create an order
Send POST to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/
```
In the body of the message send an order detail of the form:
```json
{
    "order_detail": [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 1}
    ]
}
```
### List orders
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/
```
### List one order
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
### Modify an order
Send PUT to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
In the body of the message send an order detail of the form:
```json
{
    "order_detail": [
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 1}
    ]
}
```
### Delete an order
Send DELETE to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/
```
### Get total in pesos (ARG)
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/get_total/
```
### Get total in USD
Send GET to URL:
```bash
https://luisbriones.pythonanywhere.com/v1/orders/1/get_total_usd/
```
Because the external API URL is not in the pythonanywhere whitelist, 
making this request from a free account returns an error that the URL cannot be accessed.
This error triggers the OS Error exception, which is caught and returned to the client.
```json
{
    "message": "OS Error"
}
```
More information in [https://www.pythonanywhere.com/forums/topic/14326/](https://www.pythonanywhere.com/forums/topic/14326/)
