from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox
import socket 
import requests
import xmltodict
from xml.etree import ElementTree
from datetime import datetime
import json

BASE_SERVICE = ''
#
def getUserData(id):
    BASE_PARAMS = {'processo': id.get()}
    
    try:
        response = requests.get(BASE_SERVICE, timeout=.5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        Messagebox.show_error(title="Erro", message=str(e))
        return None
    
    if(len(id.get()) != 8): Messagebox.show_error(title="Erro", message="Numero de Processo Inválido, tamanho do processo tem de ser sempre 8."); return None 
      

    if response.status_code == 200:
        try:
            response = requests.get(BASE_SERVICE, params=BASE_PARAMS, timeout=.1)
            root = ElementTree.fromstring(response.content)

            dict_obj = xmltodict.parse(ElementTree.tostring(root))
            first_key = list(dict_obj.keys())[0]
            dict_obj = dict_obj[first_key]
        except Exception as e:
            Messagebox.show_error(title="Erro", message=str(e))
            return None
         
    return dict_obj

'''
Nova
^XA
^CI28
^FO5,5^GB390,150,2^FS
^FO10,95^A0N,14^FDProcesso: 123456^FS
^FO10,115^A0N,14^FDNome: Fernandes de Sousa e Sá Carneiro de Niro^FS
^FO10,135^A0N,14^FDData de Nascimento: 10-05-2023^FS
^FO80,15^BY2,2,50^BC^FD83023059^FS
^XZ
'''

#Prints Above Label with number of fields given on the label Info
def printLabel(labelInfo, host):

    outputLabel = b"^XA^CI28^FO5,5^GB390,150,2^FS"
    currentL = 0

    for obj in labelInfo:

        outputLabel += bytes(f"^FO10,{90 + 20*currentL}^A0N,19^FD{obj.upper()}: {labelInfo[obj]}^FS", 'utf-8')
        if(obj == "episodio" or obj == "processo"): outputLabel += bytes(f"^FO140,15^BY1,1,50^BC^FD{labelInfo[obj]}^FS", 'utf-8')
        currentL += 1
    
    # Nao Usado # outputLabel += bytes(f"^FO10,{70 + 20*currentL}^A0N,14^FDData Admissão: { datetime.now().isoformat(' ', 'seconds') } ^FS", 'utf-8')
    outputLabel += bytes(f"^Xz", 'utf-8')
    
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
    host = host.get()
    port = 9100   
    
    try:           
        mysocket.connect((host, port))
        mysocket.send(outputLabel)
        mysocket.close ()
        with open('historico.txt', 'a') as f:
            f.write(f"({datetime.now().isoformat(' ', 'seconds')}) Imprimida/Printed => {str(outputLabel)} \n")
            Messagebox.show_info(title="Successo", message="Etiqueta Imprimida com sucesso")
    except Exception as e:
        Messagebox.show_error(title="Erro", message=str(e))

#Create Row of Given Data
def createInputCamp(name, where, value = "John Doe", txtvariable = None):
    nameFrame = LabelFrame(where, border_color=None, text=name)
    nameFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=True, padx=20, pady=10)
    lName = Label(nameFrame, wraplength=600, textvariable=txtvariable, text=value, font=('TkDefaultFont', 14))
    lName.pack(side=LEFT, anchor=N, fill=X, expand=True)
    return lName

    
