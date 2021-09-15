const contenedor = document.querySelector('tbody')
let resultados = ''

//Usuarios de ejemplo
function mesaEjemplo(uno,dos,tres){
    this.uno = uno;
    this.dos = dos;
    this.tres = tres;
}

let mesasEjemplo = [
    new mesaEjemplo('1', 'Disponible', 'Desocupada'),
    new mesaEjemplo('2','No disponible','Ocupada' ),
    new mesaEjemplo('3','No disponible','En Mantenimiento'),
]



const modalMesa = new bootstrap.Modal(document.getElementById('modalMesa'))
const formMesa = document.querySelector('form')

const id = document.getElementById('id')
const dispon = document.getElementById('dispon')
const estado = document.getElementById('estado')


let opcion = ''

btnAgregarMesa.addEventListener('click', () => {
    id.value = ''
    dispon.value = ''
    estado.value = ''
    modalMesa.show()
    opcion = 'crear'

    mostrar()
})

//Procedimiento agregar
btnAgregar.addEventListener('click', () => {
    mesasEjemplo.push(
        new mesaEjemplo(id.value, dispon.value, estado.value)
    )
    console.log(mesasEjemplo)
    mostrar()
    modalMesa.hide()
})

//Procedimiento mostrar
btnActualizar.addEventListener('click', () => {
    mostrar()
})

const mostrar = () =>{
    var elmtTable = document.getElementById('tablaMesas');
    var tableRows = elmtTable.getElementsByTagName('tr');
    var rowCount = tableRows.length;

    for (var x=rowCount-1; x>0; x--) {
        elmtTable.removeChild(tableRows[x]);
    }


    mesasEjemplo.forEach( mesasEjemplo => {
        resultados +=   `<tr>
                            <td>${mesasEjemplo.uno}</td>
                            <td>${mesasEjemplo.dos}</td>
                            <td>${mesasEjemplo.tres}</td>
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
    const idBusqueda = fila.firstElementChild //con esto conseguimos el correo, que viene siendo el identificador
    //console.log(id) 
    let index = 0

    mesasEjemplo.forEach( mesasEjemplo =>{
        if(idBusqueda == mesasEjemplo.uno){
            mesasEjemplo.splice(index,1)
            console.log(mesasEjemplo.uno)
        }
        index = index + 1
    })
})

