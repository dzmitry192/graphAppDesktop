from tkinter import *
from customtkinter import *
from tkinter import messagebox

import networkx as nx
import matplotlib.pyplot as plt


class GraphOperationsFrame:
    def __init__(self, root, graph, centerWindow, onClosing):
        self.startVertex = None
        self.endVertex = None
        self.root = root
        self.graph = graph
        self.centerWindow = centerWindow
        self.onClosing = onClosing
        # ----frame-----
        self.graphOperationsFrame = Toplevel(self.root)
        self.graphOperationsFrame.geometry("460x153")
        self.graphOperationsFrame.configure(bg='#2c3a55')
        self.graphOperationsFrame.grid_propagate(False)
        self.graphOperationsFrame.protocol("WM_DELETE_WINDOW", lambda: self.onClosing(self.Groot))

        centerWindow(self.graphOperationsFrame, 460, 153)

        self.initComponents()

    def initComponents(self):
        startVertexLbl = CTkLabel(master=self.graphOperationsFrame, text="Вершина 1", text_color="#FFFFFF", font=("Consolas", 14))
        startVertexLbl.grid(row=0, column=0, padx=25, pady=5, sticky='nw')

        endVertexLbl = CTkLabel(master=self.graphOperationsFrame, text="Вершина 2", text_color="#FFFFFF",
                                  font=("Consolas", 14))
        endVertexLbl.grid(row=1, column=0, padx=25, pady=5, sticky='nw')

        keys = list(self.graph.keys())

        self.startVertex = StringVar()
        self.startVertex.set(keys[0])
        startVertexOption = CTkOptionMenu(master=self.graphOperationsFrame, values=keys,
                                          command=self.startVertex.set)
        startVertexOption.grid(row=0, column=1, pady=5, sticky='nw')

        self.endVertex = StringVar()
        self.endVertex.set(keys[0])
        endVertexOption = CTkOptionMenu(master=self.graphOperationsFrame, values=keys,
                                        command=self.endVertex.set)
        endVertexOption.grid(row=1, column=1, pady=5, sticky='nw')

        shortestPathFromAToBBtn = CTkButton(master=self.graphOperationsFrame, text="Кр. путь от 1 до 2",
                                            text_color="#FFFFFF", font=("Consolas", 14),
                                            command=self.shortestPathBtnClicked)

        printGraphBtn = CTkButton(master=self.graphOperationsFrame, width=140, text="Распечатать граф", text_color="#FFFFFF",
                                  font=("Consolas", 14),
                                  anchor='center',
                                  command=self.printGraphBtnClicked)

        shortestPathFromAToBBtn.grid(row=0, column=2, padx=10, pady=5, sticky='e')
        printGraphBtn.grid(row=1, column=2, padx=10, pady=5, sticky='e')

        showStartFrameBtn = CTkButton(master=self.graphOperationsFrame, width=140, text="На главную", text_color="#FFFFFF",
                                      font=("Consolas", 14),
                                      anchor='center',
                                      command=self.showStartFrameBtnClicked)
        showStartFrameBtn.grid(row=2, column=2, padx=10, pady=5, sticky='e')

    def shortestPathBtnClicked(self):
        if self.startVertex.get() == self.endVertex.get():
            messagebox.showinfo("Кратчайший путь от вершины 1 до 2", "Начало {}, конец - {}\nПуть: {}\nДлина пути: {}".format(self.startVertex.get(), self.endVertex.get(), self.startVertex.get(), "0"))
        else:
            newGraph = nx.Graph()
            for vertex, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    newGraph.add_edge(vertex, neighbor, weight=int(weight))

            try:
                shortest_path = nx.shortest_path(newGraph, source=self.startVertex.get(), target=self.endVertex.get(), weight='weight')
                path_length = nx.shortest_path_length(newGraph, source=self.startVertex.get(), target=self.endVertex.get(), weight='weight')
                messagebox.showinfo("Кратчайший путь от вершины 1 до 2", "Начало - {}, конец - {}:\nПуть: {}\nДлина пути: {}".format(
                                    self.startVertex.get(), self.endVertex.get(), shortest_path, path_length))
            except nx.NodeNotFound:
                messagebox.showwarning("Предупреждение", "Пути от {} до {} не существует!".format(self.startVertex.get(), self.endVertex.get()))

    def shortestPathsFromAToAllBtnClicked(self):
        pass

    def printGraphBtnClicked(self):
        plt.close()
        graph = nx.Graph()
        graph.add_nodes_from(self.graph.copy().keys())
        for node, neighbors in self.graph.copy().items():
            for neighbor, weight in neighbors.items():
                graph.add_edge(node, neighbor, weight=int(weight))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()

    def showStartFrameBtnClicked(self):
        self.root.showStartFrame()
        self.graphOperationsFrame.destroy()
