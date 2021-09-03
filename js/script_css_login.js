document.getElementById("btn_registro").addEventListener("click", animacionRegister);
document.getElementById("btn_iniciar-sesion").addEventListener("click", animacionIniciarSesion);
document.getElementById("btn_loginUser").addEventListener("click", iniciarSesion);

window.addEventListener("resize", anchoPagina);

//Declarar variables de animaciones
var contenedor_login_registro = document.querySelector(".contenedor_login-registro");
var formulario_login = document.querySelector(".form_login");
var formulario_registro = document.querySelector(".form_registro");
var caja_trasera_login = document.querySelector(".caja_trasera-login");
var caja_trasera_registro = document.querySelector(".caja_trasera-registro");


//Function para animaciones
function anchoPagina(){
    if(window.innerWidth > 850){
        caja_trasera_login.style.display = "block";
        caja_trasera_registro.style.display = "block";
    }else{
        caja_trasera_registro.style.display = "block";
        caja_trasera_registro.style.opacity = "1";
        caja_trasera_login.style.display = "none";
        formulario_login.style.display = "block";
        contenedor_login_registro.style.left = "0px";
        formulario_registro.style.display = "none";
        
    }
}
anchoPagina();


function animacionIniciarSesion(){
    if(window.innerWidth > 850){
        formulario_login.style.display = "block";
        contenedor_login_registro.style.left= "10px";
        formulario_registro.style.display= "none";
        caja_trasera_registro.style.opacity = "1";
        caja_trasera_login.style.opacity = "0";
    }else{
        formulario_login.style.display = "block";
        contenedor_login_registro.style.left= "0px";
        formulario_registro.style.display= "none";
        caja_trasera_registro.style.display = "block";
        caja_trasera_login.style.display = "none";
    }
    
}

function animacionRegister(){
    if(window.innerWidth > 850){
        formulario_registro.style.display = "block";
        contenedor_login_registro.style.left= "410px";
        formulario_login.style.display= "none";
        caja_trasera_registro.style.opacity = "0";
        caja_trasera_login.style.opacity = "1";
    }else{
        formulario_registro.style.display = "block";
        contenedor_login_registro.style.left= "0px";
        formulario_login.style.display= "none";
        caja_trasera_registro.style.display = "none";
        caja_trasera_login.style.display = "block";
        caja_trasera_login.style.opacity = "1";

    }
    
}

//Login


//var user = document.getElementById("txtLoginEmail").value;
//var password = document.getElementById("txtLoginPassword").value;

//Function login
function iniciarSesion(){
    if(document.getElementById("txtLoginEmail").value == "admin@admin.com" && document.getElementById("txtLoginPassword").value == "admin"){
        alert("Usuario y contraseña verificados correctamente");
    }else{
        alert("Combinación de credenciales incorrecta");
    }
}