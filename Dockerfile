FROM python:3.11-slim

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt
RUN pip install --upgrade lxml_html_clean

WORKDIR /app
COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD [ "python", "src/__main__.py" ]