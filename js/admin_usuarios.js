const contenedor = document.querySelector('tbody')
let resultados = ''

//Usuarios de ejemplo
function usuarioEjemplo(uno,dos,tres,cuatro,cinco){
    this.uno = uno;
    this.dos = dos;
    this.tres = tres;
    this.cuatro = cuatro;
    this.cinco = cinco;
}

let usuariosEjemplo = [
    new usuarioEjemplo('cote@gmail.com', 'Juan Fernandez', '123456789', 'patatas123', 'garzon'),
    new usuarioEjemplo('otec@gmail.com','Maria Nuñez','987654321', 'fideos321', 'administrador')
]




const modalUsuario = new bootstrap.Modal(document.getElementById('modalUsuario'))
const formUsuario = document.querySelector('form')

const correo = document.getElementById('correo')
const nombre = document.getElementById('nombre')
const numero = document.getElementById('numero')
const contra = document.getElementById('contra')
const tipoUsuario = document.getElementById('tipoUsuario')

let opcion = ''

btnAgregarUsuario.addEventListener('click', () => {
    correo.value = ''
    nombre.value = ''
    numero.value = ''
    contra.value = ''
    tipoUsuario.value = ''
    modalUsuario.show()
    opcion = 'crear'

    mostrar()
})

//Procedimiento agregar
btnAgregar.addEventListener('click', () => {
    usuariosEjemplo.push(
        new usuarioEjemplo(correo.value, nombre.value, numero.value, contra.value, tipoUsuario.value)
    )
    console.log(usuariosEjemplo)
    mostrar()
})

//Procedimiento mostrar
btnActualizar.addEventListener('click', () => {
    mostrar()
})

const mostrar = () =>{
    var elmtTable = document.getElementById('tablaUsuarios');
    var tableRows = elmtTable.getElementsByTagName('tr');
    var rowCount = tableRows.length;

    for (var x=rowCount-1; x>0; x--) {
        elmtTable.removeChild(tableRows[x]);
    }


    usuariosEjemplo.forEach( usuariosEjemplo => {
        resultados +=   `<tr>
                            <td>${usuariosEjemplo.uno}</td>
                            <td>${usuariosEjemplo.dos}</td>
                            <td>${usuariosEjemplo.tres}</td>
                            <td>${usuariosEjemplo.cuatro}</td>
                            <td>${usuariosEjemplo.cinco}</td>
                            <td class='text-center'><a class="btnEditar btn btn-primary">Editar</a><a class="btnEliminar btn btn-danger">Eliminar</a></td>
                        </tr>
                        `
    })
    contenedor.innerHTML = resultados
}

//Procedimiento Eliminar
const on = (element,event,selector,handler) =>{
    element.addEventListener(event, e =>{
        if(e.target.closest(selector)){
            handler(e)
        }
    })
}

on(document, 'click', '.btnEliminar', e =>{
    const fila = e.target.parentNode.parentNode
    const id = fila.firstElementChild //con esto conseguimos el correo, que viene siendo el identificador
    //console.log(id) 
    let index = 0

    usuariosEjemplo.forEach( usuariosEjemplo =>{
        if(id == usuariosEjemplo.uno){
            usuariosEjemplo.splice(index,1)
            console.log(usuariosEjemplo.uno)
        }
        index = index + 1
    })
})

