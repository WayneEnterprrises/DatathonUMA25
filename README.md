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
$ pip install streamlit transformers pillow torch openai
```

4. Ejecutamos el comando para desplegar la aplicación en local de la siguinte forma:

```bash
$ python3 -m streamlit run ./app.py
```

## To-do list

- [ ] Arreglar fallos simples de flujo de ejecución (MVC model)
- [ ] Iniciar desarrollo de pipelines entre LLMs
- [ ] Investigar sobre generación de gráficas y contenido no textual para mayor riqueza en las respuestas
- [x] Base de datos con los chats (usuarios y autenticación)
