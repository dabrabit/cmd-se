import tkinter as tk
import GUI


def getScreenResolution(parent):
    width = parent.winfo_reqwidth()
    height = parent.winfo_reqheight()
    screenWidth = int(parent.winfo_screenwidth()/2.5 - width/2)
    screenHeight = int(parent.winfo_screenheight()/4 - height/2)

    parent.geometry("+{}+{}".format(screenWidth, screenHeight))

    return GUI.App(master=parent)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("550x500")
    root.title("Buscador de comandos para Linux")
    app = getScreenResolution(root)
    app.mainloop()
    app.destroy()
