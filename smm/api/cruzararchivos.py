import pandas as pd
from django.http import HttpResponse
from smm.api.serializer import PagosSerializer, GestionSerializer
from smm.models import Pagos, Gestion
from rest_framework.views import APIView

class DescargarCsv(APIView):
 def get(self, request):
    # Obtén todos los datos de Gestion y Pagos
    Gestions = Gestion.objects.all()
    Pago = Pagos.objects.all()
   
    
    # Serializa los datos
    serializerGestion = GestionSerializer(Gestions, many=True)
    serializerPagos = PagosSerializer(Pago, many=True)
    
    # Convierte los datos serializados a listas de diccionarios
    dataGestion = [
        {
            'Codigo_Gestión': item['Codigo_gestion'],
            'Nombre_Asesor': item['Nombre_asesor'],
            'Numero_documento': item['Numero_documento'],
            'Fecha_gestion': item['Fecha_gestion'],
            'Resultado': item['Resultado']
        } 
        for item in serializerGestion.data
    ]
    fecha = dataGestion[0]
    fecha = pd.to_datetime(fecha.get("Fecha_gestion")).month
    print(fecha)
    dataPagos = [
        {
            'Cedula': itemP['Nit_cliente'],
            'Fecha_pago': itemP['Fecha_pago'],
            'Valor_pago': itemP['Valor_pago'],
        }
        for itemP in serializerPagos.data
        if pd.to_datetime(itemP["Fecha_pago"]).month == fecha
    ]
    
    
        
    dfGestion = pd.DataFrame(dataGestion)
    dfPagos = pd.DataFrame(dataPagos)

# Realiza la unión de los DataFrames
    dfJuntada = pd.merge(dfGestion, dfPagos, left_on='Numero_documento', right_on='Cedula', how='inner')    
  
    # Verifica que 'Numero_documento' y 'Cedula' no sean listas
    # if dfGestion['Numero_documento'].apply(lambda x: isinstance(x, list)).any():
    #     raise ValueError("El campo 'Numero_documento' contiene listas en lugar de valores simples.")
    # if dfPagos['Cedula'].apply(lambda x: isinstance(x, list)).any():
    #     raise ValueError("El campo 'Cedula' contiene listas en lugar de valores simples.")
    

    #  pd.merge(dfGestion, dfPagos, left_on='Numero_documento', right_on='Cedula', how='outer')
    
    # Crear una respuesta HTTP con el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Cruce_registro.csv"'
    
    # Exportar el DataFrame a CSV en la respuesta
    dfJuntada.to_csv(path_or_buf=response, index=False)
    
    return response
