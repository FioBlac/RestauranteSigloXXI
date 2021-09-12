//Function login
function iniciarSesion(){
    if(document.getElementById("txtLoginEmail").value == "admin@admin.com" && document.getElementById("txtLoginPassword").value == "admin"){
        alert("Usuario y contraseña verificados correctamente");
    }else{
        alert("Combinación de credenciales incorrecta");
    }
}