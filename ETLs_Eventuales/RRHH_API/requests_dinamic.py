#Librerias Necesarias

from datetime import datetime, timedelta #Manejo de fechas
import requests #Consulta de API´s
from requests.auth import HTTPBasicAuth #Para autenticación BASIC Auth
import json #Para conversión a JSON
import os #Para construcción de path del archivo de salida

# Función principal de consulta a las API's con autenticación BASIC AUTH
"""
La función recibe:
    - base_url : conformada con los campos correspondientes a cada una
    - Username y Password para la autenticación
    - Filter: cada api tendrá su propio filtro para la consulta
    - Ruta: ruta de la carpeta donde se exporta el archivo 
    - nombre_archivo: nombre con la extensión .json para cada api
    - Format: el formato con el que se lee la api
"""
def consulta_api(base_url, username, password, filter, ruta, nombre_archivo, format):
    try:
        # Conforma la url de la api, aplicando los filtros necesarios y el formato de salida
        api_url = f'{base_url}{filter}{format}' if filter else base_url
        # Guarda la respuesta del pedido GET de la api
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))

        # Valida el estado de la petición, 
        # Código 200 OK

        if response.status_code == 200:
            # Guarda en data el contenido json de la respuesta
            data = response.json()
            # Uso de la libreria json de python para converión correcta del formato
            data_json = json.dumps(data)
            # Crea el path del archivo json que exporta. conformado por la ruta de la carperta + en nombre del archivo
            file_path = os.path.join(ruta, nombre_archivo)
            # Abre el archivo creado con permiso de escritura y graba en él la información obtenida en data_json
            with open(file_path, 'w') as archivo:
                archivo.write(data_json)
        else:
            # Código 500 internal server Error
            # Código 400 Bad request
            print(f'Error en la solicitud: Código de estado {response.status_code} de la URL: {api_url}')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud: {e}')

# NECESARIOS PARA LA CONSULTA DE API MAESTRO EMPLEADOS

def consulta_maestro_empleados(username, password, ruta, format):
    base_url_maestro_empleados = (
        'https://api19preview.sapsf.com/odata/v2/EmpJob?$format=json'
        '&$select=businessUnitNav/name_es_ES,companyNav/name_es_ES,customString1Nav/externalName,customString4Nav/externalName_es_ES,'
        'departmentNav/name_es_ES,divisionNav/name_es_ES,locationNav/name,seqNumber,startDate,userId,userNav/firstName,userNav/lastName,workscheduleCode'
        '&$expand=businessUnitNav,companyNav,customString1Nav,customString4Nav,departmentNav,divisionNav,locationNav,userNav'
    )
    filter_maestro_empleados = ''
    nombre_archivo_maestro_empleados = 'maestro_empleados.json'
    consulta_api(base_url_maestro_empleados, username, password, filter_maestro_empleados, ruta, nombre_archivo_maestro_empleados, format)

def consulta_temporary_time_information(username, password, ruta, format):

    """
    StarDate = Hoy
    EndDate	= hoy - 5 días
    
    EL formato solicitado por la api para el filtro de fecha es "ISO-8601 date" AAAA-MM-DDT00:00:00.000Z
    """
    start_date = datetime.now()
    start_date_format = start_date.strftime("%Y-%m-%d") # Conversión al formato de fecha solicitado
    end_date = (start_date - timedelta(days=5)).strftime("%Y-%m-%d")
    hora = 'T00:00:00Z'

    base_url_temporary_time_information = (
        'https://api19preview.sapsf.com/odata/v2/TemporaryTimeInformation?$format=json'
        '&$select=endDate,externalCode,startDate,userId,workSchedule'
    )
    
    # Los registros menores o iguales (le) a la fecha actual y mayores o iguales (ge) a la fecha actual - 5 días
    filter_temporary_time_information = (
        f"&$filter=startDate le datetime'{start_date_format}{hora}' and endDate ge datetime'{end_date}{hora}'"
    )

    nombre_archivo_temporary_time_information = 'temporary_time_information.json'

    consulta_api(base_url_temporary_time_information, username, password, filter_temporary_time_information, ruta, nombre_archivo_temporary_time_information, format)

