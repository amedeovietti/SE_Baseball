from dataclasses import dataclass

@dataclass
class Squadra:
    id : int
    team_code : str
    name : str

    def __str__(self):
        return f"{self.id} {self.team_code} {self.name}"
    

    def __repr__(self):
        return f"{self.id} {self.team_code} {self.name}"

    
    # devo aggiungere hash se voglio usare le fermate come nodi
    def __hash__(self):
        return hash(self.id)