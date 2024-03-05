FROM PYTHON:3.11

WORKDIR /bot

COPY requirements.txt /bot
RUN pip install --upgrade pip && install -r requirements.txt

COPY . /bot

CMD [ "python", "./main.py" ]