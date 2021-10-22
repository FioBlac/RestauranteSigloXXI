const cards = document.getElementById('cards')
const items = document.getElementById('items')
const footer = document.getElementById('footer')
const templateCard = document.getElementById('template-card').content
//const templateFooter = document.getElementById('template-footer').content
//const templateCarrito = document.getElementById('template-carrito').content
const fragment = document.createDocumentFragment()
let carrito = {}

// Eventos
// El evento DOMContentLoaded es disparado cuando el documento HTML ha sido completamente cargado y parseado
document.addEventListener('DOMContentLoaded', e => { fetchData() });
//cards.addEventListener('click', e => { addCarrito(e) });
//items.addEventListener('click', e => { btnAumentarDisminuir(e) })

// Objeto producto
function Producto(nombre, precio, id) {
    this.nombre = nombre;
    this.precio = precio;
    this.id = id;
}

//Productos de ejemplo
var Productos = [
    new Producto('Ensalada Cesar', '2.000', 1),
    new Producto('Ensalada Juan', '3.000', 2),
    new Producto('Esalada Verdejo', '1.500', 3),
    new Producto('Ensaladita Ñam Ñam', '2.500', 4)
]

// Traer productos
const fetchData = async () => {
    pintarCards(Productos)
}

// Pintar productos
const pintarCards = Productos => {
    Productos.forEach(item => {
        templateCard.querySelector('h5').textContent = item.nombre
        templateCard.querySelector('p').textContent = item.precio
        templateCard.querySelector('button').dataset.id = item.id
        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    })
    cards.appendChild(fragment)
}