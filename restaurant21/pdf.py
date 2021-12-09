from os import name
from jinja2 import environment, FileSystemLoader, loaders

env = environment(loader=FileSystemLoader("Cajero"))
Cajero = env.get_Cajero("Cajero.html")

usuario = {
    'Id_pedido' : '',
    'Precio pagado' : 2000,
    'Fecha de pago' : '',
}