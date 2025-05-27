from typing import Any, List

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.iMap = {}

    def model_colori(self):
        return DAO.getColori()

    def build_graph(self,anno, color):
        lista_di_prodotti = DAO.getProducts()

        for prodotto in lista_di_prodotti:
            self.iMap[prodotto.Product_number] = prodotto

        lista_archi = DAO.getArchi(anno,color)      #ogni riga in questa lista_archi è una tripla di codprod1, codprod2 e weight
        for arco in lista_archi:
            prod1 = self.iMap[arco[0]]
            prod2 = self.iMap[arco[1]]
            weight = arco[2]
            self._graph.add_edge(u_of_edge=prod1, v_of_edge=prod2, weight=weight)
        print(f"il grafo ha {len(self._graph.nodes)}nodi")
        print(f"il grafo ha {len(self._graph.edges)}archi")
        return self._graph




    def longest_increasing_path(self, start: Any) -> List[Any]:
        """
        Metodo di ingresso: inizializza lo stato e chiama la ricorsione.
        Restituisce il percorso più lungo (#archi) di archi a peso strettamente crescente.
        """
        # — E: azzera lo stato
        self._best_path = []
        # Avvio la ricorsione con peso iniziale “infinito negativo”
        self._dfs(current=self.iMap[int(start)], last_w=float('-inf'), path=[self.iMap[int(start)]])
        return self._best_path

    def _dfs(self, current: Any, last_w: float, path: List[Any]):
        """
        Metodo ricorsivo:
           E: sempre eseguito
           A: caso base
           B: genera scelte
           C: filtro + ricorsione
           D: backtracking
        """
        # — E: controllo e aggiorno il best_path se questo è più lungo
        #       (numero di archi = len(path)-1)
        if (len(path) - 1) > (len(self._best_path) - 1):
            self._best_path = path.copy()

        # — B: per ogni possibile arco uscente
        for neigh in self._graph.neighbors(current):
            w = self._graph[current][neigh].get('weight', 0)

            # — C: filtro: peso strettamente crescente e no cicli
            if w > last_w and neigh not in path:
                path.append(neigh)                        # Aggiungo al percorso
                self._dfs(current=neigh,                   # Ricorsione
                          last_w=w,
                          path=path)
                # — D: backtracking
                path.pop()


