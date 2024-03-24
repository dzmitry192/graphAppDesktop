from tkinter import *
from customtkinter import *

from addVerticesFrame import AddVerticesFrame


def centerWindow(frame, width, height):
    screen_width = frame.winfo_screenwidth()
    screen_height = frame.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    frame.geometry('%dx%d+%d+%d' % (width, height, x, y))


def onClosing(root):
    for child in root.winfo_children():
        child.destroy()
    root.destroy()


class StartFrame:
    def __init__(self):
        self.root = Tk()
        self.root.title("GraphApp")
        self.root.configure(bg='#2c3a55')
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.showStartFrame = self.showStartFrame
        self.root.protocol("WM_DELETE_WINDOW", lambda: onClosing(self.root))

        centerWindow(self.root, 400, 300)

        self.initComponents()

    def createGraphBtnClicked(self):
        self.root.withdraw()
        addVerticesFrame = AddVerticesFrame(self.root, centerWindow, onClosing)

    def initComponents(self):
        createGraphBtn = CTkButton(master=self.root, text="Создать граф", font=('Consolas', 14)
                                   , command=self.createGraphBtnClicked)
        createGraphBtn.place(relx=0.33, rely=0.3)

        exitBtn = CTkButton(master=self.root, text="Выход", font=('Consolas', 14), command=self.exitBtnClicked)
        exitBtn.place(relx=0.33, rely=0.43)

    def showStartFrame(self):
        self.root.deiconify()

    def exitBtnClicked(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StartFrame()
    app.run()
