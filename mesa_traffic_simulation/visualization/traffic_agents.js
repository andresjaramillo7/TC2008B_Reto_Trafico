'use strict';

import * as twgl from 'twgl.js';
import GUI from 'lil-gui';
import { v3, m4 } from './starter_3D_lib.js';

import { load_obj } from '../Server/trafficServer/load_obj.js'

import building from "../Server/trafficServer/Objects/cube_normals.obj?raw"
import car from "../Server/trafficServer/Objects/cube_normals.obj?raw"
import traffic_light from "../Server/trafficServer/Objects/cube_normals.obj?raw"
import road from "../Server/trafficServer/Objects/cube_normals.obj?raw/"

import vsGLSL from "../Server/trafficServer/Shaders/vs_color.glsl?raw"
import fsGLSL from "../Server/trafficServer/Shaders/fs_color.glsl?raw"


const data  = {
    NAgents: 4,
    width: 30,
    height: 30
};

const Objects = {
    'car': {
        'model': {
            data: car, //must export
            color: [Math.random(), Math.random(), Math.random(), 1],
            shininess: 100,
        },
        'vao': undefined,
        'bufferInfo': undefined,
    },
    'building': {
        'model': {
            data: building, //must export
            color:[Math.random(), Math.random(), Math.random(), 1],
            shininess: 50,
        },
        'vao': undefined,
        'bufferInfo': undefined,
    },
    'traffic_light': {
        'model': {
            data: traffic_light, //must export
            color: [0.5, 0.5, 0.5, 1],
            shininess: 50,
        },
        'vao': undefined,
        'bufferInfo': undefined
    },
    'destination': {
        'model': {
            data: building, //must export
            color: [0.529, 0.808, 0.922, 1],
            shininess: 50,
        }, 
        'vao': undefined,
        'bufferInfo': undefined,
    },
    'road': {
        'model': {
            data: road, //must export
            color: [0.1, 0.1, 0.1, 1],
            shininess: 20,
        },
        'vao': undefined,
        'bufferInfo': undefined,
    }
}

const settings = {
    rotationSpeed: {
        x: 0,
        y: 30,
        z: 0,
    },
    cameraPosition: {
        x: 17,
        y: 50,
        z: 30,
    },
    lightPosition: {
        x:20,
        y:30,
        z:20,
    },
    ambientColor: [0.5, 0.5, 0.5, 1.0],
    diffuseColor: [0.5, 0.5, 0.5, 1.0],
    specularColor: [0.5, 0.5, 0.5, 1.0],

};

class Car{
    constructor(id, position = [0,0,0], rotation = [0,0,0], scale = [0.2,0.2,0.2], color = [Math.random(), Math.random(), Math.random(), 1]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.color = color;
        this.shininess = Objects.car.model.shininess;
        this.matrix = m4.identity();
    }
}

class Building{
    constructor(id, position = [0,0,0], rotation = [0,0,0], scale = [0.5,0.5,0.5], color = [0.3, 0.3, 0.3, 1]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.color = color;
        this.shininess = Objects.building.model.shininess;
        this.matrix = m4.identity();
    }
}

class Destination{
    constructor(id, position = [0,0,0], rotation = [0,0,0], scale = [0.5,0.2,0.5]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.color = Objects.destination.model.color;
        this.shininess = Objects.destination.model.shininess;
        this.matrix = m4.identity();
    }
}

class TrafficLight{
    constructor(id, position = [0,0,0], rotation = [0,0,0], scale = [0.1,0.1,0.1], color = [1,0,0,1]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.color = color;
        this.shininess = Objects.traffic_light.model.shininess;
        this.matrix = m4.identity();
    }
}

class Road{
    constructor(id, position = [0,0,0], rotation = [0,0,0], scale = [1,0.01,1]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.color = Objects.road.model.color;
        this.shininess = Objects.road.model.shininess;
        this.matrix = m4.identity();
    }
}

const agent_server_uri = "http://localhost:8585/";
let carros = [];
const obstaculos = [];
const calles = [];
let semaforos = [];
const destinos = [];

let gl, programInfo, carArrays, obstacleArrays, trafficLightArrays, roadArrays

let frameCount = 0;



