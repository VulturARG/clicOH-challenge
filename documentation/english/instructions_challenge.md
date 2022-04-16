# Challenge Django Rest Framework

## Goal
Analyze the level of knowledge of ClicOh backend developer applicants.

## test logic
Create a REST API using DJANGO REST FRAMEWORK, which provides the following basic and limited functionality of an Ecommerce.

The system must have `Product`, `Order`, `OrderDetail` models with the following attributes:

Products:
- id PK [string]
- name [string]
- price [float]
- stock[int]
 
Order:
- id PK
- date_time [datetime]

OrderDetail:
- order [Order]
- quantity [int]
- product [Product]

It must provide the following end points:
* Register/Edit a product
* Delete a product
* Consult a product
* List all products
* Modify stock of a product
* Register/Edit an order (including its details). You must update the stock of the product
* Delete an order. Restore product stock
* Consult an order and its details
* List all orders

The Order class must expose a `get_total` method which calculates the total of the invoice and returns that value in the serializer
correspondent. You must also expose the `get_total_usd` method, using the API of
https://www.dolarsi.com/api/api.php?type=valoresprincipales, with `dólar blue` so that you get the price in dollars.

When creating or editing an order, validate that there is sufficient stock of the product, if there is no stock, a certificate must be returned.
validation error.

For the API implementation, `ModelViewSet`, `ModelSerializer` should be used.

The source code of the api must be uploaded to a public repository, which must be provided for its correct
examination.

When creating an order, you must validate:
* that the quantity of each product is greater than 0
* that products are not repeated in the same order
* Implement token-based authentication (JWT)
* Deploy the api in production, for example on heroku or https://www.pythonanywhere.com/,
* Implement unit test to validate the endpoints.