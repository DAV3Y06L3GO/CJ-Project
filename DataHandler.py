import os
import pickle

class Session():
    
    def __init__(self, id, entries=[]):
        self.id = id
        self.entries = entries

    def getEntryFromName(self, _id):
        for i in self.entries:
            if i.name == _id:
                return i
    
    def getEntryFromInt(self, _id):
        return self.entries[_id]
    

    def dump(self):
        path = f"./data/{self.id}.dat"
        
        if not os.path.exists(path):
            with open(path, "x") as file:
                pass
        
        with open(path, "wb") as file:
            pickle.dump(self, file)

                      
                      
                 




class Entry():

    def __init__(self):
        self.name = None