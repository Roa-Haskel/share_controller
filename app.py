import flask
from flask import request
import re
from common import StagingSet

app=flask.Flask(__name__)

clientMap=dict()


def chickLanaddr(lanAddrStr):
    try:
        data=eval(lanAddrStr)
    except:
        return False
    if not isinstance(data,tuple):
        return False
    lanIp,port = data
    return re.fullmatch("^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)(\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)){3}",lanIp) is not None \
            and  isinstance(port, int) and port > 1 and port <= 65535

@app.route('/register/<lanAddr>')
def register(lanAddr):
    if not chickLanaddr(lanAddr):
        return 'lanaddr error'
    data=eval(lanAddr)
    ip=request.remote_addr
    if  ip in clientMap and data not in clientMap[ip]:
        if len(clientMap[ip])<10:
            clientMap[ip].add(data)
    elif ip not in clientMap and len(clientMap)<100:
        clientMap[ip]=StagingSet([data])
    return ''

@app.route("/delete/<lanAddr>")
def delete(lanAddr):
    if not chickLanaddr(lanAddr):
        return 'lanaddr error'
    data=eval(lanAddr)
    ip = request.remote_addr
    if ip in clientMap:
        if data in clientMap[ip]:
            clientMap[ip].safeRemove(data)
    return ''

@app.route('/clients')
def getClients():
    ip=request.remote_addr
    return str(list(clientMap[ip])) if ip in clientMap else str(set())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)