FROM python:3.9

COPY lte-signal-exporter.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "pytohn", "./lte-signal-exporter.py" ]