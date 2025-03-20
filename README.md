# Arkham Med

> La IA que la medicina merece y necesita

## Instalación

Esta aplicación se puede ejecutar desde una terminal actualmente a través de un IDE o en una terminal nativa de bash.

1. Nos bajamos el repositorio

```bash
$ git clone <nombre del repositorio>
```

2. Creamos una variable de entorno con python de la siguiente forma:

```bash
$ python3 -m venv .myenv
$ source .myenv/bin/activate
```

3. Instalamos las librerias necesarias con el siguiente comando:

```bash
$ pip install -r requirements.txt
```

4. Debemos añadir las API keys válidas en el archivo `/core/config.py` del proyecto para que se realicen las llamadas a los modelos de forma correcta

(Podéis comprobar a qué modelos se llaman en el archivo `/core/chatbots.py` y cambiarlos a gusto)

5. Ejecutamos el comando para desplegar la aplicación en local de la siguiente forma:

```bash
$ python3 -m streamlit run ./app.py
```

## Presentación

![Enlace a la presentación en canva](https://www.canva.com/design/DAGiKRLITfw/TFLIXql0msxDvrfhftrYyQ/edit?utm_content=DAGiKRLITfw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
