FROM python:3.6

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . /workspace

RUN echo "Asia/SaiGon" > /etc/timezone

CMD [ "python", "/workspace/main.py" ]