async function main(){
    const canvas = document.querySelector('canvas');
    gl = canvas.getContext('webgl2');

    programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]);

    //Data Generation
    carArrays = load_obj(car); //debe hacerse
    obstacleArrays = load_obj(building); //debe hacerse
    trafficLightArrays = load_obj(traffic_light); //debe hacerse
    roadArrays = load_obj(road); //debe hacerse

    //Buffer Information
    Objects.car.bufferInfo = twgl.createBufferInfoFromArrays(gl, carArrays);
    Objects.building.bufferInfo = twgl.createBufferInfoFromArrays(gl, obstacleArrays);
    Objects.traffic_light.bufferInfo = twgl.createBufferInfoFromArrays(gl, trafficLightArrays);
    Objects.road.bufferInfo = twgl.createBufferInfoFromArrays(gl, roadArrays);
    Objects.destination.bufferInfo = twgl.createBufferInfoFromArrays(gl, obstacleArrays);

    //Vertex Array Objects (VAO)

    Objects.car.vao = twgl.createVAOFromBufferInfo(gl, programInfo, Objects.car.bufferInfo);
    Objects.building.vao = twgl.createVAOFromBufferInfo(gl, programInfo, Objects.building.bufferInfo);
    Objects.traffic_light.vao = twgl.createVAOFromBufferInfo(gl, programInfo, Objects.traffic_light.bufferInfo);
    Objects.road.vao = twgl.createVAOFromBufferInfo(gl, programInfo, Objects.road.bufferInfo);
    Objects.destination.vao = twgl.createVAOFromBufferInfo(gl, programInfo, Objects.destination.bufferInfo);

    //console.log("Info de coche: ", Objects.car)

    setupUI();

    await initAgentsModel();

    await getCars();
    await getObstacles();
    await getRoads();
    await getTrafficLights();
    await getDestination();

    await drawScene(gl, Objects);
}

async function initAgentsModel(){
    try{

        let response = await fetch(agent_server_uri + "init", {
            method: 'POST',
            headers: { 'Content-Type':'application/json' },
            body: JSON.stringify(data)
        })

        if (response.ok){
            let result = await response.json()
            //console.log(result.message)
        }
    } catch (error) {
        console.log(error)
    }
}


async function getCars(){
    try {
        let response = await fetch(agent_server_uri + "getCars")

        if (response.ok){
            let result = await response.json()

            //console.log(result.positions)

            //console.log("Carros: ", carros)

            if (carros.length == 0){

                for (const carro of result.positions){
                    const newCarro = new Car(carro.id, [carro.x, carro.y, carro.z]);
                    carros.push(newCarro)
                }

                //
            } else{
                for (const carro of result.positions){
                    const current_car = carros.find((Car) => Car.id == carro.id)

                    if (current_car != undefined){
                        current_car.position = [carro.x, carro.y, carro.z]
                    } else{
                        const newCarro = new Car(carro.id, [carro.x, carro.y, carro.z]);
                        carros.push(newCarro)

                    }
                }
            }
        }

    } catch (error){
        console.log(error)
    }
}


async function getObstacles() {
    try {

        let response = await fetch(agent_server_uri + "getObstacles")

        if (response.ok){
            let result = await response.json()

            if (obstaculos == 0){
            for (const obstacle of result.positions) {
                const newObstacle = new Building(obstacle.id, [obstacle.x, obstacle.y, obstacle.z])
                obstaculos.push(newObstacle)
            }

            //console.log("Obstaculos: ", obstaculos)
        }
        }
    } catch (error) {
        console.log(error)
    }
}

async function getRoads() {
    try {

        let response = await fetch(agent_server_uri + "getRoads")

        if (response.ok){
            let result = await response.json()

            if (calles == 0){
            for (const roads of result.positions) {
                const newRoad = new Road(roads.id, [roads.x, roads.y, roads.z])
                calles.push(newRoad)
            }

            //console.log("Calles: ", calles)
        }
        }
    } catch (error) {
        console.log(error)
    }
}

async function getDestination() {
    try {

        let response = await fetch(agent_server_uri + "getDestination")

        if (response.ok){
            let result = await response.json()

            for (const destinations of result.positions) {
                const newDestination = new Destination(destinations.id, [destinations.x, destinations.y, destinations.z])
                destinos.push(newDestination)
            }

            //console.log("Destinos: ", destinos)
        }
    } catch (error) {
        console.log(error)
    }
}

async function getTrafficLights() { //must check
    try {
        let response = await fetch(agent_server_uri + "getTrafficLight")

        if (response.ok){
            let result = await response.json()

                semaforos = []

                if (semaforos.length == 0){
                for (const semaforo of result.positions){
                    const color = semaforo.condition ? [0,1,0,1] : [1,0,0,1];
                    const newSemaforo = new TrafficLight (
                        semaforo.id,
                        [semaforo.x, semaforo.y, semaforo.z],
                        [0,0,0],
                        [0.2,0.2,0.2],
                        color,
                    );
                    semaforos.push(newSemaforo)
                } 

                //console.log("Semaforos:", semaforos)
            } else {
                for (const agent of result.positions){
                    const color = agent.condition ? [0,1,0,1] : [1,0,0,1];
                    const current_semaforo = semaforos.find((TrafficLight) => TrafficLight.id == agent.id)
                }
            } 
        }
    } catch (error){
        console.log(error)
    }
}

async function update(){
    try {
        let response = await fetch(agent_server_uri + "update")

        if (response.ok){
            await getCars()
            await getTrafficLights()
            //console.log("Agentes actualizados")
        }
    } catch (error){
        console.log(error)
    }
}


