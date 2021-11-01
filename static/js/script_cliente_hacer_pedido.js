const cardsEntradas1 = document.getElementById('cardsEntradas1')
const cardsEntradas2 = document.getElementById('cardsEntradas2')
const cardsEntradas3 = document.getElementById('cardsEntradas3')
const cardsEntradas4 = document.getElementById('cardsEntradas4')
const items = document.getElementById('items')
const footer = document.getElementById('footer')
const templateCard = document.getElementById('template-card').content
const templateFooter = document.getElementById('template-footer').content
const templateCarrito = document.getElementById('template-carrito').content
const fragment1 = document.createDocumentFragment()
const fragment2 = document.createDocumentFragment()
const fragment3 = document.createDocumentFragment()
const fragment4 = document.createDocumentFragment()
let carrito = {}

// Eventos
// El evento DOMContentLoaded es disparado cuando el documento HTML ha sido completamente cargado y parseado
//document.addEventListener('DOMContentLoaded', e => { fetchData() });
cardsEntradas1.addEventListener('click', e => { addCarrito(e) });
cardsEntradas2.addEventListener('click', e => { addCarrito(e) });
cardsEntradas3.addEventListener('click', e => { addCarrito(e) });
cardsEntradas4.addEventListener('click', e => { addCarrito(e) });
items.addEventListener('click', e => { btnAumentarDisminuir(e) })

// Objeto producto
function Entrada(nombre, precio, id) {
    this.nombre = nombre;
    this.precio = precio;
    this.id = id;
}

//Productos de ejemplo
var Entradas = [
    new Entrada('Ensalada Cesar', 2000, 1),
    new Entrada('Ensalada Juan', 3000, 2),
    new Entrada('Esalada Verdejo', 1500, 3),
    new Entrada('Ensaladita Cuatro', 2500, 4),
    new Entrada('Ensaladita Cinco', 2500, 5),
    new Entrada('Ensaladita Seis', 2500, 6),
    new Entrada('Ensaladita Siete', 2500, 7),
    new Entrada('Ensaladita Ocho', 2500, 8),
    new Entrada('Ensaladita Nueve', 2500, 9),
    new Entrada('Ensaladita Diez', 2500, 10),
    new Entrada('Ensaladita Once', 2500, 11),
    new Entrada('Ensaladita Doce', 2500, 12),
    new Entrada('Ensaladita Trece', 2500, 13),
    new Entrada('Ensaladita Catorce', 2500, 14),
    new Entrada('Ensaladita Quince', 2500, 15),
    new Entrada('Ensaladita Diesiséis', 2500, 16)
]
/*
// Traer productos
const fetchData = async () => {
    pintarCards(Entradas)
}*/

/*
// Pintar productos
const pintarCards = Entradas => {
    var contar = 0
    Entradas.forEach(item => {
        contar = contar + 1
        
        switch (true) {
            case (contar >= 1 && contar <= 4):
                templateCard.querySelector('h5').textContent = item.nombre
                templateCard.querySelector('p').textContent = item.precio
                templateCard.querySelector('button').dataset.id = item.id
                const clone1 = templateCard.cloneNode(true)
                fragment1.appendChild(clone1)
                break;

            case (contar >= 5 && contar <= 8):
                templateCard.querySelector('h5').textContent = item.nombre
                templateCard.querySelector('p').textContent = item.precio
                templateCard.querySelector('button').dataset.id = item.id
                const clone2 = templateCard.cloneNode(true)
                fragment2.appendChild(clone2)
                break;    
            
            
            case (contar >=9 && contar <= 12):
                templateCard.querySelector('h5').textContent = item.nombre
                templateCard.querySelector('p').textContent = item.precio
                templateCard.querySelector('button').dataset.id = item.id
                const clone3 = templateCard.cloneNode(true)
                fragment3.appendChild(clone3)
                break;

            case (contar >=13 && contar <= 16):
                templateCard.querySelector('h5').textContent = item.nombre
                templateCard.querySelector('p').textContent = item.precio
                templateCard.querySelector('button').dataset.id = item.id
                const clone4 = templateCard.cloneNode(true)
                fragment4.appendChild(clone4)
                break;
        }
    })
    cardsEntradas1.appendChild(fragment1)
    cardsEntradas2.appendChild(fragment2)
    cardsEntradas3.appendChild(fragment3)
    cardsEntradas4.appendChild(fragment4)
}
*/

// Agregar al carrito
const addCarrito = e => {
    if (e.target.classList.contains('btn-dark')) {
         console.log(e.target.dataset.id)
        // console.log(e.target.parentElement)
        setCarrito(e.target.parentElement)
    }
    e.stopPropagation()
}

const setCarrito = item => {
    // console.log(item)
    const producto = {
        title: item.querySelector('h5').textContent,
        precio: item.querySelector('.precioUnit').textContent,
        id: item.querySelector('button').id,
        cantidad: 1
    }
    // console.log(producto)
    if (carrito.hasOwnProperty(producto.id)) {
        producto.cantidad = carrito[producto.id].cantidad + 1
    }

    carrito[producto.id] = { ...producto }
    
    pintarCarrito()
}

const pintarCarrito = () => {
    items.innerHTML = ''

    Object.values(carrito).forEach(producto => {
        templateCarrito.querySelector('th').textContent = producto.id
        templateCarrito.querySelectorAll('td')[0].textContent = producto.title
        templateCarrito.querySelectorAll('td')[1].textContent = producto.cantidad
        templateCarrito.querySelector('span').textContent = producto.precio * producto.cantidad
        
        //botones
        templateCarrito.querySelector('.btn-info').dataset.id = producto.id
        templateCarrito.querySelector('.btn-danger').dataset.id = producto.id

        const clone = templateCarrito.cloneNode(true)
        fragment1.appendChild(clone)
    })
    items.appendChild(fragment1)

    pintarFooter()
}

const pintarFooter = () => {
    footer.innerHTML = ''
    
    if (Object.keys(carrito).length === 0) {
        footer.innerHTML = `
        <th scope="row" colspan="5">Carrito vacío. ¡Comience a ordenar!</th>
        `
        return
    }
    
    // sumar cantidad y sumar totales
    const nCantidad = Object.values(carrito).reduce((acc, { cantidad }) => acc + cantidad, 0)
    const nPrecio = Object.values(carrito).reduce((acc, {cantidad, precio}) => acc + cantidad * precio ,0)
    // console.log(nPrecio)

    templateFooter.querySelectorAll('td')[0].textContent = nCantidad
    templateFooter.querySelector('span').textContent = nPrecio

    const clone = templateFooter.cloneNode(true)
    fragment1.appendChild(clone)

    footer.appendChild(fragment1)

    const boton = document.querySelector('#vaciar-carrito')
    boton.addEventListener('click', () => {
        carrito = {}
        pintarCarrito()
    })

}

const btnAumentarDisminuir = e => {
    // console.log(e.target.classList.contains('btn-info'))
    if (e.target.classList.contains('btn-info')) {
        const producto = carrito[e.target.dataset.id]
        producto.cantidad++
        carrito[e.target.dataset.id] = { ...producto }
        pintarCarrito()
    }

    if (e.target.classList.contains('btn-danger')) {
        const producto = carrito[e.target.dataset.id]
        producto.cantidad--
        if (producto.cantidad === 0) {
            delete carrito[e.target.dataset.id]
        } else {
            carrito[e.target.dataset.id] = {...producto}
        }
        pintarCarrito()
    }
    e.stopPropagation()
}


//Boton Ordenar
const btnOrdenar = document.getElementById('btnOrdenar')