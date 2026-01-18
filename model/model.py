from database.dao import DAO
import networkx as nx

class Model:
    
    def __init__(self):
        self.lista_anni = []
        self.lista_squadre = []
        self.dict_squadre = {}
        self.grafo = nx.Graph()
        self.dict_salari = {}


    def getAnni(self):
        self.lista_anni = DAO.leggiAnni()


    def getSquadre(self, anno):
        self.lista_squadre = DAO.trovaSquadre(anno)
        for s in self.lista_squadre:
            self.dict_squadre[s.id] = s
        return DAO.trovaSquadre(anno), len(DAO.trovaSquadre(anno))
    

    def creaGrafo(self, anno):     # anno è un int, squadre una lista
        squadre = DAO.trovaSquadre(anno)        # siccome il grafo deve essere completo cioè
                                                # ogni nodo collegato con qualsiasi altro nodo
                                                # posso usare il comando automatico di networkx:  grafo = nx.complete_graph(squadre)
        self.grafo.add_nodes_from(squadre)
        for s in squadre:
            for t in squadre:
                if s != t:
                    if anno >= 1985:                # non ci sono dati sugli stipendi prima del 1985
                        peso = DAO.trovaPeso(s,t)
                    else:
                        peso = 0
                    self.grafo.add_edge(s,t, weight = peso)


    def trovaSalariPerSquadra(self, anno, id_squadra):
        squadre = DAO.trovaSquadre(anno)
        (a,b)=self.getSquadre(anno)
        salari = {}
        for s in squadre:
            if s.id != id_squadra:
                salario_s = DAO.salariSquadra(s)
                salario_scelto = DAO.salariSquadra(self.dict_squadre[int(id_squadra)])
                salari[s.id] = int(salario_s) + int(salario_scelto)
        self.dict_salari = dict(sorted(salari.items(), key = lambda x: x[1], reverse = True))
        


    def trovaNomeDaID(self, id):
        s = self.dict_squadre[id]
        return f"{s.team_code} ({s.name})"