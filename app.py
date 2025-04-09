import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

consulta = ''

url = "https://190.2.251.208:50000/b1s/v1"
url_login = f"{url}/Login"

credenciales = {
    
}

login = requests.Session()

try:
    # Autenticación
    login_response = login.post(
        url_login,
        json=credenciales,
        verify=False
    )
    
    if login_response.status_code != 200:
        print(f"Error en login: {login_response.status_code} - {login_response.text}")
        exit()
        
    print("Login exitoso!")
    
    consulta = input("ingresa codigo SAP: ")
    
    url_items = f"{url}/Items?$select=ItemWarehouseInfoCollection&$filter=ItemCode eq '{consulta}'"
    
    
    # Obtener datos del ítem
    items_response = login.get(
        url_items,
        verify=False
    )
    
    if items_response.status_code != 200:
        print(f"Error al obtener ítems: {items_response.status_code} - {items_response.text}")
        exit()
        
    items = items_response.json()
    
    if 'value' in items and len(items['value']) > 0:
        warehouse_info = items['value'][0].get('ItemWarehouseInfoCollection', [])
        
        for warehouse in warehouse_info:
            print(f"Almacén: {warehouse['WarehouseCode']}, Stock: {warehouse['InStock']}")
    
    else:
        print("No se encontraron datos del ítem")

except Exception as e:
    print(f"Error: {str(e)}")