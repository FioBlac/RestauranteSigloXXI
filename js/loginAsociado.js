//Function login asociado
function loginAsoci(){
    var user = "admin@admin.com";
    var passwd = "admin";

    if(document.getElementById("userAsoci").value == user && document.getElementById("passAsoci").value == passwd){
        window.location = "/html/admin/index_admin.html";
    }else{
        alert("Datos incorrectos, por favor intentelo nuevamente")
    }
    
}