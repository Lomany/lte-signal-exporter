# lte-signal-exporte

Python app for exporting signal information from Huawei LTE modem

## Usage
Easiest way to launch
```
docker build -t lte-signal-exporter .
docker run -d -e ROUTER_USER=admin -e ROUTER_PASS=changeme -e ROUTER_ADDRESS=192.168.8.1 -e HTTP_PORT=8080 --name lte-signal-exporter lte-signal-exporter
```
or using docker-compose
```
version: '3.9'

services:
  lte-signal-exporter:
    image: lte-signal-exporter
    ports:
    - 8080:8080
    environment:
      ROUTER_USER: admin
      ROUTER_PASS: changeme
      ROUTER_ADDRESS: 192.168.8.1
      HTTP_PORT: 8080
```
