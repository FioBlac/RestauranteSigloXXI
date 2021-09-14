//Guardar reserva
const btnReservar = document.querySelector('#btnReservar')

btnReservar.addEventListener('click', () => {
    //Obtener Fecha
    var fechaReserva = document.querySelector('#fechaReserva').value

    //Obtener Personas
    var cantPersonas = document.getElementById('cantPersonas').selectedOptions[0].text //obtiene el listado entero

    //Obtener Hora
    const horaReserva = document.getElementsByName('hora')
    let selectedValue;

    //Obtener Comentario
    const coment = document.getElementById('comentario').value


    //Seleccionar la hora elegida.
    for(i=0; i<horaReserva.length; i++){
        if(horaReserva[i].checked){
            selectedValue=horaReserva[i].value;
            if (document.getElementById(selectedValue).className.includes(" ocupado") ) {
                alert('Hora ya ocupada. Por favor, selecciona otra hora a reservar.')
            } else {
                document.getElementById(selectedValue).className += " ocupado"
                alert('Reserva hecha correctamente: Fecha '+fechaReserva+ ' a las '+selectedValue +' para ' +cantPersonas +'.'+
                    ' Comentario: ' + coment)
            } 
        } 
    }
    
    
})