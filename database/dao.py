from database.DB_connect import DBConnect
from model.squadra import Squadra


class DAO:

    @staticmethod
    def leggiAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ SELECT year 
                    FROM team """
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        anni = []
        for d in result:
            if d["year"] >= 1980 and d["year"] not in anni:
                anni.append(d["year"])
        cursor.close()
        conn.close()
        return anni
    

    @staticmethod
    def trovaSquadre(anno):
        # salva tutte le squadre (come oggetti Squadra) che
        # hanno giocato in un determinato anno scelto dal dd
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ SELECT id, team_code, name
                    FROM team t
                    WHERE t.year = %s """
        cursor.execute(query, (anno,))
        for row in cursor:
            r = Squadra(row["id"], row["team_code"], row["name"])
            result.append(r)
        cursor.close()
        conn.close()
        return result
    

    @staticmethod
    def trovaPeso(squadra1, squadra2):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ SELECT salary
                    FROM salary s
                    WHERE s.team_id = %s OR s.team_id = %s """
        cursor.execute(query, (squadra1.id,squadra2.id))
        for row in cursor:
            result.append(row)
        total_salary = 0
        for d in result:
            total_salary += int(d["salary"])
        cursor.close()
        conn.close()
        return total_salary
    

    @staticmethod
    def salariSquadra(squadra):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ SELECT salary
                    FROM salary s
                    WHERE s.team_id = %s """
        cursor.execute(query, (squadra.id,))
        for row in cursor:
            result.append(row)
        total_salary = 0
        for d in result:
            total_salary += int(d["salary"])
        cursor.close()
        conn.close()
        return total_salary