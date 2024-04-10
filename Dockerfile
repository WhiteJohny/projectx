FROM PYTHON:3.11

WORKDIR /projectx

COPY requirements.txt /projectx
RUN pip install --upgrade pip && install -r requirements.txt

COPY /projectx /projectx

CMD [ "python", "./main.py" ]