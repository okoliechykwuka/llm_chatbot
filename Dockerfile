FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["panel", "serve", "/code/chatbot.py", "--address", "0.0.0.0", "--port", "7860", "--allow-websocket-origin", "chukypedro-chatbot.hf.space",  "--allow-websocket-origin", "0.0.0.0:7860"]

RUN mkdir /.cache
RUN chmod 777 /.cache