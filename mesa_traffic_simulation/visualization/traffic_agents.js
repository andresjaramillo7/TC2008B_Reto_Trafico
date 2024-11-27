'use strict'

import * as twgl from 'twgl.js'
import GUI from 'lil-gui';

const vsGLSL = `#version 300 es
in vec4 a_position;
in vec4 a_color;

uniform mat4 u_transforms;
uniform mat4 u_matrix;

out vec4 v_color;

void main() {
gl_Position = u_matrix * a_position;
v_color = a_color;
}
`;

const fsGLSL = `#version 300 es
precision highp float;

in vec4 v_color;

out vec4 outColor;

void main() {
outColor = v_color;
}
`;

class Objeto3D{
    constructor(id, position =[0,0,0], rotation = [0,0,0], scale = [1,1,1]){
        this.id = id;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
        this.matrix = twgl.m4.create();
    }
}

const agent_server_uri = "http://localhost:8585/";

const carros = [];
const obstaculos = [];
const calles = [];
const semaforos = [];
const destinos = [];

let gl, programInfo, 

carArrays, carBufferInfo, carsVao, 

obstacleArrays, obstaclesBufferInfo, obstaclesVao,

roadArrays, roadbufferInfo, roadsVao,

trafficLightArrays, trafficLightBufferInfo, trafficLightVao,

destinationArrays, destinationBufferInfo, destinationVao;

let cameraPosition = {x:0, y:9, z:9};
let frameCount = 0;

const data  = {
    NAgents: 500,
    width: 100,
    height: 100
};

