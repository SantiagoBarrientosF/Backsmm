from django.urls import path
from smm.api.views import CargarArchivoExcelView
from smm.api.views import CargarArchivoCvsView

urlpatterns = [
    path('cargar-archivo-excel/', CargarArchivoExcelView.as_view(), name='cargar-archivo-excel'),
    path('cargar-pagos/', CargarArchivoCvsView.as_view(), name='cargar-pagos')
]
