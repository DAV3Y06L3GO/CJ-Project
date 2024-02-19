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
    


    
    def constructEntry(self, name, gps, date, genus, species, substrate, terrain, gill, other):
        self.entries.append(Entry(name, gps, date, genus, species, substrate, terrain, gill, other))





    def dump(self):
        path = f"./data/sessions/{self.id}.dat"
        
        if not os.path.exists(path):
            with open(path, "x") as file:
                pass
        
        with open(path, "wb") as file:
            pickle.dump(self, file)

                      
                      
                 




class Entry():

    def __init__(self, name, gps, date, genus, species, substrate, terrain, gill, other):
        self.name = name
        self.gps = gps
        self.date = date
        self.genus = genus
        self.species = species
        self.substrate = substrate
        self.terrain = terrain
        self.gill = gill
        self.other = other