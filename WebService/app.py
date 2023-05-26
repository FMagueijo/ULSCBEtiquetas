import mimetypes
from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

app.debug = True


# dados utente aleatorios
dadosurgencia = [
    {'processo': '82122023',
     'nome'  : 'Francisco Gomes Gonçalves Magueijo',
     'data'  : '16-05-2022',
     'hora'  : '12:23'},
    {'episodio': '80250123',
     'nome'  : 'Carlos Asdrubal Leitão ',
     'data'  : '13-05-2022',
     'hora'  : '02:23'},
    {'episodio': '81010296',
     'nome'  : 'Cavaco Vieira Silva Pires Arizmendi Mancini Mourinho Guardiola Paulo Portas Vilhena Camilo',
     'data'  : '01-02-2022',
     'hora'  : '20:01'},
    {'episodio': '80123456',
     'nome'  : 'Cataria Rocha da Silva Cunha Dias',
     'data'  : '16-05-2022',
     'hora'  : '12:23'},
    {'episodio': '80654785',
     'nome'  : 'Marta Feliz Temido Ribeiro',
     'data'  : '16-05-2022',
     'hora'  : '10:30'},
    {'episodio': '80127458',
     'nome'  : 'António Vitorina de Almeida Silva da Costa Paiva',
     'data'  : '10-05-2022',
     'hora'  : '16:23'}
]


# Router per definition
@app.route("/", methods=['GET'])
def home():
    return '<h1>Web services para Episodios Urgencia</h1>\n'

# JSON
# Get dados urgencia
@app.route('/api/v1/resources/daurgencia', methods=['GET'])
def getUrgencia():
    if 'episodio' in request.args:
        episodio = request.args.get('episodio')
    else:
        return jsonify({'resultUrgencia':''})
    # find the episode
    for dados in range (len(dadosurgencia)):
        #print (dados)
        for key, value in dadosurgencia[dados].items():
            #print (value)
            if episodio == value:
                return (jsonify(dadosurgencia[dados]))
                break
        
    return jsonify({'resultUrgencia':''})

# Get dados urgencia xml
"""
    <urgencia>
        <episodio></episodio>
        <nome></nome>
        <data></data>
        <hora></hora>
    </urgencia>
"""
@app.route('/api/v1/resources/daurgenciaxml', methods=['GET'])
def getUrgenciaxml():
    print("Ola " + str(request.args))

    if 'episodio' in request.args:
        episodio = request.args.get('episodio')
    else:
        return jsonify({'resultUrgencia':''})
    # find the episode
    for dados in range (len(dadosurgencia)):
        #print (dados)
        for key, value in dadosurgencia[dados].items():
            #print (value)
            if episodio == value:
                # loop again
                urgencia = dadosurgencia[dados]
                break
        
    root = ET.Element('urgencia')
    episodioxml = ET.SubElement(root, 'episodio')
    episodioxml.text = str(episodio)
    nome = ET.SubElement(root, 'nome')
    nome.text = str(urgencia['nome'])
    data = ET.SubElement(root, 'data')
    data.text = str(urgencia['data'])
    hora = ET.SubElement (root, 'hora')
    hora.text = str(urgencia['hora'])
    
    return Response (ET.tostring(root).decode('utf-8'), mimetype='text/xml')



# main
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port='5000')
