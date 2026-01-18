import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.anno_scelto = None
        self.squadre_filtrate = []
        self.squadra_scelta = None


    def popolaDropdown(self, dd):
        dd.options.clear()
        self._model.getAnni()
        for anno in self._model.lista_anni:
            dd.options.append(ft.dropdown.Option(text=anno))

    def handleCambiaAnno(self, e):
        self.anno_scelto = e.control.value
        if self.anno_scelto is None:
            return
        (squadre, n_squadre) = self._model.getSquadre(self.anno_scelto)
        self.squadre_filtrate = squadre
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {n_squadre}"))
        self._view.dd_squadra.options.clear()
        for s in squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{s.team_code} ({s.name})"))
            self._view.dd_squadra.options.append(ft.dropdown.Option(key=s.id, text=f"{s.team_code} ({s.name})"))
        self._view.dd_squadra.update()
        self._view.page.update()


    def handle_crea_grafo(self, e):
        if self.anno_scelto is None or self.squadre_filtrate is None:
            self._view.show_alert("Seleziona anno e forma")
            return
        self._model.creaGrafo(int(self.anno_scelto))

        # solo per stampare i dati del grafo (per controllare)
        print(self._model.grafo)
        for u, v, data in self._model.grafo.edges(data=True):
            peso = data.get("weight", 0)
            print(f"{u}, {v}, peso = {peso}")


    def handleCambiaSquadra(self, e):
        self.squadra_scelta = e.control.value       # id squadra


    def handle_dettagli(self, e):
        if self.squadra_scelta is None:
            return
        self._model.trovaSalariPerSquadra(self.anno_scelto, self.squadra_scelta)
        self._view.txt_risultato.controls.clear()
        for id in self._model.dict_salari:
            nome_squadra = self._model.trovaNomeDaID(id)
            self._view.txt_risultato.controls.append(ft.Text(f"{nome_squadra}, salario totale: {self._model.dict_salari[id]}"))
        self._view.page.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO