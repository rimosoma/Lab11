import copy

from collections import Counter

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self.listProd = []

    def fillDD(self):
        colori = self._model.model_colori()
        for color in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(key=color))
        self._view.update_page()


    def handle_graph(self, e):
        anno = self._view._ddyear.value
        color = self._view._ddcolor.value
        grafico = self._model.build_graph(anno,color)
        self.listProd=grafico.nodes()
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {len(grafico.nodes())} nodi"))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {len(grafico.edges())} archi"))
        top3=[]
        maxWeight=0
        edges = list(grafico.edges(data='weight'))
        edges_sorted = sorted(edges, key=lambda x: x[2], reverse=True)
        top3 = edges_sorted[:3]
        lista6nodi=[]
        for idx, (u, v, w) in enumerate(top3):
            self._view.txtOut.controls.append(
                ft.Text(f"{idx + 1}. da {u.Product_number} a {v.Product_number} con peso {w}"))
            lista6nodi.append(u.Product_number)
            lista6nodi.append(v.Product_number)

        counter = Counter(lista6nodi)
        nodi_ripetuti = [node for node, cnt in counter.items() if cnt > 1]

        self._view.txtOut.controls.append(
            ft.Text(f"Nodi ripetuti: {nodi_ripetuti}"))
        self.fillDDProduct()
        self._view.update_page()

    def fillDDProduct(self):
        for node in self.listProd:
            codice = node.Product_number
            self._view._ddnode.options.append(ft.Dropdown(key=codice))
        self._view.update_page()


    def handle_search(self, e):
        codice = self._view._ddnode.value
        path = self._model.longest_increasing_path(codice)
        self._view.txtOut.controls.append(ft.Text(f"Il percorso crescente a partire da {codice} è lungo {len(path)} nodi"))
        self._view.update_page()