import pickle

from GraphManager import Graphmanager

def storeData(graphManager:Graphmanager):
    # Its important to use binary mode
    dbfile = open('examplePickle', 'wb')
    
    # source, destination
    pickle.dump(graphManager, dbfile)                    
    dbfile.close()

def loadData() -> Graphmanager:
    # for reading also binary mode is important
    dbfile = open('examplePickle', 'rb')    
    db = pickle.load(dbfile)
    dbfile.close()
    return db
    
  