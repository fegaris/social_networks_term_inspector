from pymongo import MongoClient
from datetime import datetime

class Connection(object):
    def __init__(self, **kwargs):
        defaultAttr = dict(serverName = 'localhost', port = 27017, logDestination = '')

        allowedAttr = list(defaultAttr.keys())
        defaultAttr.update(kwargs)

        for key in defaultAttr:
            if key in allowedAttr:
                self.__dict__[key] = defaultAttr.get(key)

        self.client = MongoClient(self.serverName, self.port)

    def insert(self, database, collection, query):
        self.client[database][collection].insert_one(query)
    
    def multipleInsert(self, database, collection, query):
        self.client[database][collection].insert_many(query)

    def select(self, database, collection, query):
        return self.client[database][collection].find(query)

    def insertCompanies(self, database, collection):
        self.client[database][collection].insert_many([
            {'timestamp': datetime.now(), 'Business': 'ACCIONA', 'InstagramUsername': 'acciona', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ACERINOX', 'InstagramUsername': 'grupoacerinox', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ACS', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'AENA', 'InstagramUsername': 'aena.es', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ALMIRALL', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'AMADEUS', 'InstagramUsername': 'amadeusitgroup', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ARCELORMITTAL', 'InstagramUsername': 'arcelormittalgroup', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'B. SANTANDER', 'InstagramUsername': 'santander_es', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'BANCO SABADELL', 'InstagramUsername': 'bancosabadell', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'BANKINTER', 'InstagramUsername': 'bankinter', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'BBVA', 'InstagramUsername': 'bbva', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'CAIXABANK', 'InstagramUsername': 'caixabank', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'CELLNEX TELECOM', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'CIE AUTOMOTIVE', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ENAGAS', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ENDESA', 'InstagramUsername': 'endesa', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'FERROVIAL', 'InstagramUsername': 'ferrovial', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'FLUIDRA', 'InstagramUsername': 'fluidraprojects', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'GRIFOLS', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'IAG', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'IBERDROLA', 'InstagramUsername': 'iberdrola', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'INDITEX', 'InstagramUsername': 'inditex', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'INDRA', 'InstagramUsername': 'indracompany', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'INMOBILIARIA COLONIAL', 'InstagramUsername': 'inmocolonial', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'MAPFRE', 'InstagramUsername': 'mapfre', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'MELIÁ HOTELS', 'InstagramUsername': 'meliahtlresorts', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'MERLIN PROPERTIES', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'NATURGY', 'InstagramUsername': 'naturgy', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'PHARMAMAR', 'InstagramUsername': 'pharmamar', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'RED ELÉCTRICA (R.E.C.)', 'InstagramUsername': 'redelectrica', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'REPSOL', 'InstagramUsername': 'repsol', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'ROVI', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'SIEMENS GAMESA', 'InstagramUsername': 'siemensgamesa', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'SOLARIA ENERGIA Y MEDIO AMBIENTE', 'InstagramUsername': '', 'Active': 1}
            ,{'timestamp': datetime.now(), 'Business': 'TELEFÓNICA', 'InstagramUsername': 'telefonica', 'Active': 1}])

    """
    TO DO
        # DELETE
        # DELETE MANY
        # UPDATE
    """