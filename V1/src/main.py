import json
from ttkbootstrap import *
from tkinter.font import Font
import customFunctions as cf
import WidgetVerifications

#App Initial Configuration
app = Window(themename="darkly")
app.iconbitmap('icon.ico')
app.title("ULSCB - Etiquetas Ambulatório")
app.geometry("720x576")
app.resizable(0,0)
app.position_center()


#Function that gets the printer name/ip
data = None
f = None
      
#Variables
nProcesso = StringVar()
host = StringVar()
dataUtente = []


#Grab Data From Json
try:
    f = open("data.json")
except FileNotFoundError:    
    with open('host.txt', 'a') as f:
        f.write("{'impressora': 'ZPLQuarto', 'webservice': 'http://localhost:5000/api/v1/resources/usersxml'}")
        data = json.load(f)
        host.set(data["impressora"])
        cf.BASE_SERVICE = data['webservice']    
else:
    data = json.load(f)
    host.set(data["impressora"])
    cf.BASE_SERVICE = data['webservice']    


#MainCon Frame
mainCon = LabelFrame(app, border_color=None, bootstyle="secondary", text="Dados do Utente")
mainCon.grid(row=1, column=0, sticky="nsew", padx=20,pady=10)


#Topbar Frame
topbar = LabelFrame(app, border_color=None, bootstyle="secondary", text="Entrada de dados")
topbar.grid(row=0, column=0, sticky="nsew", padx=20,pady=20)


#Topbar Content
Label(topbar, text="Nome da Impressora", bootstyle="light").grid(row=0, column=0, sticky="nsew", padx=25,pady=10)
Label(topbar, text="Numero de Utente", bootstyle="light").grid(row=1, column=0, sticky="nsew", padx=25,pady=10)


#Processo Label Field
Verifications_Impressora = (app.register(WidgetVerifications.Verification_Impressora), '%P', '%S')
etImpressora = Label(topbar, textvariable=host, bootstyle="light")
etImpressora.grid(row=0, column=1, sticky="nsew", padx=25,pady=10)


#Processo Entry Field
Verifications_Processo = (app.register(WidgetVerifications.Verification_Processo), '%P', '%S')
etProcesso = Entry(topbar, textvariable=nProcesso, bootstyle="light", validate='all', validatecommand=(Verifications_Processo))
etProcesso.grid(row=1, column=1, sticky="nsew", padx=25,pady=10, )


#Submit Button
def OnClick_Processo(): createBasedData(frame)
btProcesso = Button(topbar, text="Submeter", bootstyle="light", command=OnClick_Processo)
btProcesso.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=25,pady=10)


#Main Frame Content
newS = Style()
newS.configure('TLabel', font_size=24)


# Create a canvas widget inside the mainCon frame
canvas = Canvas(mainCon, borderwidth=0, highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)


# Create a frame widget inside the canvas to hold the widgets
frame = Frame(canvas)
frame.pack(side=TOP, anchor=N, fill=BOTH, expand=True)
canvas.create_window((0, 0), window=frame, anchor="n")


# Configure the canvas to scroll
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
scrollbar = Scrollbar(mainCon, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)


# Pack the scrollbar widget
scrollbar.pack(side="right", fill="y")


#Topbar Grid Configuration
topbar.grid_columnconfigure(0, weight=1)
topbar.grid_columnconfigure(1, weight=100)
topbar.grid_rowconfigure(0, weight=100)
topbar.grid_rowconfigure(1, weight=100)
topbar.grid_rowconfigure(2, weight=100)


#App Grid Configuration
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=100)


#Creates Data Widgets inside specific Frame/Container 
#Depending on the Data providedz
def createBasedData(container):
    killChild(container)
    if cf.getUserData(nProcesso) != None:
        dataUtente = cf.getUserData(nProcesso)
        print(dataUtente)
        for obj in dataUtente:
            print("Birth Child")
            cf.createInputCamp(name=obj.upper(), where=container, value=dataUtente[obj])
        def OnClick_Imprimir():cf.printLabel(dataUtente, host)
        btImprimir = Button(container, text="Imprimir", bootstyle="light", command=OnClick_Imprimir)
        btImprimir.pack(fill=BOTH, expand=True, padx=25,pady=25)
        
    else: nProcesso.set(""); dataUtente = None


#Deletes all rows inside a specific container
def killChild(container):
    for child in container.winfo_children():
        child.destroy()


#App Loop :b
app.mainloop()