async function main(){
    const canvas = document.querySelector('canvas');
    gl = canvas.getContext('webgl2');

    programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]);

    //Data Generation
    carArrays = generateCarData(1); //debe hacerse
    obstacleArrays = generateData(1); //debe hacerse
    trafficLightArrays = generateData(1); //debe hacerse
    roadArrays = generateData(1); //debe hacerse
    destinationArrays = generateData(1); //debe hacerse

    //Buffer Information
    carBufferInfo = twgl.createBufferInfoFromArrays(gl, carArrays);
    obstaclesBufferInfo = twgl.createBufferInfoFromArrays(gl, obstacleArrays);
    trafficLightBufferInfo = twgl.createBufferInfoFromArrays(gl, trafficLightArrays);
    roadbufferInfo = twgl.createBufferInfoFromArrays(gl, roadArrays);
    destinationBufferInfo = twgl.createBufferInfoFromArrays(gl, destinationArrays);

    //Vertex Array Objects (VAO)

    carsVao = twgl.createVAOFromBufferInfo(gl, programInfo, carBufferInfo);
    obstaclesVao = twgl.createVAOFromBufferInfo(gl, programInfo, obstaclesBufferInfo);
    trafficLightVao = twgl.createVAOFromBufferInfo(gl, programInfo, trafficLightBufferInfo);
    roadsVao = twgl.createVAOFromBufferInfo(gl, programInfo, roadbufferInfo);
    destinationVao = twgl.createVAOFromBufferInfo(gl, programInfo, destinationBufferInfo);

    setupUI();

    await initAgentsModel();

    await getCars();
    await getObstacles();
    await getRoads();
    await getTrafficLights();
    await getDestination();

    await drawScene(gl, programInfo, carsVao, carBufferInfo, obstaclesVao, obstaclesBufferInfo, roadsVao, roadbufferInfo, trafficLightVao, trafficLightBufferInfo, destinationVao, destinationBufferInfo);
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
            console.log(result.message)
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

            console.log(result.position)

            if (carros.length == 0){
                for (const carro of result.position){
                    const newCarro = new Objeto3D(carro.id, [carro.x, carro.y, carro.z]);
                    carros.push(newCarro)
                }

                console.log("Carros: ", carros)

            } else {
                for (const carro of result.position){
                    const current_carro = carros.find((Objeto3D) => Objeto3D.id == carro.id)

                    if(current_carro != undefined){
                        current_carro.position = [carro.x, carro.y, carro.z];
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

            for (const obstacle of result.position) {
                const newObstacle = new Objeto3D(obstacle.id, [obstacle.x, obstacle.y, obstacle.z])
                obstaculos.push(newObstacle)
            }

            console.log("Obstaculos: ", obstaculos)
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

            for (const road of result.positions) {
                const newRoad = new Objeto3D(road.id, [road.x, road.y, road.z])
                calles.push(newRoad)
            }

            console.log("Calles: ", calles)
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

            for (const destination of result.positions) {
                const newDestination = new Objeto3D(destination.id, [destination.x, destination.y, destination.z])
                destinos.push(newDestination)
            }

            console.log("Destinos: ", destinos)
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

            if (semaforos.length == 0){
                for (const semaforo of result.positions){
                    const newSemaforo = new Objeto3D (
                        semaforo.id,
                        [semaforo.x, semaforo.y, semaforo.z],
                        [0,0,0],
                        [1,1,1],
                        semaforo.state ? [0,1,0,1] : [1,0,0,1],
                    );
                    semaforos.push(newSemaforo)
                }

                console.log("Semaforos:", semaforos)
            } else{
                for (const semaforo of SpeechRecognitionResultList.positions){
                    const currentSemaforo = semaforos.find((Objeto3D) => Objeto3D.id == semaforo.id)

                    if (currentSemaforo != undefined){
                        currentSemaforo.state = light.state;
                        currentSemaforo.color = light.state ? [0,1,0,1] : [1,0,0,1]; 
                    }
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
            //podría agregar semáforo
            console.log("Agentes actualizados")
        }
    } catch (error){
        console.log(error)
    }
}


async function drawScene(gl, programInfo, carsVao, carBufferInfo, obstaclesVao, obstaclesBufferInfo, roadsVao, roadbufferInfo, trafficLightVao, trafficLightBufferInfo, destinationVao, destinationBufferInfo) {

    twgl.resizeCanvasToDisplaySize(gl.canvas);

    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    gl.clearColor(0.2, 0.2, 0.2, 1);
    gl.enable(gl.DEPTH_TEST)

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.useProgram(programInfo.program);

    const viewProjectionMatrix = setupWorldView(gl);
    const distance = 1;

    //drawing agents
    drawRoads(distance, roadsVao, roadbufferInfo, viewProjectionMatrix)
    drawTrafficLight(distance, trafficLightVao, trafficLightBufferInfo, )
    drawObstacles(distance, obstaclesVao, obstaclesBufferInfo, viewProjectionMatrix)
    drawDestinations(distance, destinationVao, destinationBufferInfo, viewProjectionMatrix)
    drawCars(distance, carsVao, carBufferInfo, viewProjectionMatrix)

    frameCount++

    if(frameCount%30 == 0){
        frameCount = 0
        await update()
    }

    requestAnimationFrame(() => drawScene(gl, programInfo, carsVao, carBufferInfo, obstaclesVao, obstaclesBufferInfo, roadsVao, roadbufferInfo, trafficLightVao, trafficLightBufferInfo, destinationVao, destinationBufferInfo))

}

function drawCars(distance, carsVao, carBufferInfo, viewProjectionMatrix){

    gl.bindVertexArray(carsVao);

    for (const carro of carros){

        const carro_trans = twgl.v3.create(...carro.position);
        const carro_scale = twgl.v3.create(...carro.scale);

        carro.matrix = twgl.m4.translate(viewProjectionMatrix, carro_trans);
        carro.matrix = twgl.m4.rotateX(carro.matrix, carro.rotation[0]);
        carro.matrix = twgl.m4.rotateY(carro.matrix, carro.rotation[1]);
        carro.matrix = twgl.m4.rotateZ(carro.matrix, carro.rotation[2]);
        carro.matrix = twgl.m4.scale(carro.matrix, carro_scale);

        let uniforms = {
            u_matrix: carro.matrix,
        }

        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, carBufferInfo);
    }
}

function drawObstacles(distance, obstaclesVao, obstaclesBufferInfo, viewProjectionMatrix){

    gl.bindVertexArray(obstaclesVao);

    for (const obstaculo of obstaculos){
        const obstacle_trans = twgl.v3.create(...obstaculo.position);
        const obstacle_scale = twgl.v3.create(...obstaculo.scale);

        obstaculo.matrix = twgl.m4.translate(viewProjectionMatrix, obstacle_trans);
        obstaculo.matrix = twgl.m4.rotateX(obstaculo.matrix, obstaculo.rotation[0]);
        obstaculo.matrix = twgl.m4.rotateY(obstaculo.matrix, obstaculo.rotation[1]);
        obstaculo.matrix = twgl.m4.rotateZ(obstaculo.matrix, obstaculo.rotation[2]);
        obstaculo.matrix = twgl.m4.scale(obstaculo.matrix, obstacle_scale);

        let uniforms = {
            u_matrix: obstaculo.matrix
        }

        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, obstaclesBufferInfo);
    }
}

