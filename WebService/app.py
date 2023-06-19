import mimetypes
from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

app.debug = True



users = [
    {'processo': '82122023',
     'nome'  : 'Francisco Gomes Gonçalves Magueijo',
     'dn'  : '16-05-2022'},
    {'processo': '80250123',
     'nome'  : 'Carlos Asdrubal Leitão',
     'dn'  : '13-05-2022'},
    {'processo': '81010296',
     'nome'  : 'Cavaco Vieira Silva Pires Arizmendi Mancini Mourinho Guardiola Paulo Portas Vilhena Camilo',
     'dn'  : '01-02-2022'},
    {'processo': '80123456',
     'nome'  : 'Cataria Rocha da Silva Cunha Dias',
     'dn'  : '16-05-2022'},
    {'processo': '80654785',
     'nome'  : 'Marta Feliz Temido Ribeiro',
     'dn'  : '16-05-2022'},
    {'processo': '80127458',
     'nome'  : 'António Vitorina de Almeida Silva da Costa Paiva',
     'dn'  : '10-05-2022'}
]


# Router per definition
@app.route("/", methods=['GET'])
def home():
    return '<h1>Web services para Episodios Urgencia</h1>\n'

# JSON
# Get user data
@app.route('/api/v1/resources/users', methods=['GET'])
def getUsers():
    if 'processo' in request.args:
        processo = request.args.get('processo')
    else:
        return jsonify({'result': ''})

    # Find the user by process number
    for user in users:
        if processo == user['processo']:
            return jsonify(user)

    return jsonify({'result': ''})

# Get user data in XML format
"""
    <user>
        <processo></processo>
        <nome></nome>
        <dn></dn>
    </user>
"""
@app.route('/api/v1/resources/usersxml', methods=['GET'])
def getUsersXml():
    if 'processo' in request.args:
        processo = request.args.get('processo')
    else:
        return jsonify({'result': ''})

    # Find the user by process number
    for user in users:
        if processo == user['processo']:
            # Create XML response
            root = ET.Element('user')
            processo_xml = ET.SubElement(root, 'processo')
            processo_xml.text = str(user['processo'])
            nome = ET.SubElement(root, 'nome')
            nome.text = str(user['nome'])
            dn = ET.SubElement(root, 'dn')
            dn.text = str(user['dn'])

            return Response(ET.tostring(root).decode('utf-8'), mimetype='text/xml')

    return jsonify({'result': ''})




# main
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port='5000')
