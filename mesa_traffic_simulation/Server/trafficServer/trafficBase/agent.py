from mesa import Agent
from a_star import a_star_graph

# This map is used to determine the direction of the graph's nodes and the direction they have to take to reach the next node.
direction_map = {
            # Direcciónes desde A
            ("A", "B"): "Right",
            ("A", "D"): "Up",
            ("A", "a"): "Right",
            
            # Direcciónes desde B
            ("B", "C"): "Left",
            ("B", "M"): "Up",
            
            # Direcciónes desde C
            ("C", "c"): "Left",
            ("C", "B"): "Down",
            ("C", "D"): "Left",
            ("C", "a"): "Down",
            
            # Direcciónes desde D
            ("D", "E"): "Left",
            ("D", "I"): "Up",
            
            # Direcciónes desde E
            ("E", "A"): "Down",
            ("E", "d"): "Left",
            ("E", "f"): "Left",
            ("E", "J"): "Left",
            
            # Direcciónes desde H
            ("H", "e"): "Down",
            ("H", "C"): "Down",
            ("H", "M"): "Right",
            
            # Direcciónes desde I
            ("I", "N"): "Up",
            ("I", "g"): "Right",
            ("I", "H"): "Right",
            
            # Direcciónes desde J
            ("J", "I"): "Right",
            ("J", "E"): "Down",
            
            # Direcciónes desde K
            ("K", "J"): "Right",
            ("K", "Z"): "Down",
            
            # Direcciones desde L
            ("L", "K"): "Right",
            ("L", "Z"): "Down",
            
            # Direcciones desde M
            ("M", "N"): "Left",
            ("M", "W"): "Up",
            
            # Direcciones desde N
            ("N", "O"): "Left",
            ("N", "k"): "Up",
            ("N", "R"): "Up",
            
            # Direcciones desde O
            ("O", "h"): "Down",
            ("O", "J"): "Down",
            ("O", "i"): "Left",
            ("O", "L"): "Left",
            
            # Direcciones desde P
            ("P", "O"): "Right",
            ("P", "i"): "Down",
            ("P", "L"): "Down",
            
            # Direcciones desde Q
            ("Q", "L"): "Down",
            ("Q", "p"): "Right",
            ("Q", "m"): "Right",
            ("Q", "j"): "Right",
            ("Q", "P"): "Right",
            
            # Direcciones desde R
            ("R", "l"): "Right",
            ("R", "W"): "Right",
            ("R", "Y"): "Up",
            
            # Direcciones desde T
            ("T", "q"): "Left",
            ("T", "U"): "Left",
            
            # Direcciones desde U
            ("U", "$"): "Up",
            ("U", "n"): "Left",
            ("U", "!"): "Left",
            
            # Direcciones desde X
            ("X", "Q"): "Down",
            ("X", "x"): "Right",
            ("X", "Ñ"): "Right",
            
            # Direcciones desde %
            ("%", "&"): "Right",
            ("%", "T"): "Down",
            ("%", "O"): "Right",
            
            # Direcciones desde $
            ("$", "X"): "Up",
            ("$", "%"): "Right",
            
            # Direcciones desde !
            ("!", "o"): "Left",
            ("!", "Q"): "Left",
            ("!", "m"): "Down",
            ("!", "j"): "Down",
            ("!", "P"): "Down",
            
            # Direcciones desde Ñ
            ("Ñ", "ñ"): "Right",
            ("Ñ", "$"): "Right",
            ("Ñ", "X"): "Up",
            ("Ñ", "!"): "Down",
            
            # Direcciones desde Y
            ("Y", "X"): "Left",
            ("Y", "&"): "Down",
            
            # Direcciones desde W
            ("W", "w"): "Left",
            ("W", "Y"): "Up",
            ("W", "u"): "Up",
            ("W", "Y"): "Left",
            
            # Direcciones desde Z
            ("Z", "b"): "Up",
            ("Z", "f"): "Up",
            ("Z", "A"): "Right",
            ("Z", "J"): "Up",
            
            # Direcciones desde &
            ("&", "T"): "Left",
            ("&", "O"): "Down",
        }

