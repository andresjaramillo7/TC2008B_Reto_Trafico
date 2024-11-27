from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import random
import json

graph = {
    'A': ['a','B','F'],
    'B': ['G','F'],
    'C': ['B','b', 'A'],
    'D': ['c', 'd', 'C', 'A'],
    'E': ['D', 'A'],
    'F': ['G', 'l', 'K'],
    'G': ['H', 'e', 'j', 'K'],
    'H': ['I'],
    'I': ['E', 'g', 'i', 'h'],
    'J': ['i', 'h', 'E', 'f', 'H'],
    'K': ['m', 'h', 'E', 'k', 'J'],
    'a': [],
    'b': [],
    'c': [],
    'd': [],
    'e': [],
    'f': [],
    'g': [],
    'h': [],
    'i': [],
    'j': [],
    'k': [],
    'l': [],
    'm': []
}

destination_positions = {
    'a': (19, 1),
    'b': (13, 4),
    'c': (6, 4),
    'd': (10, 8),
    'e': (17, 14),
    'f': (13, 15),
    'g': (6, 15),
    'h': (1, 15),
    'i': (3, 18),
    'j': (17, 20),
    'k': (13, 20),
    'l': (22, 22),
    'm': (3, 23)
}

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))
        self.graph = graph
        print ("grafo creado: ", self.graph)

        self.traffic_lights = []
        self.destinations = []
        self.destination_positions = destination_positions

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                               "K", "a", "b","c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "?":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))

        self.num_agents = N
        self.running = True
        self.current_step = 0
        self.next_id = 1000
        
        for i in range(self.num_agents):
            pos = [(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)]
            initial_node = ["A", "E", "F", "K"]
            a = Car(self.next_id, self, graph = self.graph, start_node = initial_node[i], destination_mapping = self.destination_positions)
            
            a.destination = random.choice(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]) # Asigna un destino aleatorio
            print(f"Auto {self.next_id} creado con destino {a.destination}")
            
            self.next_id += 1
            self.schedule.add(a)
            self.grid.place_agent(a, pos[i])


    def step(self):
        '''Advance the model by one step.'''
        self.current_step += 1
        if self.current_step % 10 == 0:
            for i in range(4):
                pos = [(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)]
                initial_node = ["A", "E", "F", "K"]
                a = Car(self.next_id, self, graph = self.graph, start_node = initial_node[i], destination_mapping = self.destination_positions)
                
                a.destination = random.choice(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]) # Asigna un destino aleatorio
                print(f"Auto {self.next_id} creado con destino {a.destination}")
                
                self.next_id += 1
                self.schedule.add(a)
                self.grid.place_agent(a, pos[i])
        self.schedule.step()