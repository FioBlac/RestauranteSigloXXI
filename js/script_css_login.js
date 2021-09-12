//Function login cliente
function loginCli(){
    var user = "cliente@cliente.com";
    var passwd = "cliente";

    if(document.getElementById("txtLoginEmail").value == user && document.getElementById("txtLoginPassword").value == passwd){
        window.location = "indexLogin.html";
    }else{
        alert("Datos incorrectos, por favor intentelo nuevamente")
    }
    
}