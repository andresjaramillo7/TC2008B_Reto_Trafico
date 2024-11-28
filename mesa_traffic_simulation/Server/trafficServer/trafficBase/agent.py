from mesa import Agent
from a_star import a_star_graph

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
    def __init__(self, unique_id, model, graph, start_node, destination_mapping, destination):
        super().__init__(unique_id, model)
        self.waiting_at_light = False  # Flag para manejar semáforos
        self.last_direction = None  # Guarda la última dirección válida
        self.destination = None  # Guarda la posición de destino
        self.at_intersection = False
        self.reaching_destination = False
        self.route_calculated = False
        self.final_destination = None
        self.route = []
        self.graph = graph
        self.initial_node = start_node
        self.destination_mapping = destination_mapping
        self.final_destination_verification = destination
    
    def calculate_route(self):
        """Calcula la ruta desde el nodo inicial hasta el destino."""
        path = a_star_graph(self.graph, self.initial_node, self.destination)  # Ruta como lista de nodos
        print(f"Car {self.unique_id}: Calculated path: {path}")

        # Convertir la ruta de nodos en direcciones
        self.route = []
        for i in range(len(path) - 1):
            current, next_node = path[i], path[i + 1]
            direction = direction_map.get((current, next_node), None)
            self.route.append(direction)
        print(f"Car {self.unique_id}: Route: {self.route}")
        
    def choose_direction_based_on_route(self, options):
        """
        Decide la dirección basándose en la lista predefinida de direcciones (self.route).
        """
        if not self.route:
            return None  # Si no hay más direcciones, no se toma ninguna decisión

        next_direction = self.route[0]  # Obtener la próxima dirección de la ruta

        # Verificar si la próxima dirección está disponible en las opciones de la intersección
        if next_direction in options:
            return next_direction

        print(f"Car {self.unique_id}: Next direction {next_direction} not available in options {options}.")
        return None  # Si la próxima dirección no está en las opciones, no hacer nada

    def contains_destination(self, pos):
        """Checks if there is any trash in the specified grid cell.

        Args:
            pos: The grid position to check for trash.
        """
        items = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(item, Destination) for item in items)

    def move_towards_final_destination(self):
        """
        Mueve el auto hacia las coordenadas de self.final_destination.
        Cuando llega al lado de la celda de Destination, se mueve hacia esa celda y se elimina.
        """
        if not self.final_destination:
            print(f"Car {self.unique_id}: Final destination not set. Cannot move.")
            return

        # Verificar si el agente ya está al lado del Destination
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        looking_destination = [pos for pos in neighborhood if self.contains_destination(pos)
                               and pos == self.final_destination_verification.get(self.destination)]

        # Si está al lado del Destination
        if looking_destination:
            dest_pos = looking_destination[0]  # Obtener la posición del Destination
            print(f"Car {self.unique_id}: Moving to final destination ('?') at {dest_pos}.")
            self.model.grid.move_agent(self, dest_pos)
            return

        # Si no está al lado del Destination, moverse hacia self.final_destination
        current_x, current_y = self.pos
        target_x, target_y = self.final_destination

        # Calcular la dirección basada en las coordenadas
        if current_x < target_x:
            direction = "Right"
        elif current_x > target_x:
            direction = "Left"
        elif current_y < target_y:
            direction = "Down"
        elif current_y > target_y:
            direction = "Up"
        else:
            # Ya está en la posición final
            print(f"Car {self.unique_id}: Reached the position near the final destination at {self.pos}.")
            return

        # Calcular la posición siguiente
        if direction == "Right":
            next_pos = (current_x + 1, current_y)
        elif direction == "Left":
            next_pos = (current_x - 1, current_y)
        elif direction == "Down":
            next_pos = (current_x, current_y + 1)
        elif direction == "Up":
            next_pos = (current_x, current_y - 1)

        # Verificar si hay semáforo en la posición siguiente
        next_cell_agents = self.model.grid.get_cell_list_contents(next_pos)
        traffic_light = next((a for a in next_cell_agents if isinstance(a, Traffic_Light)), None)

        if traffic_light:
            if not traffic_light.state:  # Semáforo en rojo
                print(f"Car {self.unique_id}: Waiting at red light at {next_pos}")
                self.waiting_at_light = True
                return
            else:
                self.waiting_at_light = False

        # Verificar si la celda está ocupada por otro auto
        if any(isinstance(a, Car) for a in next_cell_agents):
            print(f"Car {self.unique_id}: Next position {next_pos} is occupied by another car.")
            return  # No avanzar si está ocupado

        # Mover al auto
        print(f"Car {self.unique_id}: Moving from {self.pos} to {next_pos}.")
        self.model.grid.move_agent(self, next_pos)

        
    def get_previous_direction(self):
        """
        Busca la dirección válida en las celdas detrás del auto.
        """
        directions = {
            "Right": (-1, 0),
            "Left": (1, 0),
            "Down": (0, 1),
            "Up": (0, -1),
        }

        if not self.last_direction or self.last_direction not in directions:
            return None 

        # Calcula la celda detrás del auto
        dx, dy = directions[self.last_direction]
        previous_pos = (self.pos[0] + dx, self.pos[1] + dy)
        previous_road = next(
            (a for a in self.model.grid.get_cell_list_contents(previous_pos) if isinstance(a, Road)),
            None
        )
        return previous_road.direction if previous_road else None
    
    def move(self):
        if self.reaching_destination:
            self.move_towards_final_destination()
            print(f"Car {self.unique_id}: Moving towards final destination.")
            return
        
        # neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        # looking_destination = [pos for pos in neighborhood if self.contains_destination(pos)
        #                        and pos == self.final_destination_verification.get(self.destination)]

        # # Si está al lado del Destination
        # if looking_destination:
        #     dest_pos = looking_destination[0]  # Obtener la posición del Destination
        #     print(f"Car {self.unique_id}: Moving to final destination ('?') at {dest_pos}.")
        #     self.model.grid.move_agent(self, dest_pos)
        #     return
        
        # Filtra para encontrar el agente Road en la celda actual
        road_agent = next((a for a in self.model.grid.get_cell_list_contents(self.pos) if isinstance(a, Road)), None)
        direction = road_agent.direction if road_agent else None
        
        last_neighbor_map = {
        "Right": (-1, 0),
        "Left": (1, 0),
        "Down": (0, 1),
        "Up": (0, -1)
        }
        
        opposite_neighbor = None
        if self.last_direction in last_neighbor_map:
            dx, dy = last_neighbor_map[self.last_direction]
            opposite_neighbor = (self.pos[0] + dx, self.pos[1] + dy)

        # Verificar si el vecino opuesto era una intersección y el actual no lo es
        if opposite_neighbor:
            previous_road = next(
                (a for a in self.model.grid.get_cell_list_contents(opposite_neighbor) if isinstance(a, Road)), None
            )
            if (
                previous_road and isinstance(previous_road.direction, list)  # Vecino opuesto era una intersección
                and not isinstance(direction, list)
                and not self.waiting_at_light# Dirección actual no es una lista (salió de la intersección)
            ):
                print(f"Car {self.unique_id}: Exiting intersection. Consuming route direction.")
                if self.route:
                    self.route.pop(0)  # Consumir la dirección actual de la ruta
                    print(f"Car {self.unique_id}: Route after pop: {self.route}")

        # Si la dirección es una lista (intersección), obtén las opciones
        if isinstance(direction, list):
            print(f"Car {self.unique_id}: At intersection {self.pos} with options {direction}")
    
            # Elegir dirección basándose en el destino
            if self.destination:  # Si el auto tiene un destino
                direction = self.choose_direction_based_on_route(direction)

        if not direction:
            # Si no encuentra una dirección, usa la última dirección válida o revisa detrás
            print(f"Car {self.unique_id}: No direction found at {self.pos}, checking previous direction...")
            direction = self.get_previous_direction()

        # Calcula la posición siguiente
        if direction == "Right":
            next_pos = (self.pos[0] + 1, self.pos[1])
        elif direction == "Left":
            next_pos = (self.pos[0] - 1, self.pos[1])
        elif direction == "Down":
            next_pos = (self.pos[0], self.pos[1] - 1)
        elif direction == "Up":
            next_pos = (self.pos[0], self.pos[1] + 1)
        
        print(f"Car {self.unique_id}: Trying to move from {self.pos} to {next_pos} (Direction: {direction})")

        # Verificar si hay semáforo en la posición siguiente
        next_cell_agents = self.model.grid.get_cell_list_contents(next_pos)
        traffic_light = next((a for a in next_cell_agents if isinstance(a, Traffic_Light)), None)
        if road_agent and not isinstance(road_agent.direction, list):
            self.at_intersection = False

        if traffic_light:
            if not traffic_light.state:  # Semáforo en rojo
                print(f"Car {self.unique_id}: Waiting at red light at {next_pos}")
                self.waiting_at_light = True
                return
            else:
                self.waiting_at_light = False

        # Verificar si la celda está ocupada por otro auto
        if any(isinstance(a, Car) for a in next_cell_agents):
            print(f"Car {self.unique_id}: Next position {next_pos} is occupied")
            return  # No avanzar si está ocupado

        # Actualizar la última dirección válida antes de moverse
        self.last_direction = direction

        # Mover al auto
        self.model.grid.move_agent(self, next_pos)
        print(f"Car {self.unique_id}: Moved to {next_pos}")

    def step(self):
        if self.final_destination is None:
            # Obtener la posición final basada en la letra del destino
            self.final_destination = self.destination_mapping.get(self.destination)
            print(self.final_destination)
            if self.final_destination is None:
                print(f"Car {self.unique_id}: Final destination not found in mapping.")
                return            
        cell_agents = self.model.grid.get_cell_list_contents(self.pos)
        if any(isinstance(agent, Destination) for agent in cell_agents):
            print(f"Car {self.unique_id}: Reached final destination at {self.pos}. Removing from map.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.cars_reached_destination += 1
            return
        if not self.route and not self.route_calculated:
            self.calculate_route()
            self.route_calculated = True
            print(f"Car {self.unique_id}: Calculated route: {self.route}")
            
        if not self.route and self.route_calculated:
            self.reaching_destination = True
            print(f"Car {self.unique_id}: Route is empty. Activating reaching_destination.")
        
        print(f"Car {self.unique_id}: Moving along route: {self.route}")
        self.move()

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