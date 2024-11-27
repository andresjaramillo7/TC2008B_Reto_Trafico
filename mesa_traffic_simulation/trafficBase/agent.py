from mesa import Agent
import math

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.waiting_at_light = False  # Flag para manejar semáforos
        self.last_direction = None  # Guarda la última dirección válida
        self.destination = None  # Guarda la posición de destino
        self.route = []
        
    def get_distance(self, pos_1, pos_2):
        """Calcula la distancia euclidiana entre dos puntos."""
        x1, y1 = pos_1
        x2, y2 = pos_2
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def choose_direction_based_on_goal(self, options):
        """
        Decide la dirección basándose en el destino del auto.
        """
        current_x, current_y = self.pos
        goal_x, goal_y = self.destination

        if "Up" in options and goal_y > current_y:
            return "Up"
        if "Down" in options and goal_y < current_y:
            return "Down"
        if "Right" in options and goal_x > current_x:
            return "Right"
        if "Left" in options and goal_x < current_x:
            return "Left"

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
        # Filtra para encontrar el agente Road en la celda actual
        road_agent = next((a for a in self.model.grid.get_cell_list_contents(self.pos) if isinstance(a, Road)), None)
        direction = road_agent.direction if road_agent else None

        # Si la dirección es una lista (intersección), obtén las opciones
        if isinstance(direction, list):
            print(f"Car {self.unique_id}: At intersection {self.pos} with options {direction}")
            # Elegir dirección basándose en el destino
            if self.destination:  # Si el auto tiene un destino
                direction = self.choose_direction_based_on_goal(direction)

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
        else:
            print(f"Car {self.unique_id}: Invalid direction '{direction}' at {self.pos}")
            return

        print(f"Car {self.unique_id}: Trying to move from {self.pos} to {next_pos} (Direction: {direction})")

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
            print(f"Car {self.unique_id}: Next position {next_pos} is occupied")
            return  # No avanzar si está ocupado

        # Actualizar la última dirección válida antes de moverse
        self.last_direction = direction

        # Mover al auto
        self.model.grid.move_agent(self, next_pos)
        print(f"Car {self.unique_id}: Moved to {next_pos}")

    def step(self):
        """Determines the new direction it will take, and then moves."""
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