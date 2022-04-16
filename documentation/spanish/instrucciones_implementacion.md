# Desafío ClicOh

## Instalación

```bash
git clone https://github.com/VulturARG/clicOH-challenge.git
cd clicOH-challenge
git checkout development

# Virtualenv instalación (Linux)
virtualenv venv
source venv/bin/activate

# Virtualenv instalación (Windows)
virtualenv venv
.\venv\Scripts\activate

pip3 install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

```

### URL Producción

```bash
https://luisbriones.pythonanywhere.com/
```
### Login

```bash
https://luisbriones.pythonanywhere.com/login/
User: clicoh
Password: clicoh
```

Ejemplo de respuesta
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5MTkxMzEyLCJpYXQiOjE2NDkxMDQ5MTIsImp0aSI6IjI1N2NlZGRhOGE5ZjRhMjQ5NTMyMzUxZWVlNThlZjI2IiwidXNlcl9pZCI6N30.ixgQ6yT54m81w9Wy1yNBGG87W0bELmNS0qz1fobLhdM",
    "refresh-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTE5MTMxMiwiaWF0IjoxNjQ5MTA0OTEyLCJqdGkiOiIzODQxYzNlZjFmNGQ0YzE2OWNlMmEyZmNhMGMxZjM5ZiIsInVzZXJfaWQiOjd9.q8PtlnGC1pn3pSbik1auaka0BimsDiIibFmY3wwlyAU",
    "user": {
        "username": "clicoh",
        "email": "clicoh@clicoh.com",
        "name": "clic",
        "last_name": "oh"
    },
    "message": "login successful"
}
```

### Order
Las instrucciones se encuentran en el siguiente [archivo](orders.md)

### Product
Las instrucciones se encuentran en el siguiente [archivo](products.md)

------------------------------------

Se instalaron los siguientes generadores de documentación: 

### Swagger
```bash
https://luisbriones.pythonanywhere.com/swagger/
```
[https://django-rest-swagger.readthedocs.io/en/latest/](https://django-rest-swagger.readthedocs.io/en/latest/)

No funciona en bien en pythonanywhere.com

### Redoc
```bash
https://luisbriones.pythonanywhere.com/redoc/
```
[https://github.com/Redocly/redoc](https://github.com/Redocly/redoc)

No funciona en bien en pythonanywhere.com