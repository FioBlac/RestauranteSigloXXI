//Obtener Fecha
var fechaReserva = document.querySelector('#fechaReserva')
const btnFecha = document.querySelector(".hora")

btnFecha.addEventListener('click', () => {
    console.log(fechaReserva.value)
})

//Cambiar color a botón seleccionado
btnFecha.addEventListener('click', () =>{
    btnFecha.style.borderColor = "blue";
})