function drawRoads(distance, roadsVao, roadbufferInfo, viewProjectionMatrix){

    gl.bindVertexArray(roadsVao);

    for (const calle of calles){
        const calle_trans = twgl.v3.create(...calle.position);
        const calle_scale = twgl.v3.create(...calle.scale);

        calle.matrix = twgl.m4.translate(viewProjectionMatrix, calle_trans);
        calle.matrix = twgl.m4.rotateX(calle.matrix, calle.rotation[0]);
        calle.matrix = twgl.m4.rotateY(calle.matrix, calle.rotation[1]);
        calle.matrix = twgl.m4.rotateZ(calle.matrix, calle.rotation[2]);
        calle.matrix = twgl.m4.scale(calle.matrix, calle_scale);

        let uniforms = {
            u_matrix: calle.matrix
        }

        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, roadbufferInfo);
    }
}

function drawTrafficLight(distance, trafficLightVao, trafficLightBufferInfo, ){

    gl.bindVertexArray(trafficLightVao);

    for (const semaforo of semaforos){
        const semaforo_trans = twgl.v3.create(...semaforo.position);
        const semaforo_scale = twgl.v3.create(...semaforo.scale);

        semaforo.matrix = twgl.m4.translate(viewProjectionMatrix, semaforo_trans);
        semaforo.matrix = twgl.m4.rotateX(semaforo.matrix, calle.rotation[0]);
        semaforo.matrix = twgl.m4.rotateY(semaforo.matrix, calle.rotation[1]);
        semaforo.matrix = twgl.m4.rotateZ(semaforo.matrix, calle.rotation[2]);
        semaforo.matrix = twgl.m4.scale(semaforo.matrix, semaforo_scale);

        let uniforms = {
            u_matrix: semaforo.matrix
        }

        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, trafficLightBufferInfo);
    }
}

function drawDestinations(distance, destinationVao, destinationBufferInfo, viewProjectionMatrix){

    gl.bindVertexArray(destinationVao);

    for (const destino of destinos){
        const destino_trans = twgl.v3.create(...destino.position);
        const destino_scale = twgl.v3.create(...destino.scale);

        semaforo.matrix = twgl.m4.translate(viewProjectionMatrix, destino_trans);
        semaforo.matrix = twgl.m4.rotateX(destino.matrix, calle.rotation[0]);
        semaforo.matrix = twgl.m4.rotateY(destino.matrix, calle.rotation[1]);
        semaforo.matrix = twgl.m4.rotateZ(destino.matrix, calle.rotation[2]);
        semaforo.matrix = twgl.m4.scale(destino.matrix, destino_scale);

        let uniforms = {
            u_matrix: destino.matrix
        }

        twgl.setUniforms(programInfo, uniforms);
        twgl.drawBufferInfo(gl, destinationBufferInfo);
    }
}

function setupWorldView(gl) {

    const fov = 45 * Math.PI / 180;
    const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;

    const projectionMatrix = twgl.m4.perspective(fov, aspect, 1, 200);
    const target = [data.width/2, 0, data.height/2];

    const up = [0, 1, 0];
    
    const camPos = twgl.v3.create(cameraPosition.x + data.width/2, cameraPosition.y, cameraPosition.z+data.height/2)

    const cameraMatrix = twgl.m4.lookAt(camPos, target, up);

    const viewMatrix = twgl.m4.inverse(cameraMatrix);

    const viewProjectionMatrix = twgl.m4.multiply(projectionMatrix, viewMatrix);

    return viewProjectionMatrix;
}

function setupUI() {
    // Create a new GUI instance
    const gui = new GUI();

    // Create a folder for the camera position
    const posFolder = gui.addFolder('Position:')

    // Add a slider for the x-axis
    posFolder.add(cameraPosition, 'x', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            cameraPosition.x = value
        });

    // Add a slider for the y-axis
    posFolder.add( cameraPosition, 'y', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            cameraPosition.y = value
        });

    // Add a slider for the z-axis
    posFolder.add( cameraPosition, 'z', -50, 50)
        .onChange( value => {
            // Update the camera position when the slider value changes
            cameraPosition.z = value
        });
}

