// 17/11/2024
// Create an .js file with the cylinder obj attributes
// node load_objs.js [path]

// Código inspirado en el trabajo de Ricardo Alfredo Calvo Perez - A01028889


function load_obj(content) {

    const vertices = [[0, 0, 0]];
    const normals = [[0, 0, 0]];
    const a_position = [];
    const a_normal = [];
  
    const lines = content.split('\n');
  
    for (const line of lines) {
      const trimmedLine = line.trim();
  
      if (trimmedLine.startsWith('v ')) {
  
        const parts = trimmedLine.split(/\s+/).slice(1).map(parseFloat);
        vertices.push(parts);
      }
      else if (trimmedLine.startsWith('vn ')) {
  
        const parts = trimmedLine.split(/\s+/).slice(1).map(parseFloat);
        normals.push(parts);
      }
      else if (trimmedLine.startsWith('f ')) {
  
        const parts = trimmedLine.split(/\s+/).slice(1);
        for (let part of parts) {
          const parts2 = part.split('/').map(parseFloat); // [v, vt, vn]
          a_position.push(...vertices[parts2[0]]);
          a_normal.push(...normals[parts2[2]]);
        }
      }
    }
  
    // console.log(vertices);
    // console.log(a_normal);
    // console.log(a_position);
  
  
    const arrays = {
      a_position: {
        numComponents: 3,
        data: a_position,
      },
      a_color: {
        numComponents: 4,
        data: [
          0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1, 0.4, 0.4, 0.4, 1
        ],
      },
      a_normal: {
        numComponents: 3,
        data: a_normal,
      }
    };
  
    return arrays;
  }
  
  export { load_obj }