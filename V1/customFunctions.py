import cups
import zebra
import requests
from ttkbootstrap import *
from tkinter import messagebox

BASE_URL = 'https://dummyjson.com/products'


def getUserData(id):
    finalUtente = None

    if id.get() != "" and len(id.get()) > 0:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            for product in data['products']:
                if product['id'] == int(id.get()):
                    finalUtente = product

        else: messagebox.showerror('Erro', 'Erro: Pedido falhou com o Erro ' + str(response.status_code))
            

    if finalUtente == None: messagebox.showwarning('Erro', 'Erro: Utente não encontrado')
        
    return finalUtente

    # Send the request using the requests library
    
    # Check the response status code to see if the request was successful
    
def createInputCamp(name, where, value = "John Doe", txtvariable = None):
    nameFrame = LabelFrame(where, border_color=None, text=name)
    nameFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=True, padx=20, pady=10)
    lName = Label(nameFrame, wraplength=600, textvariable=txtvariable, text=value, font=('TkDefaultFont', 14))
    lName.pack(side=LEFT, anchor=N, fill=X, expand=True)
    return lName


def printLabel():
    
    zpl_code = "^XA^FO50,50^A0N,50,50^FDHello, World!^FS^XZ"

    # create PNG image from ZPL code
    zpl_image = pyzpl.convert(zpl_code)
    png_image = Image.frombytes('RGB', zpl_image.size, zpl_image.convert('RGB'))

    # save PNG image to file
    png_image.save('label.png', 'PNG')

    # print label using CUPS
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = printers.keys()[0] # choose the first printer

    # send print job
    job_id = conn.printFile(printer_name, 'label.zpl', 'Label', {})
    print('Print job submitted:', job_id)
