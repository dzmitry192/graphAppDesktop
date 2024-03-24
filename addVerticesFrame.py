from tkinter import *
from customtkinter import *
from tkinter import messagebox

from addNeighborsFrame import AddNeighborsFrame


def validateVertexName(newValue):
    return (newValue.isalpha() and newValue.isupper() and len(newValue) <= 1) or newValue == ""


def removeVertexBtnClicked(vertexComponentFrame):
    vertexComponentFrame.destroy()


class AddVerticesFrame:
    def __init__(self, root, centerWindow, onClosing):
        # variables
        self.root = root
        self.centerWindow = centerWindow
        self.onClosing = onClosing
        self.vertices = []
        self.frameNameLbl = ""
        self.listVerticesLbl = ""
        self.addVerticesBtn = None
        self.continueBtn = None
        self.listVerticesScrollFrame = None
        self.listComponents = {}
        # --------frame------------
        self.addVerticesFrame = Toplevel(self.root)
        self.addVerticesFrame.geometry("600x390")
        self.addVerticesFrame.configure(bg='#2c3a55')
        self.addVerticesFrame.grid_propagate(False)
        self.addVerticesFrame.protocol("WM_DELETE_WINDOW", lambda: self.onClosing(self.root))

        centerWindow(self.addVerticesFrame, 600, 390)

        self.initComponents()

    def initComponents(self):
        self.frameNameLbl = CTkLabel(self.addVerticesFrame, text="Создание вершин", text_color='#FFFFFF',
                                     font=("Consolas", 14))
        self.frameNameLbl.place(relx=0.5, rely=0.02, anchor='n')

        self.listVerticesLbl = CTkLabel(self.addVerticesFrame, text="Список вершин", text_color='#FFFFFF',
                                        font=("Consolas", 14))
        self.listVerticesLbl.place(relx=0, rely=0.138, x=20, anchor='w')

        self.addVerticesBtn = CTkButton(self.addVerticesFrame, text="Добавить вершину", font=('Consolas', 14),
                                        command=self.addVerticesBtnClicked)
        self.addVerticesBtn.place(relx=1.0, x=-243, rely=0.1, anchor='n')

        self.continueBtn = CTkButton(self.addVerticesFrame, text="Далее>", font=('Consolas', 14),
                                     command=self.continueBtnClicked)
        self.continueBtn.place(relx=1.0, x=-90, rely=0.1, anchor='n')

        self.listVerticesScrollFrame = CTkScrollableFrame(master=self.addVerticesFrame, width=560, height=270)
        self.listVerticesScrollFrame.place(relx=0.5, rely=1.0, x=0, y=-20, anchor='s')

    def createVertexComponent(self):
        vertexComponentFrame = CTkFrame(self.listVerticesScrollFrame, width=550, height=200, fg_color='#2c3a55')

        validateVertexNameCommand = vertexComponentFrame.register(validateVertexName)

        vertexNameLbl = CTkLabel(vertexComponentFrame, text="Название вершины:", text_color='#FFFFFF',
                                 font=("Consolas", 14))
        vertexNameLbl.pack(side='left', padx=30)

        removeVertexBtn = CTkButton(vertexComponentFrame, text='Удалить', text_color="#FFFFFF", font=("Consolas", 14),
                                    command=lambda: removeVertexBtnClicked(vertexComponentFrame))
        removeVertexBtn.pack(side='right', padx=30)

        vertexNameInp = CTkEntry(vertexComponentFrame)
        vertexNameInp.configure(validate='key', validatecommand=(validateVertexNameCommand, '%P'))
        vertexNameInp.pack(side='right')

        vertexComponentFrame.pack(pady=5, fill='both')
        vertexComponentFrame.lift()

    def getVertices(self):
        vertex_names = []
        seen_names = set()
        duplicate_names = set()

        for child in self.listVerticesScrollFrame.winfo_children():
            if isinstance(child, CTkFrame):
                for widget in child.winfo_children():
                    if isinstance(widget, CTkEntry):
                        name = widget.get()
                        if name in seen_names:
                            duplicate_names.add(name)
                        else:
                            vertex_names.append(name)
                            seen_names.add(name)
        if len(vertex_names) == 0:
            messagebox.showwarning("Предупреждение", "Вы не добавили вершин графа!")
            return {}
        elif duplicate_names:
            message = "Найдены повторяющиеся вершины: {}".format(", ".join(duplicate_names))
            messagebox.showwarning("Предупреждение", message)
            return {}
        elif vertex_names.__contains__(""):
            messagebox.showwarning("Предупреждение", "Вы не заполнили названия всех вершин!")
            return {}
        else:
            return vertex_names

    def addVerticesBtnClicked(self):
        self.createVertexComponent()

    def backToAddVertices(self):
        self.addVerticesFrame.deiconify()

    def continueBtnClicked(self):
        self.vertices = self.getVertices()
        if len(self.vertices) > 0:
            self.addVerticesFrame.withdraw()
            addNeighborsFrame = AddNeighborsFrame(self.root, self.vertices, self.backToAddVertices, self.centerWindow, self.onClosing)
