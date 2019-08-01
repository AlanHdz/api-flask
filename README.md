# Flask RESTful API Example

API creada en el framework Flask con autenticación de usuarios y migraciones, utilizando SQLAlchemy. Algunas carateristicas, que podras encontrar es:

- Retornar status code y headers
- Crear recursos usando peticiones POST
- Pruebas unitarias de los modelos y peticiones

## Guía de instalación

** Clonar repositorio **
```
$ git clone https://github.com/AlanHdz/api-flask.git
$ cd api-flask
```

** Crear virtualenv **
```
> $ virtualenv env
```

** Instalar las dependencias **
```
> $ pip install -r requirements.txt
```

** Correr aplicación **
Nota: No te olvides de configurar tu base de datos en el archivo config.py
```
> $ python manage.py runserver
```

## Test
```
> $ python manage.py test
```