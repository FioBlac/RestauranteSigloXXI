from django.urls import  path
from  .import views

urlpatterns = [
    path('', views.orden, name='orden'),
    path('confirmacion', views.confirmacion, name='confirmacion'),
    path('cancelar', views.cancelar_orden, name='cancelar'),  
    path('completado', views.completado, name='completado'),  
    path('completados', views.OrdenViews.as_view(), name='completados'),  

]
