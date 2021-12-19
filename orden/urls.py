from django.urls import  path
from .import views
from .views import modificar_orden, listar_orden

urlpatterns = [
    path('', views.orden, name='orden'),
    path('confirmacion', views.confirmacion, name='confirmacion'),
    path('cancelar', views.cancelar_orden, name='cancelar'),  
    path('completado', views.completado, name='completado'),  
    path('completados', views.OrdenViews.as_view(), name='completados'),  
    path('modificar_orden/<id>/', modificar_orden, name='modificar_orden'),  
    path('listar_orden', listar_orden, name='listar_orden'),  
    

]
