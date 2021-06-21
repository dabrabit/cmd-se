import tkinter as tk
from tkinter import messagebox as msg
import widgetAdapter as interface
import menu as ExpertSystem


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.resizable(0, 0)

        self.checkBox = list()
        self.checkboxSelectedOption = list()
        self.CheckOption = list()
        self.radioSelectedOption = -1
        self.RadioOption = tk.IntVar()
        self.headerLbl = None

        self.mainFrame = tk.Frame(self, width=550, height=500, bg="#FEFEFE")
        self.dataFrame = tk.Frame(self, width=550, height=500, bg="#FEFEFE")
        self.auxFrame = tk.Frame(self, width=550, height=500, bg="#FEFEFE")
        self.frames = [self.mainFrame, self.dataFrame, self.auxFrame]

        self.nextBtn = None
        self.beforeBtn = None
        self.quitBtn = tk.Button(self.mainFrame, text="Salir", bg="white", fg="red",
                                 command=self.master.quit, cursor="hand2")

        self.rbPosX = [30, 290, 30, 290]
        self.rbPosY = [90, 90, 270, 270]
        self.rb = list()
        self.wordlist = self.setWordList()
        self._interface = interface.widgetAdaper(self.mainFrame, self.wordlist)
        self.rb.append(self._interface.getwidget())

        self.mainFrame.pack(fill='both', expand=1)
        self.setMainFrame()
        self.pack()

    def setWordList(self):
        frameList = ["INTRODUCIR OBJETOS\nA LA BC", "CONSULTAR", "GUARDAR BASE DE\nCONOCIMIENTO",
                     "CARGAR BASE DE\nCONOCIMIENTO\nEXISTENTE"]
        return frameList

    def setMainFrame(self):
        self.resetRadioButton()
        # self.selectedRadioButton()
        self.radioSelectedOption = - 1

        self.grid()
        self.headerLbl = tk.Label(self.mainFrame, text="Seleccione una opción", font=("Arial", 12), bg="#FEFEFE")

        self.headerLbl.place(x=10, y=20, width=200, height=50)
        for i in range(len(self.rb[0])):
            self.rb[0][i]["command"] = self.selectedRadioButton
            self.rb[0][i]["variable"] = self.RadioOption
            self.rb[0][i]["font"] = ("arial", 10, "bold")
            self.rb[0][i].place(x=self.rbPosX[i], y=self.rbPosY[i], width=230, height=140)

        self.nextBtn = tk.Button(self.mainFrame, text="Siguiente", fg="white", bg="#1877F2", font=("arial", 10, "bold"),
                                 cursor="hand2", command=self.onClickNext)
        self.nextBtn.place(x=450, y=450, width=70, height=30)
        self.quitBtn.place(x=30, y=450, width=70, height=30)

    def selectedRadioButton(self):
        self.radioSelectedOption = self.RadioOption.get()
        self.resetRadioButton()
        self.rb[0][self.radioSelectedOption - 1]["bg"] = "#076DF1"
        self.rb[0][self.radioSelectedOption - 1]["fg"] = "white"

    def selectedCheckbox(self):
        # Guardar si self.CheckOption[i].get() == 1
        for i in range(len(self.CheckOption)):
            if self.CheckOption[i].get() == 1:
                print(f"El elemento {i} se encuentra seleccionado ")

    def resetRadioButton(self):
        for i in range(len(self.rb[0])):
            self.rb[0][i]["bg"] = "#DCDCDC"
            self.rb[0][i]["fg"] = "black"

    def onClickNext(self):
        if self.radioSelectedOption == -1:
            msg.showinfo("Opcion no seleccionada",
                         "Selecciona alguna de las opciones disponibles.")
        else:
            self.startAnimationNext()

    def onClickBefore(self):
        self.radioSelectedOption -= 1
        self.startAnimationNext()
        self.radioSelectedOption = 0
        self.resetRadioButton()

    def startAnimationNext(self):
        alpha = self.master.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.1
            self.master.attributes("-alpha", alpha)
            self.after(10, self.startAnimationNext)
        else:
            self.setFrame()
            self.endAnimationNext()

    def endAnimationNext(self):
        alpha = self.master.attributes("-alpha")
        if alpha < 1.0:
            alpha = min(alpha + 0.1, 1.0)
            self.master.attributes("-alpha", alpha)
            self.after(5, self.endAnimationNext)

    def clearFrames(self):
        self.mainFrame.pack_forget()
        self.dataFrame.pack_forget()
        self.auxFrame.pack_forget()
        if len(self.checkBox) > 0:
            for i in range(len(self.checkBox[0])):
                self.checkBox[0][i].destroy()
            self.checkBox.clear()

    def setFrame(self):
        self.clearFrames()
        self.checkBox.clear()

        self.frames[min(self.radioSelectedOption, 1)].pack(fill='both', expand=1)

        if self.radioSelectedOption == 0:
            self.setMainFrame()
        elif self.radioSelectedOption == 1:
            self.createKnowledgeDBFrame()
        elif self.radioSelectedOption == 2:
            self.retrieveKnowledgeDB()
        elif self.radioSelectedOption == 3:
            self.saveKnowledgeDB()
        elif self.radioSelectedOption == 4:
            self.changeKnowledgeDB()

    def createKnowledgeDBFrame(self):
        ExpertSystem.menu(self.master, 1)
        self.radioSelectedOption = 0
        self.setFrame()

    def retrieveKnowledgeDB(self):
        ExpertSystem.menu(self.master, 2)
        self.radioSelectedOption = 0
        self.setFrame()

    def saveKnowledgeDB(self):
        ExpertSystem.menu(self.master, 3)
        self.radioSelectedOption = 0
        self.setFrame()

    def changeKnowledgeDB(self):
        ExpertSystem.menu(self.master, 4)
        self.radioSelectedOption = 0
        self.setFrame()
