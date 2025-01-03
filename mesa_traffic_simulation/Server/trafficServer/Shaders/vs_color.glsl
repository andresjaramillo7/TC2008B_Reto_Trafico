#version 300 es
in vec4 a_position;

// in vec4 a_color;

uniform vec4 u_color;
//uniform mat4 u_transforms;
uniform mat4 u_matrix;

out vec4 v_color;

void main() {
gl_Position = u_matrix * a_position;
v_color = u_color;
}