from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from agent import *
import random
import json
import requests

# Graph representation of the city's intersections and connection between them.
graph = {
    'A': ['a', 'B', 'D'],
    'B': ['C', 'M'],
    'C': ['B', 'D', 'c'],
    'D': ['E', 'I'],
    'E': ['A', 'd', 'f', 'J'],
    'H': ['e', 'C', 'M'],
    'I': ['N', 'g', 'H'],
    'J': ['I', 'E'],
    'K': ['J', 'Z'],
    'L': ['K', 'Z'],
    'M': ['N', 'W'],
    'N': ['O', 'k', 'R'],
    'O': ['h', 'J', 'i', 'L'],
    'P': ['O', 'i', 'L'],
    'Q': ['L', 'p', 'm', 'j', 'P'],
    'R': ['l', 'W', 'Y'],
    'T': ['q', 'U'],
    'U': ['$', 'n', '!'],
    'X': ['Q', 'x', 'Ñ'],
    '%': ['&', 'T', 'O'],
    '$': ['X', '%'],
    '!': ['o', 'Q', 'm', 'j', 'P'],
    'Ñ': ['ñ', '$', 'X', '!'],
    'Y': ['X', '&'],
    'W': ['w', 'Y', 'u'],
    'Z': ['b', 'J', 'f', 'A'],
    '&': ['T', 'O'],
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
    'm': [],
    'n': [],
    'o': [],
    'p': [],
    'q': [],
    'u': [],
    'w': [],
    'x': [],
    'ñ': [],
    'n': [],
}

# Dictionary that gives each character a position of the closest point to the Destination in the map.
destination_positions = {
    'a': (25, 1),
    'b': (7, 4),
    'c': (18, 6),
    'd': (9, 7),
    'e': (21, 10),
    'f': (7, 10),
    'g': (21, 13),
    'h': (11, 15),
    'i': (7, 18),
    'j': (7, 20),
    'k': (16, 20),
    'l': (25, 22),
    'm': (6, 18),
    'o': (3, 22),
    'p': (3, 20),
    'q': (9, 22),
    'u': (22, 28),
    'w': (22, 26),
    'x': (3, 25),
    'ñ': (6, 25),
    'n': (6, 22),
}

# Dictionary that gives each character the Destination in the map.
final_positions = {
    'a': (25, 2),
    'b': (8, 4),
    'c': (18, 5),
    'd': (9, 8),
    'e': (20, 10),
    'f': (8, 10),
    'g': (21, 14),
    'h': (10, 15),
    'i': (7, 19),
    'j': (7, 19),
    'k': (17, 20),
    'l': (25, 21),
    'm': (6, 21),
    'o': (3, 21),
    'p': (3, 21),
    'q': (9, 23),
    'u': (22, 27),
    'w': (22, 27),
    'x': (3, 24),
    'ñ': (6, 26),
    'n': (6, 21),
}

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open('city_files/mapDictionary.json'))
        self.graph = graph # Graph representation of the city's intersections and connection between them.
        self.traffic_lights = [] # List of traffic lights in the city.
        self.destinations = [] # List of destination points in the city.
        self.destination_positions = destination_positions # Dictionary that gives each character a position of the closest point to the Destination in the map.
        self.final_positions = final_positions # Dictionary that gives each character the Destination in the map.
        self.total_cars_spawned = 0 # Total number of cars spawned in the simulation.
        self.cars_reached_destination = 0 # Total number of cars that reached their destination.

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/2024_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            print("width: ", self.width, "height: ", self.height)

            # Create the grid and scheduler.
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = BaseScheduler(self)

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "A", "B", "C", "D", "E", "H", "I", "J",
                               "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U", "!", "W", "%",
                               "$", "Ñ", "X", "Y", "&", "Z", "a", "b", "c", "d", "e", "f", "g",
                               "h", "i", "j", "k", "l", "m", "o", "p", "q", "u", "w", "x", "ñ",
                               "n"]:
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

        # Create the agents in the simulation.
        self.num_agents = N
        self.running = True
        self.current_step = 0
        self.next_id = 1000
        
        """
            Create the agents in the simulation. Each agent is placed in a corner of the map. And is given a random destination.
            
            Args:
                num_agents: Number of agents to create.
        """
        for i in range(self.num_agents):
            pos = [(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)] # Position of each agent
            initial_node = ["Z", "X", "B", "Y"] # Initial node for each agent
            a = Car(self.next_id, self, graph = self.graph, start_node = initial_node[i],
                    destination_mapping = self.destination_positions, destination = self.final_positions) # Creates a new agent with
                                                                                                          # the given parameters
            a.destination = random.choice(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                                           "l", "m","o", "p", "q", "u", "w", "x", "ñ", "n"]) # Assigns a random destination
            
            self.next_id += 1 # Increments the next id to create a unique id for each agent
            self.schedule.add(a) # Adds the agent to the scheduler
            self.grid.place_agent(a, pos[i]) # Places the agent in the grid
            self.total_cars_spawned += 1 # Increments the total number of cars spawned

    def step(self):
        '''Advance the model by one step.'''
        self.current_step += 1
        """
            Create a new agent every 10 steps. Each agent is placed in a corner of the map. And is given a random destination
            
            Args:
                num_agents: Number of agents to create.
        """
        if self.current_step % 10 == 0:
            for i in range(4):
                pos = [(0, 0), (0, self.height - 1), (self.width - 1, 0), (self.width - 1, self.height - 1)] # Position of each agent
                initial_node = ["Z", "X", "B", "Y"] # Initial node for each agent
                a = Car(self.next_id, self, graph = self.graph, start_node = initial_node[i],
                        destination_mapping = self.destination_positions, destination = self.final_positions) # Creates a new agent with
                                                                                                            # the given parameters
                a.destination = random.choice(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                                            "l", "m","o", "p", "q", "u", "w", "x", "ñ", "n"]) # Assigns a random destination
                
                self.next_id += 1 # Increments the next id to create a unique id for each agent
                self.schedule.add(a) # Adds the agent to the scheduler
                self.grid.place_agent(a, pos[i]) # Places the agent in the grid
                self.total_cars_spawned += 1 # Increments the total number of cars spawned
                
        """
            Send the data to the server every 10 steps.
            
            This is commented out because the server challenge is not running and it causes errors.
        """
        
        # if self.current_step % 10 == 0:    
        #     url = "http://10.49.12.55:5000/api/"
        #     endpoint = "attempt"

        #     data = {
        #         "year": 2024,
        #         "classroom": 301,
        #         "name": "Umizumi",
        #         "current_cars": self.total_cars_spawned,
        #         "total_arrived": self.cars_reached_destination
        #     }
            
        #     headers = {
        #         "Content-Type": "application/json"
        #     }
            
        #     response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)
        #     print("Request " + "succesful" if response.status_code == 200 else "failed", "Status code: ", response.status_code)
        #     print("Response:", response.json())

        self.schedule.step()