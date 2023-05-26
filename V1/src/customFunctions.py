from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox
import socket 
import requests
import xmltodict
from xml.etree import ElementTree
from datetime import datetime

BASE_SERVICE = 'http://localhost:5000/api/v1/resources/daurgenciaxml'

def getUserData(id):
    
      
    BASE_PARAMS = {'episodio': id.get()}
    
    try:
        response = requests.get(BASE_SERVICE, timeout=.1)
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
^XA
^CI28
^FO5,5^GB627.5,150,2^FS
^FO10,15^A0N,26^FDULSCB - Ambulatório^FS
^FO10,45^A0N,16^FDINFORMAÇÃO DO UTENTE^FS
^FO10,70^A0N,14^FDNome: Fernandes de Sousa e Sá Carneiro de Niro^FS
^FO10,90^A0N,14^FDProcesso: 123456^FS
^FO10,110^A0N,14^FDData de Admissão: 10-05-2023^FS
^FO10,130^A0N,14^FDDN: 19-02-2005^FS ^FO150,130^A0N,14^FDM / 18 anos^FS
^FO360,40^BY2^BCN,80,Y,N,N^FD83023059^FS
^XZ
'''    





def printLabel(labelInfo, host):

    outputLabel = b"^XA^CI28^FO5,5^GB627.5,150,2^FS^FO10,15^A0N,26^FDULSCB - Ambulatorio^FS^FO10,45^A0N,16^FDINFORMACAO DO UTENTE^FS"
    currentL = 0

    for obj in labelInfo:

        outputLabel += bytes(f"^FO10,{70 + 20*currentL}^A0N,14^FD{obj}: {labelInfo[obj]}^FS", 'utf-8')
        if(obj == "episodio" or obj == "processo"): outputLabel += bytes(f"^FO360,40^BY2^BCN,80,Y,N,N^FD{labelInfo[obj]}^FS", 'utf-8')
        currentL += 1
    
    outputLabel += bytes(f"^FO10,{70 + 20*currentL}^A0N,14^FDData Admissão: { datetime.now().isoformat(' ', 'seconds') } ^FS^Xz", 'utf-8')
         
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
    host = host.get()
    port = 9100   
    try:           
        mysocket.connect((host, port)) #connecting to host
        mysocket.send(outputLabel)#using bytes
        mysocket.close () #closing connection
        with open('history.txt', 'a') as f:
            f.write(f"({datetime.now().isoformat(' ', 'seconds')}) Imprimida/Printed => {str(outputLabel)} \n")
    except Exception as e:
        Messagebox.show_error(title="Erro", message=str(e))


def createInputCamp(name, where, value = "John Doe", txtvariable = None):
    nameFrame = LabelFrame(where, border_color=None, text=name)
    nameFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=True, padx=20, pady=10)
    lName = Label(nameFrame, wraplength=600, textvariable=txtvariable, text=value, font=('TkDefaultFont', 14))
    lName.pack(side=LEFT, anchor=N, fill=X, expand=True)
    return lName

    
