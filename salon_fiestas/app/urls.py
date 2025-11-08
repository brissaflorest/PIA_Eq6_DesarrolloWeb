from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('listar/', views.listar_reservaciones, name='listar'),
    path('listar_empleado/', views.listar_empleado, name='listar_empleado'),
    path('marcar_listo/<int:id>/', views.marcar_listo, name='marcar_listo'),
    path('crear/', views.crear_reservacion, name='crear'),
    path('editar/<int:id>/', views.editar_reservacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_reservicion, name='eliminar'),
]