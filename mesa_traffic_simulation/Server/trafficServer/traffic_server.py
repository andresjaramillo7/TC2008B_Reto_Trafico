# TC2008B Sistemas Multiagentes y Gráficas Computacionales
# Servidor de Python en Flask para comunicarse con WebGL

# Simulación de Movilidad Urbana

# Rodrigo Sosa Rojas / A01027913
# Andrés Jaramillo Barón / A01029079

from flask import  Flask, request, jsonify
from flask_cors import CORS, cross_origin
from trafficBase.model import CityModel
from trafficBase.agent import Road, Traffic_Light,Obstacle, Destination, Car

number_agents = 10
width = 28
height = 28
cityModel = None
currentStep = 0

app = Flask("Movilidad Urbana")
cors = CORS(app, origins=['http://localhost'])

@app.route('/init', methods=['POST'])
@cross_origin()
def initModel():
    global currentStep, cityModel, number_agents, width, height

    if request.method == 'POST':
        try:

            number_agents = int(request.json.get('NAgents'))
            width = int(request.json.get('width'))
            height = int(request.json.get('height'))
            currentStep = 0

            print(request.json)
            print(f"Parámetros del modelo:{number_agents, width, height}")

            cityModel = CityModel(number_agents, width, height)

            return jsonify({"message":"Parámetros recibidos. Iniciando simulación..."})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error, inicializando el modelo"}), 500
        
@app.route('/getCars', methods = ['GET'])
@cross_origin()
def getCars():
    global cityModel

    if request.method == 'GET':
        try:
            CarPositions = [
                {"id": str(a.unique_id), "x": x, "y": 1, "z": z}
                for a, (x,z) in cityModel.grid.coord_iter()
                if isinstance(a, Car)]
            return jsonify({'posiciones de los autos': CarPositions})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al obtener las posiciones de los autos"}), 500
        
        
@app.route('/getObstacles', methods = ['GET'])
@cross_origin()
def getObstacles():
    global cityModel

    if request.method == 'GET':
        try:
            ObstaclePositions = [
                {"id": str(a.unique_id), "x": x, "y": 1, "z": z}
                for a, (x,z) in cityModel.grid.coord_iter()
                if isinstance(a, Obstacle)]
            return jsonify({'posiciones de los autos': ObstaclePositions})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al obtener las posiciones de los obstáculos"}), 500
        
        
@app.route('/getRoads', methods = ['GET'])
@cross_origin()
def getRoads():
    global cityModel

    if request.method == 'GET':
        try:
            RoadPositions = [
                {"id": str(a.unique_id), "x": x, "y": 1, "z": z}
                for a, (x,z) in cityModel.grid.coord_iter()
                if isinstance(a, Road)]
            return jsonify({'posiciones de los autos': RoadPositions})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al obtener las posiciones de las calles"}), 500
        
@app.route('/getTrafficLight', methods = ['GET'])
@cross_origin()


def getTrafficLight():
    global cityModel

    if request.method == 'GET':
        try:
            TrafficLightPositions = [
                {"id": str(a.unique_id), "x": x, "y": 1, "z": z}
                for a, (x,z) in cityModel.grid.coord_iter()
                if isinstance(a, Traffic_Light)]
            return jsonify({'posiciones de los autos': TrafficLightPositions})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al obtener las posiciones de los semáforos"}), 500
        
        
@app.route('/getDestination', methods = ['GET'])
@cross_origin()
def getDestination():
    global cityModel

    if request.method == 'GET':
        try:
            DestinationPositions = [
                {"id": str(a.unique_id), "x": x, "y": 1, "z": z}
                for a, (x,z) in cityModel.grid.coord_iter()
                if isinstance(a, Destination)]
            return jsonify({'posiciones de los autos': DestinationPositions})
        
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al obtener las posiciones de los destinos"}), 500
        
@app.route('/update', methods=['GET'])
@cross_origin()
def updateModel():
    global currentStep, cityModel
    if request.method == 'GET':
        try:
            cityModel.step()
            currentStep += 1
            return jsonify({'message':f'Modelo actualizado al step {currentStep}.', 'step actual':currentStep})
        except Exception as e:
            print(e)
            return jsonify({"message":"Error al hacer el step."}), 500
        

if __name__ == '__main__':
    app.run(host = "localhost", port = 8585, debug = True)