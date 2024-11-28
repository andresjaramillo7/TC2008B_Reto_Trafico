import heapq

def a_star_graph(graph, start, goal):
    """
    Algoritmo A* para un grafo representado como diccionario.
    :param graph: Grafo como diccionario (nodo -> lista de vecinos).
    :param start: Nodo inicial (str).
    :param goal: Nodo destino (str).
    :return: Lista con la ruta más corta en forma de nodos.
    """
    # Inicializar estructuras de datos
    open_set = []  # Priority queue
    heapq.heappush(open_set, (0, start))  # (f_score, nodo)
    
    came_from = {}  # Para reconstruir la ruta
    g_score = {node: float('inf') for node in graph}  # Costo del inicio al nodo
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}  # f(n) = g(n) + h(n)
    f_score[start] = 0  # Suponiendo heurística cero para ahora (peso uniforme)

    while open_set:
        # Nodo con menor f_score
        current = heapq.heappop(open_set)[1]
        
        # Si alcanzamos el destino
        if current == goal:
            # Reconstruir la ruta desde el destino al inicio
            route = []
            while current in came_from:
                route.append(current)
                current = came_from[current]
            route.append(start)  # Agregar el inicio
            route.reverse()  # Ruta desde el inicio al destino
            return route

        # Evaluar vecinos
        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + 1  # Peso uniforme para cada conexión
            if tentative_g_score < g_score[neighbor]:  # Si encontramos una mejor ruta
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor]  # Heurística opcional aquí
                # Agregar a open_set si no está ya
                if all(neighbor != item[1] for item in open_set):
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Si no se encuentra ruta