class Car(Agent):
    """
        Car agent. Represents a car moving through the city, it calculates the route to the destination and follows the city's rules.
        
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            graph: Graph representation of the city's intersections and connection between them.
            start_node: The node where the car starts
            destination_mapping: The mapping of the destination to the grid position
            destination: The destination of the car
    """
    def __init__(self, unique_id, model, graph, start_node, destination_mapping, destination):
        super().__init__(unique_id, model)
        self.waiting_at_light = False  # Flag to indicate if the car is waiting at a red light
        self.last_direction = None  # Saves the last valid direction the car took
        self.destination = None  # Closest point to the destination
        self.at_intersection = False # Flag to indicate if the car is at an intersection
        self.reaching_destination = False # Flag to indicate if the car is reaching the destination
        self.route_calculated = False # Flag to indicate if the route has been calculated
        self.final_destination = None # Final destination of the car
        self.route = [] # Route to the destination
        self.graph = graph # City's graph
        self.initial_node = start_node # Initial node of the car
        self.destination_mapping = destination_mapping # Mapping of the destination to the grid position
        self.final_destination_verification = destination # Final Destination's position of the car
    
    def calculate_route(self):
        """Calculates the route to the destination using the A* algorithm."""
        path = a_star_graph(self.graph, self.initial_node, self.destination)  # Route as a list of nodes

        # Converts the path to a list of directions
        self.route = []
        for i in range(len(path) - 1):
            current, next_node = path[i], path[i + 1]
            direction = direction_map.get((current, next_node), None)
            self.route.append(direction)
        
    def choose_direction_based_on_route(self, options):
        """
            Gives the car the direction to take based on the route to the destination.
            
            Args:
                options: The possible directions the car can take.
        """
        if not self.route:
            return None  # If there are no directions in the route, return None

        next_direction = self.route[0]  # Obtains the next direction from the route

        # Verifies if the next direction is in the options
        if next_direction in options:
            return next_direction

        return None  # If the next direction is not in the options, return None

    def contains_destination(self, pos):
        """Checks if there is a Destination agent in the given position.

        Args:
            pos: The position to check for Destination agents.
        """
        items = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(item, Destination) for item in items)

    def move_towards_final_destination(self):
        """
            When the car is reaching the destination, it moves towards the final destination.
        """
        # Verifies if the final destination is set
        if not self.final_destination:
            return

        # Verifies if the car is near the final destination
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        looking_destination = [pos for pos in neighborhood if self.contains_destination(pos)
                               and pos == self.final_destination_verification.get(self.destination)]

        # If the car is near the final destination then move to the final destination
        if looking_destination:
            dest_pos = looking_destination[0]
            print(f"Car {self.unique_id}: Moving to final destination ('?') at {dest_pos}.")
            self.model.grid.move_agent(self, dest_pos)
            return

        # If the car is not near the final destination, then move towards the final destination
        current_x, current_y = self.pos
        target_x, target_y = self.final_destination

        # Calculates the direction to move
        if current_x < target_x:
            direction = "Right"
        elif current_x > target_x:
            direction = "Left"
        elif current_y < target_y:
            direction = "Down"
        elif current_y > target_y:
            direction = "Up"
        else:
            return

        # Calculates the next position
        if direction == "Right":
            next_pos = (current_x + 1, current_y)
        elif direction == "Left":
            next_pos = (current_x - 1, current_y)
        elif direction == "Down":
            next_pos = (current_x, current_y + 1)
        elif direction == "Up":
            next_pos = (current_x, current_y - 1)

        # Verifies if there is a Traffic Light in the next position
        next_cell_agents = self.model.grid.get_cell_list_contents(next_pos)
        traffic_light = next((a for a in next_cell_agents if isinstance(a, Traffic_Light)), None)

        # If there is a Traffic Light in the next position then wait
        if traffic_light:
            if not traffic_light.state:  # If the Traffic Light is red
                self.waiting_at_light = True # Set the waiting_at_light flag to True
                return
            else:
                self.waiting_at_light = False # Set the waiting_at_light flag to False

        # Verifies if there is a Car in the next position
        if any(isinstance(a, Car) for a in next_cell_agents):
            return  # If there is a Car in the next position then don't move

        # Moves the car to the next position
        self.model.grid.move_agent(self, next_pos)

        
    def get_previous_direction(self):
        """
            Obtains the previous direction the car took.
        """
        # Map of the last neighbor based on the last direction
        directions = {
            "Right": (-1, 0),
            "Left": (1, 0),
            "Down": (0, 1),
            "Up": (0, -1),
        }

        # Verifies if the last direction is valid
        if not self.last_direction or self.last_direction not in directions:
            return None 

        # Obtains the previous position
        dx, dy = directions[self.last_direction]
        previous_pos = (self.pos[0] + dx, self.pos[1] + dy)
        previous_road = next(
            (a for a in self.model.grid.get_cell_list_contents(previous_pos) if isinstance(a, Road)),
            None
        )
        return previous_road.direction if previous_road else None # Returns the previous direction
    
    def move(self):
        """
            Moves the car through the city. It follows the city's rules and the route to the destination.
        """
        # Verifies if the car is reaching the destination
        if self.reaching_destination:
            self.move_towards_final_destination()
            print(f"Car {self.unique_id}: Moving towards final destination.")
            return
        
        # Verifies if the car is near the final destination
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        looking_destination = [pos for pos in neighborhood if self.contains_destination(pos)
                               and pos == self.final_destination_verification.get(self.destination)]

        # If the car is near the final destination then move to the final destination
        if looking_destination:
            dest_pos = looking_destination[0]  # Obtener la posición del Destination
            print(f"Car {self.unique_id}: Moving to final destination ('?') at {dest_pos}.")
            self.model.grid.move_agent(self, dest_pos)
            return
        
        # Filters the agents in the next position
        road_agent = next((a for a in self.model.grid.get_cell_list_contents(self.pos) if isinstance(a, Road)), None)
        direction = road_agent.direction if road_agent else None
        
        # Verifies if the car is at an intersection 
        last_neighbor_map = {
        "Right": (-1, 0),
        "Left": (1, 0),
        "Down": (0, 1),
        "Up": (0, -1)
        }
        
        opposite_neighbor = None
        # If the last direction is in the last neighbor map then obtain the opposite neighbor
        if self.last_direction in last_neighbor_map:
            dx, dy = last_neighbor_map[self.last_direction]
            opposite_neighbor = (self.pos[0] + dx, self.pos[1] + dy)

        # Verifies if the car is at an intersection and the opposite neighbor is a Road to consume the route direction
        if opposite_neighbor:
            previous_road = next(
                (a for a in self.model.grid.get_cell_list_contents(opposite_neighbor) if isinstance(a, Road)), None
            )
            # If the opposite neighbor is a Road with a list direction and the car is not waiting at a red light
            if (
                previous_road and isinstance(previous_road.direction, list)  # Opposite neighbor is a Road with a list direction
                and not isinstance(direction, list) # Current direction is not a list
                and not self.waiting_at_light # Car is not waiting at a red light
            ):
                if self.route:
                    self.route.pop(0) # Consume the route direction

        # If the car is at an intersection obtain the possible directions
        if isinstance(direction, list):
    
            # Chooose the direction based on the route
            if self.destination:
                direction = self.choose_direction_based_on_route(direction)

        # If the car is not at an intersection then obtain the possible directions
        if not direction:
            # Si no encuentra una dirección, usa la última dirección válida o revisa detrás
            direction = self.get_previous_direction()

        # Calculates the next position based on the direction
        if direction == "Right":
            next_pos = (self.pos[0] + 1, self.pos[1])
        elif direction == "Left":
            next_pos = (self.pos[0] - 1, self.pos[1])
        elif direction == "Down":
            next_pos = (self.pos[0], self.pos[1] - 1)
        elif direction == "Up":
            next_pos = (self.pos[0], self.pos[1] + 1)

        # Verifies if the next position is a Traffic Light
        next_cell_agents = self.model.grid.get_cell_list_contents(next_pos)
        traffic_light = next((a for a in next_cell_agents if isinstance(a, Traffic_Light)), None)

        # If the next position is a Traffic Light then wait
        if traffic_light:
            if not traffic_light.state:  # Traffic Light is red
                print(f"Car {self.unique_id}: Waiting at red light at {next_pos}")
                self.waiting_at_light = True # Set the waiting_at_light flag to True
                return
            else:
                self.waiting_at_light = False # Set the waiting_at_light flag to False

        # Verifies if the next position is a Car
        if any(isinstance(a, Car) for a in next_cell_agents):
            print(f"Car {self.unique_id}: Next position {next_pos} is occupied")
            return  # If the next position is a Car then don't move

        # Keep track of the last valid direction
        self.last_direction = direction

        # Move the car to the next position
        self.model.grid.move_agent(self, next_pos)
        print(f"Car {self.unique_id}: Moved to {next_pos}")

    def step(self):
        """
            Advances the car by one step. It calculates the route to the destination and moves the car through the city.
        """
        # Verifies if the final destination is set if not then set it
        if self.final_destination is None:
            # Obtener la posición final basada en la letra del destino
            self.final_destination = self.destination_mapping.get(self.destination)
            print(self.final_destination)
            if self.final_destination is None:
                print(f"Car {self.unique_id}: Final destination not found in mapping.")
                return            
        
        # Verifies if the car has reached the final destination and removes it from the map
        cell_agents = self.model.grid.get_cell_list_contents(self.pos)
        if any(isinstance(agent, Destination) for agent in cell_agents):
            print(f"Car {self.unique_id}: Reached final destination at {self.pos}. Removing from map.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.cars_reached_destination += 1
            return

        # Verifies if the car has not calculated the route
        if not self.route and not self.route_calculated:
            self.calculate_route()
            self.route_calculated = True
            print(f"Car {self.unique_id}: Calculated route: {self.route}")
            
        # Verifies if the car is about to reach the destination
        if not self.route and self.route_calculated:
            self.reaching_destination = True
            print(f"Car {self.unique_id}: Route is empty. Activating reaching_destination.")
        
        print(f"Car {self.unique_id}: Moving along route: {self.route}")
        self.move() # Move the car

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
    
class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass