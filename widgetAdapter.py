import tkinter as tk


class widgetAdaper():
    def __init__(self, frame, wordlist, option=1):
        super(widgetAdaper, self).__init__()

        self.frame = frame
        self.widget = list()
        self.option = option
        self.wordlist = wordlist

    def setRadio(self):
        for i in range(len(self.wordlist)):
            self.widget.append(tk.Radiobutton(self.frame, text=self.wordlist[i], value=i + 1,
                                              activebackground="#076DF1", activeforeground="white", bg="#DCDCDC", bd=10,
                                              cursor="hand2", justify=tk.CENTER))

    def setCheckbox(self):
        for i in range(len(self.wordlist)):
            self.widget.append(tk.Checkbutton(self.frame, text=self.wordlist[i],
                                              activebackground="#076DF1", activeforeground="white", bg="#DCDCDC", bd=10,
                                              cursor="hand2", justify=tk.CENTER))

    def getwidget(self):
        self.widget.clear()
        if self.option == 1:
            self.setRadio()
        elif self.option == 2:
            self.setCheckbox()
        return self.widget