function generateData(size){

    let arrays =
    {
        a_position: {
                numComponents: 3,
                data: [
                  // Front Face
                  -0.5, -0.5,  0.5,
                  0.5, -0.5,  0.5,
                  0.5,  0.5,  0.5,
                 -0.5,  0.5,  0.5,

                 // Back face
                 -0.5, -0.5, -0.5,
                 -0.5,  0.5, -0.5,
                  0.5,  0.5, -0.5,
                  0.5, -0.5, -0.5,

                 // Top face
                 -0.5,  0.5, -0.5,
                 -0.5,  0.5,  0.5,
                  0.5,  0.5,  0.5,
                  0.5,  0.5, -0.5,

                 // Bottom face
                 -0.5, -0.5, -0.5,
                  0.5, -0.5, -0.5,
                  0.5, -0.5,  0.5,
                 -0.5, -0.5,  0.5,

                 // Right face
                  0.5, -0.5, -0.5,
                  0.5,  0.5, -0.5,
                  0.5,  0.5,  0.5,
                  0.5, -0.5,  0.5,

                 // Left face
                 -0.5, -0.5, -0.5,
                 -0.5, -0.5,  0.5,
                 -0.5,  0.5,  0.5,
                 -0.5,  0.5, -0.5
                ].map(e => size * e)
            },
        a_color: {
                numComponents: 4,
                data: [
                  // Front face
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                  // Back Face
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                  // Top Face
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                  // Bottom Face
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                  // Right Face
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                  // Left Face
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                ]
            },
        indices: {
                numComponents: 3,
                data: [
                  0, 1, 2,      0, 2, 3,    // Front face
                  4, 5, 6,      4, 6, 7,    // Back face
                  8, 9, 10,     8, 10, 11,  // Top face
                  12, 13, 14,   12, 14, 15, // Bottom face
                  16, 17, 18,   16, 18, 19, // Right face
                  20, 21, 22,   20, 22, 23  // Left face
                ]
            }
    };
    return arrays;
}

function generateCarData(size){

    let arrays =
    {
        a_position: {
                numComponents: 3,
                data: [
                  // Front Face
                  -0.5, -0.5,  0.5,
                  0.5, -0.5,  0.5,
                  0.5,  0.5,  0.5,
                 -0.5,  0.5,  0.5,

                 // Back face
                 -0.5, -0.5, -0.5,
                 -0.5,  0.5, -0.5,
                  0.5,  0.5, -0.5,
                  0.5, -0.5, -0.5,

                 // Top face
                 -0.5,  0.5, -0.5,
                 -0.5,  0.5,  0.5,
                  0.5,  0.5,  0.5,
                  0.5,  0.5, -0.5,

                 // Bottom face
                 -0.5, -0.5, -0.5,
                  0.5, -0.5, -0.5,
                  0.5, -0.5,  0.5,
                 -0.5, -0.5,  0.5,

                 // Right face
                  0.5, -0.5, -0.5,
                  0.5,  0.5, -0.5,
                  0.5,  0.5,  0.5,
                  0.5, -0.5,  0.5,

                 // Left face
                 -0.5, -0.5, -0.5,
                 -0.5, -0.5,  0.5,
                 -0.5,  0.5,  0.5,
                 -0.5,  0.5, -0.5
                ].map(e => size * e)
            },
        a_color: {
                numComponents: 4,
                data: [
                  // Front face
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                    0, 0, 0, 1, // v_1
                  // Back Face
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                    0.333, 0.333, 0.333, 1, // v_2
                  // Top Face
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                    0.5, 0.5, 0.5, 1, // v_3
                  // Bottom Face
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                    0.666, 0.666, 0.666, 1, // v_4
                  // Right Face
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                    0.833, 0.833, 0.833, 1, // v_5
                  // Left Face
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                    1, 1, 1, 1, // v_6
                ]
            },
        indices: {
                numComponents: 3,
                data: [
                  0, 1, 2,      0, 2, 3,    // Front face
                  4, 5, 6,      4, 6, 7,    // Back face
                  8, 9, 10,     8, 10, 11,  // Top face
                  12, 13, 14,   12, 14, 15, // Bottom face
                  16, 17, 18,   16, 18, 19, // Right face
                  20, 21, 22,   20, 22, 23  // Left face
                ]
            }
    };
    return arrays;
}




main()
