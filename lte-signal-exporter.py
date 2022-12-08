from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Client import Client


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(prometheusExporter().encode())


def prometheusExporter():
    # Auth to router
    connection = AuthorizedConnection('http://' + os.environ['ROUTER_USER'] + ':' + os.environ['ROUTER_PASS'] + '@' + os.environ['ROUTER_ADDRESS'] + '/')
    # Init Client
    client = Client(connection)

    # Common attributes
    device = 'deviceName="' + client.device.information().get('DeviceName') + \
        '",iccid="' + client.device.information().get('Iccid') + '"'
    band = client.device.signal().get('band')
    deviceband = device
    if band is not None:
        deviceband = device + ',band="' + band + '"'

    # Get signal attributes
    signal = {
        'band': {'help': 'The signal band the LTE connection is using', 'type': 'gauge', 'device': device, 'value': band},
        'rsrp': {'help': 'The average power received from a single Reference signal in dBm', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('rsrp')},
        'rsrq': {'help': 'Indicates quality of the received signal in db', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('rsrq')},
        'rssi': {'help': 'Represents the entire received power including the wanted power from the serving cell as well as all co-channel power and other sources of noise in dBm', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('rssi')},
        'rscp': {'help': 'Denotes the power measured by a receiver on a particular physical communication channel in dBm', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('rscp')},
        'sinr': {'help': 'The signal-to-noise ratio of the given signal in dB', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('sinr')},
        'ecio': {'help': 'The EC/IO is a measure of the quality/cleanliness of the signal from the tower to the modem and indicates the signal-to noise ratio in dB', 'type': 'gauge', 'device': deviceband, 'value': client.device.signal().get('ecio')}
    }

    # Format for metric
    for attribute, info in signal.items():
        if info['value'] is not None:
            info['value'] = info['value'].replace("dBm", "")
            info['value'] = info['value'].replace("dB", "")
            info['value'] = info['value'].replace(">=", "")

    # Format data for prometheus
    response = []
    for attribute, info in signal.items():
        if attribute is not None and info['value'] is not None:
            response.append('#HELP ' + attribute + ' ' + info['help'])
            response.append('#TYPE ' + attribute + ' ' + info['type'])
            response.append(
                attribute + '{' + info['device'] + '} ' + info['value'])

    return '\n'.join(response)


httpd = HTTPServer(('', os.environ['HTTP_PORT']), SimpleHTTPRequestHandler)
httpd.serve_forever()