async function drawScene(gl, Objects) {

    twgl.resizeCanvasToDisplaySize(gl.canvas);

    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    gl.clearColor(0.2, 0.2, 0.2, 1);
    gl.enable(gl.DEPTH_TEST)

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.useProgram(programInfo.program);

    let v3_cameraPosition = v3.create(
        settings.cameraPosition.x,
        settings.cameraPosition.y,
        settings.cameraPosition.z
    );
    let v3_lightPosition = v3.create(
        settings.lightPosition.x,
        settings.lightPosition.y,
        settings.lightPosition.z
    );
/*
   let globalUniforms = {
        
        u_viewWorldPosition: [10,20,10],
        u_lightWorldPosition: v3_lightPosition,
        u_ambientLight: settings.ambientColor,
        u_diffuseLight: settings.diffuseColor,
        u_specularLight: settings.specularColor,
    }; 
    twgl.setUniforms(programInfo, globalUniforms); */

    const viewProjectionMatrix = setupWorldView(gl);

    //drawing agents
    drawAgent(calles, Objects.road.vao, Objects.road.bufferInfo, viewProjectionMatrix);
    drawAgent(obstaculos, Objects.building.vao, Objects.building.bufferInfo, viewProjectionMatrix);
    drawAgent(destinos, Objects.destination.vao, Objects.destination.bufferInfo, viewProjectionMatrix);
    drawAgent(semaforos, Objects.traffic_light.vao, Objects.traffic_light.bufferInfo, viewProjectionMatrix);
    drawAgent(carros, Objects.car.vao, Objects.car.bufferInfo, viewProjectionMatrix);
    
    frameCount++;

    if(frameCount%20 == 0){
        frameCount = 0
        await update()
    }

    requestAnimationFrame(() => drawScene(gl, Objects))

}

function drawAgent(list, Vao, BufferInfo, viewProjectionMatrix){

    gl.bindVertexArray(Vao);

    //console.log("List: ", list)

    for (const agent of list){

        const trans = twgl.v3.create(...agent.position);
        const scale = twgl.v3.create(...agent.scale);

        let mat = m4.identity();
        mat = m4.multiply(m4.scale(scale), mat);
        mat = m4.multiply(m4.rotationX(agent.rotation[0]), mat);
        mat = m4.multiply(m4.rotationY(agent.rotation[1]), mat);
        mat = m4.multiply(m4.rotationZ(agent.rotation[2]), mat);
        mat = m4.multiply(m4.translation(trans), mat);


        let modelViewProjectionMatrix = m4.multiply(viewProjectionMatrix, mat)


        let uniforms = {
            u_matrix: modelViewProjectionMatrix,
            u_color: agent.color,
        }

        if (agent.state != undefined){
            uniforms.u_color = agent.color
            
        }


        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, BufferInfo);
    }
        
}


function setupWorldView(gl) {
    const fov = 45 * Math.PI / 180;
    const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;

    // Creando la matriz de proyección (sin cambios)
    const projectionMatrix = twgl.m4.perspective(fov, aspect, 1, 200);

    // Definir el objetivo hacia el cual apunta la cámara (puedes cambiar esto si es necesario)
    const target = [data.width / 2, 0, data.height / 2];

    const up = [0, 1, 0];

    // Aquí estamos usando directamente la posición de la cámara sin desplazamientos adicionales
    const camPos = twgl.v3.create(settings.cameraPosition.x, settings.cameraPosition.y, settings.cameraPosition.z);

    // Creando la matriz de la cámara (posicionando la cámara en camPos y mirando hacia el objetivo)
    const cameraMatrix = twgl.m4.lookAt(camPos, target, up);

    // La matriz de vista es la inversa de la matriz de la cámara
    const viewMatrix = twgl.m4.inverse(cameraMatrix);

    // Multiplicamos la matriz de proyección por la matriz de vista
    const viewProjectionMatrix = twgl.m4.multiply(projectionMatrix, viewMatrix);

    //console.log("View Projection Matrix: ", viewProjectionMatrix)

    return viewProjectionMatrix;
}

function setupUI() {
    // Create a new GUI instance
    const gui = new GUI();

    // Create a folder for the camera position
    const posFolder = gui.addFolder('Position:')

    // Add a slider for the x-axis
    posFolder.add(settings.cameraPosition, 'x', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            settings.cameraPosition.x = value
        });

    // Add a slider for the y-axis
    posFolder.add( settings.cameraPosition, 'y', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            settings.cameraPosition.y = value
        });

    // Add a slider for the z-axis
    posFolder.add( settings.cameraPosition, 'z', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            settings.cameraPosition.z = value
        });

    const lightFolder = gui.addFolder('Light controls: ')
    lightFolder.add(settings.lightPosition, 'x', -20, 20).decimals(2)
    lightFolder.add(settings.lightPosition, 'y', -20, 30).decimals(2)
    lightFolder.add(settings.lightPosition, 'z', -20, 20).decimals(2)

    lightFolder.addColor(settings, 'ambientColor')
    lightFolder.addColor(settings, 'diffuseColor')
    lightFolder.addColor(settings, 'specularColor')



}

main()