from tkinter import *
from customtkinter import *
from tkinter import messagebox

from graphOperationsFrame import GraphOperationsFrame


def validateVertexWeight(newValue):
    return (newValue.isdigit() and len(newValue) <= 2 and int(newValue) >= 0) or newValue == ''


def removeVertexNeighborComponentClicked(vertexNeighborComponentFrame):
    vertexNeighborComponentFrame.destroy()


class AddNeighborsFrame:
    def __init__(self, root, vertices, backToAddVertices, centerWindow, onClosing):
        # variables
        self.root = root
        self.centerWindow = centerWindow
        self.onClosing = onClosing
        self.vertices = vertices
        self.backToAddVertices = backToAddVertices
        self.frameNameLbl = None
        self.listNeighborsComponents = []
        self.listNeighborsComponentsScrollFrame = None
        self.addVerticesBtn = None
        self.createGraphBtn = None
        self.backBtn = None
        # --------------------
        self.addNeighborsFrame = Toplevel(self.root)
        self.addNeighborsFrame.geometry("600x440")
        self.addNeighborsFrame.configure(bg='#2c3a55')
        self.addNeighborsFrame.grid_propagate(False)
        self.addNeighborsFrame.protocol("WM_DELETE_WINDOW", lambda: self.onClosing(self.root))

        centerWindow(self.addNeighborsFrame, 600, 440)

        self.initComponents()

    def initComponents(self):
        self.frameNameLbl = CTkLabel(self.addNeighborsFrame, text="Добавление соседей", text_color='#FFFFFF',
                                     font=("Consolas", 14))
        self.frameNameLbl.place(relx=0.5, rely=0.02, anchor='n')

        self.listNeighborsComponents = CTkLabel(self.addNeighborsFrame, text="Список связей", text_color='#FFFFFF',
                                                font=("Consolas", 14))
        self.listNeighborsComponents.place(relx=0, rely=0.138, x=20, anchor='w')

        self.addVerticesBtn = CTkButton(self.addNeighborsFrame, text="Добавить вершину", font=('Consolas', 14),
                                        command=self.addVerticesBtnClicked)
        self.addVerticesBtn.place(relx=1.0, x=-243, rely=0.1, anchor='n')

        self.createGraphBtn = CTkButton(self.addNeighborsFrame, text="Создать граф", font=('Consolas', 14),
                                        command=self.createGraphBtnClicked)
        self.createGraphBtn.place(relx=1.0, x=-90, rely=0.1, anchor='n')

        self.listNeighborsComponentsScrollFrame = CTkScrollableFrame(master=self.addNeighborsFrame, width=560,
                                                                     height=270)
        self.listNeighborsComponentsScrollFrame.place(relx=0.5, rely=1.0, x=0, y=-60, anchor='s')

        self.backBtn = CTkButton(self.addNeighborsFrame, text="<Назад", font=('Consolas', 14),
                                 command=self.backBtnClicked)
        self.backBtn.pack(side='bottom', pady=13)

    def createGraphBtnClicked(self):
        graph = {}
        for vertex in self.vertices:
            graph[vertex] = {}

        if len(self.listNeighborsComponentsScrollFrame.winfo_children()) == 0:
            self.addNeighborsFrame.withdraw()
            graphOperationsFrame = GraphOperationsFrame(self.root, graph, self.centerWindow, self.onClosing)
        else:
            isValid = True
            for child in self.listNeighborsComponentsScrollFrame.winfo_children():
                if isinstance(child, CTkFrame):
                    selectedVertex = child.selectedVertex.get()
                    selectedNeighbor = child.selectedNeighbor.get()
                    vertexWeight = child.vertexWeightInp.get()

                    if len(vertexWeight) == 0:
                        messagebox.showwarning("Предупреждение", "Вы не заполнили все поля")
                        isValid = False
                        break
                    elif selectedVertex == selectedNeighbor and int(vertexWeight) != 0:
                        messagebox.showwarning("Предупреждение", "Расстояние точки до себя должно быть равно 0!")
                        isValid = False
                        break
                    elif selectedVertex in graph and graph[selectedVertex].__contains__(selectedNeighbor):
                        messagebox.showwarning("Предупреждение",
                                               "Вы добавили одну и ту же соседнюю вершину несколько раз!")
                        isValid = False
                        break
                    else:
                        graph[selectedVertex][selectedNeighbor] = vertexWeight
                        if selectedNeighbor in graph:
                            graph[selectedNeighbor][selectedVertex] = vertexWeight
                        else:
                            graph[selectedNeighbor] = {selectedVertex: vertexWeight}
            if isValid:
                self.addNeighborsFrame.withdraw()
                graphOperationsFrame = GraphOperationsFrame(self.root, graph, self.centerWindow, self.onClosing)

    def addVerticesBtnClicked(self):
        vertexNeighborComponentFrame = CTkFrame(self.listNeighborsComponentsScrollFrame, width=550, height=100,
                                                fg_color='#2c3a55')
        vertexNeighborComponentFrame.pack_propagate(False)

        validateVertexWeightInpCommand = vertexNeighborComponentFrame.register(validateVertexWeight)

        vertexNameLbl = CTkLabel(vertexNeighborComponentFrame, text="Вершина 1", text_color='#FFFFFF',
                                 font=("Consolas", 14))
        vertexNameLbl.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        vertexNeighborComponentFrame.selectedVertex = StringVar()
        vertexNeighborComponentFrame.selectedVertex.set(self.vertices.copy()[0])
        vertexOptionMenu = CTkOptionMenu(master=vertexNeighborComponentFrame, values=self.vertices.copy(),
                                         command=vertexNeighborComponentFrame.selectedVertex.set)
        vertexOptionMenu.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

        vertexWeightLbl = CTkLabel(master=vertexNeighborComponentFrame, text="Вес", text_color="#FFFFFF",
                                   font=("Consolas", 14))
        vertexWeightLbl.grid(row=0, column=1, padx=10, pady=10)

        vertexNeighborComponentFrame.vertexWeightInp = CTkEntry(master=vertexNeighborComponentFrame)
        vertexNeighborComponentFrame.vertexWeightInp.configure(validate='key',
                                                               validatecommand=(validateVertexWeightInpCommand, '%P'))
        vertexNeighborComponentFrame.vertexWeightInp.grid(row=1, column=1, padx=10, pady=10)

        neighborNameLbl = CTkLabel(vertexNeighborComponentFrame, text="Вершина 2", text_color='#FFFFFF',
                                   font=("Consolas", 14))
        neighborNameLbl.grid(row=0, column=2, padx=30, pady=10, sticky='ne')

        vertexNeighborComponentFrame.selectedNeighbor = StringVar()
        vertexNeighborComponentFrame.selectedNeighbor.set(self.vertices.copy()[0])
        neighborOptionMenu = CTkOptionMenu(master=vertexNeighborComponentFrame, values=self.vertices.copy(),
                                           command=vertexNeighborComponentFrame.selectedNeighbor.set)
        neighborOptionMenu.grid(row=1, column=2, padx=10, pady=10, sticky='ne')

        removeBtn = CTkButton(vertexNeighborComponentFrame, text='Удалить', width=20, text_color="#FFFFFF",
                              font=("Consolas", 14),
                              command=lambda: removeVertexNeighborComponentClicked(vertexNeighborComponentFrame))
        removeBtn.grid(row=0, column=3, padx=10, pady=10, sticky='ne')

        vertexNeighborComponentFrame.pack(pady=5, fill='both')
        vertexNeighborComponentFrame.lift()

    def backBtnClicked(self):
        self.backToAddVertices()
        self.addNeighborsFrame.destroy()
