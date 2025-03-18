# Primer borrador de la aplicación

## Instalación

1. Nos bajamos el repositorio
2. Creamos una variable de entorno con python de la siguiente forma:

```bash
$ python3 -m venv .myenv
$ source .myenv/bin/activate
```

3. Instalamos las librerias necesarias con el siguiente comando:

```bash
$ pip install -r requirements.txt
```

4. Ejecutamos el comando para desplegar la aplicación en local de la siguinte forma:

```bash
$ python3 -m streamlit run ./app.py
```