def consulta_employee_time_sheet(username, password, ruta, format):
    """
    Toma como filtro los últimos 5 días
    Filtrando por el campo bookingDate

    EL formato solicitado por la api para el filtro de fecha es "ISO-8601 date" AAAA-MM-DDT00:00:00.000Z
    """
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=5)).strftime("%Y-%m-%d")
    hora = 'T00:00:00Z'

    base_url_employee_time_sheet = (
        'https://api19preview.sapsf.com/odata/v2/EmployeeTimeSheet?$format=json'
        '&$select=absencesExistNav/es_ES,approvalStatus,employeeTimeSheetEntry/endTime,employeeTimeSheetEntry/physicalEndDate,'
        'employeeTimeSheetEntry/physicalStartDate,employeeTimeSheetEntry/quantityInHours,employeeTimeSheetEntry/startTime,'
        'employeeTimeSheetEntry/timeType,employeeTimeSheetEntry/timeTypeName,employeeTimeValuationResult/bookingDate,employeeTimeValuationResult/hours,'
        'employeeTimeValuationResult/payTypeExternalName,employeeTimeValuationResult/payTypeName,endDate,externalCode,startDate,userId'
        '&$expand=absencesExistNav,employeeTimeSheetEntry,employeeTimeValuationResult'
    )

    # Usa "ge" para indicar que son los registros Mayores o iguales a la fecha indicada
    filter_employee_time_sheet = (
        f"&$filter=employeeTimeValuationResult/bookingDate ge datetime'{start_date}{hora}'"
    )

    nombre_archivo_employee_time_sheet = 'employee_time_sheet.json'

    consulta_api(base_url_employee_time_sheet, username, password, filter_employee_time_sheet, ruta, nombre_archivo_employee_time_sheet, format)

def consulta_api_ausencias (username, password, ruta, format):
    """
    StarDate = Hoy
    EndDate	= hoy - 5 días
    
    EL formato solicitado por la api para el filtro de fecha es "ISO-8601 date" AAAA-MM-DDT00:00:00.000Z
    """
    start_date = datetime.now()
    start_date_format = start_date.strftime("%Y-%m-%d") # Conversión al formato de fecha solicitado
    end_date = (start_date - timedelta(days=5)).strftime("%Y-%m-%d")
    hora = 'T00:00:00Z'

    base_url_ausencias = (
        'https://api19preview.sapsf.com/odata/v2/EmployeeTime?$select=approvalStatus,endDate,endTime,externalCode,physicalEndDate,physicalStartDate,quantityInDays,quantityInHours,startDate,startTime,timeType,timeTypeNav/externalCode,timeTypeNav/externalName_es_ES,userId&$expand=timeTypeNav'
    )


        # Los registros menores o iguales (le) a la fecha actual y mayores o iguales (ge) a la fecha actual - 5 días
    filter_ausecias = (
        
        f"&$filter=approvalStatus eq 'APPROVED' and (timeType ne 'EX_NOA' and timeType ne 'HE' and timeType ne 'HS_COMP' and timeType ne 'NOAUT' and timeType ne 'RCHE' and timeType ne 'Regular_Working_Hours' and timeType ne 'REC_EX' and timeType ne 'TRABAJO' and timeType ne 'Break') and (startDate le datetime'{start_date_format}{hora}' and endDate ge datetime'{end_date}{hora}')"
    )

    nombre_archivo_ausencias = 'ausencias.json'

    consulta_api(base_url_ausencias, username, password, filter_ausecias, ruta, nombre_archivo_ausencias, format)

def main():
    # Credenciales de Autenticación BASIC AUTH
    username = 'SFAPI@ferrumsaT1'
    password = 'Sap2023!'

    # Ruta donde se exporta el archivo .json
    ruta = '//fe-files01/sap-ssff/Descargas SSFF/'
    
    # Formato de la API
    format = "&$format=json"

    consulta_maestro_empleados(username, password, ruta, format)
    consulta_employee_time_sheet(username, password, ruta, format)
    consulta_temporary_time_information(username, password, ruta, format)
    consulta_api_ausencias(username, password, ruta, format)

if __name__ == "__main__":
    main()
