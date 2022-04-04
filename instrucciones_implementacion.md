# Desafío ClicOh

## Instalación en entorno de desarrollo

```bash
1) git clone https://github.com/VulturARG/clicOH-challenge.git
2) cd django-personal-porfolio

# Virtualenv instalación (Linux)
3) virtualenv venv
4) source venv/bin/activate

# Virtualenv instalación (Windows)
3) virtualenv venv
4) .\venv\Scripts\activate

5) pip3 install -r requirements.txt
```

### Correr en entorno de desarrollo
```bash
6) python manage.py makemigrations
7) python manage.py migrate
8) python manage.py createsuperuser

# Para correr en desarrollo
python manage.py runserver

# Para configuar la aplicación
http://127.0.0.1:8000/admin
```

## Instalación y puesta en marcha en entorno de producción con Docker
```bash
1) Instalar Docker
2) Instalar Docker Composer

3) sudo git clone https://github.com/VulturARG/django-personal-porfolio.git
4) cd django-personal-porfolio
5) Crear archivo .env (Formato abajo)
6) docker-compose up -d
7) docker-compose exec django_gunicorn python3 manage-prod.py migrate

# Opcional, para rellenar la base de datos con valores precargados
# Si no se ejecuta, saltar al paso 7) Los datos deberan cargarse manualmente desde /admin ANTES de correr la aplicación para que no de error
8) docker-compose exec django_gunicorn python3 manage-prod.py loaddata pre_data.json

9) docker-compose exec django_gunicorn python3 manage-prod.py createsuperuser
```

### Para configurar la aplicación
```bash
http://xxx.xxx.xxx.xxx:8000/admin
```

```bash
## do not put this file under version control!
SECRET_KEY=some_secret_key
API_VERSION=v1/
API_DOLLAR_SI_URL=https://www.dolarsi.com/api/api.php?type=valoresprincipales
API_DOLLAR_SI_USERNAME=
API_DOLLAR_SI_PASSWORD=
ALLOWED_HOSTS_PROD=[]
```

Fuente docker-compose producción
https://youtu.be/vJAfq6Ku4cI

github: (Fork)
https://github.com/VulturARG/django-docker-compose

