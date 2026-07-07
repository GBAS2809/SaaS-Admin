import requests
import json
import customtkinter

from requests.exceptions import ConnectionError

#Debo limpiar esta parte del c[odigo, es la mas messy de todas las demas

def consulta_bcv():
    urlBCV="https://ve.dolarapi.com/v1/dolares/oficial"
    urlPll="https://ve.dolarapi.com/v1/dolares/paralelo"
    #en este bloque le pido la https la peticion con requests
    
    try:
    
        pet1 = requests.get(urlBCV, timeout=10)
        pet2 = requests.get(urlPll, timeout=10)

        #lanzamos error si el resultado no  es 200
        pet1.raise_for_status
        #esta parte pide por debug los codigos de operacion
        debug1=pet1.status_code
        debug2=pet2.status_code
        
        #lleno los datos del json en un diccionario para python datos_of y datos_p
        datos_of = pet1.json()
        datos_p = pet2.json()

        #para evitar que el programa explote cuando el json esta vacio le asigno un valor default
        #Esto convierte el texto en un Diccionario de Python
        TasaBcv=datos_of.get('promedio', 0)
        TasaPll=datos_p.get('promedio', 0)


        if TasaBcv > 0 and TasaPll > 0:
            TasaPrm= (TasaBcv+TasaPll)/2
        else: 
            TasaPll=0


        fecha = datos_of.get('fechaActualizacion', "Sin fecha")
        return(TasaBcv, TasaPll, TasaPrm, fecha)

    except requests.exceptions.RequestException as e: 
        #print(f"Problemas para acceder al servidor: {e}\n")
        win=customtkinter.CTk()
        win.title=("Error")
        win.geometry("200x200")
        win.mainloop()
        return None



        
        
        
import requests
from bs4 import BeautifulSoup
import urllib3
#Apartir de esta parte del bloque se busca la tasa del euro usando web scrapping
# Desactivar advertencias de certificados (el BCV suele tener problemas con ellos)


def obtener_euro_bcv():
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://www.bcv.org.ve/"
    # El User-Agent es vital para que el servidor no te bloquee pensando que eres un bot malicioso
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        # verify=False porque el certificado SSL del BCV falla a menudo
        response = requests.get(url, headers=headers, verify=False, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # El BCV organiza las tasas en contenedores con IDs específicos
        # Buscamos el div que contiene el Euro
        contenedor_euro = soup.find('div', {'id': 'euro'})
        
        if contenedor_euro:
            # Buscamos la etiqueta <strong> dentro de ese div
            tasa = contenedor_euro.find('strong').text.strip()
            # Limpiamos la string: cambiamos coma por punto para poder convertir a float
            tasa_float = float(tasa.replace(',', '.'))
            return tasa_float
        else:
            #print("No se encontró el contenedor del Euro.")
            return None

    except Exception as e:
        #print(f"Error haciendo scraping al BCV: {e}")
        win=customtkinter.CTk()
        win.title=("!Error")
        win.geometry("200x200")
        win.mainloop()
        return None

# Prueba

#get rate lo que hace es ejecutar ambos consultas al mismo tiempo guardarlas si las logra realizar  y si no devolver
#las últimas tasas guardadas
def GetRates():

    teuro=obtener_euro_bcv()
    datos_bcv=consulta_bcv()


    if teuro and datos_bcv:
        tbcv_dia, tpll_dia, tprm_dia, fecha = datos_bcv

        tbcv_dia=round(tbcv_dia, 2)
        tpll_dia=round(tpll_dia)
        tprm_dia=round(tprm_dia, 2)
        teuro=round(teuro, 2)


        GuardarTasas(tbcv_dia, tpll_dia, tprm_dia, teuro,  fecha)

        return tbcv_dia, tpll_dia, tprm_dia, teuro, fecha
    else:
      datos_rate=ConsultaTasasGuardadas()
      if datos_rate== None:
          exit()
      tbcv_dia, teuro, tpll_dia, tprm_dia, fecha=datos_rate
      return tbcv_dia, tpll_dia, tprm_dia, teuro, fecha

    


def GuardarTasas(TasaBcv, TasaPll, TasaPrm, tasa_euro, fecha):
 if tasa_euro and TasaBcv and TasaPll:
    #guardo los datos en un json para usarlos despues
    datos_json={
        "bcv": TasaBcv,
        "euro": tasa_euro,
        "paralelo": TasaPll,
        "promedio": TasaPrm,
        "fecha": fecha
    }
    with open("data_tasas.json", "w") as file:
        json.dump(datos_json, file, indent=4)
    #print("\n\tGuardado en data_tasas.json\n")
    #else:
    #print("\n\tno se pudo guardar en data_tasas.json\n")
    

def ConsultaTasasGuardadas():
    try:
        with open("data_tasas.json", "r") as filer: #file reading i guess
            datos=json.load(filer)
        fecha= datos.get('fecha')
        #print(f"Trabajando con el respaldo de\t {fecha[0:10]} {fecha[11:19]}")
    
        #print(" cargando desde la última consulta...")
        return (datos['bcv'], 
            datos['euro'],
            datos['paralelo'],
            datos['promedio'],
            datos['fecha'])
    except FileNotFoundError:
        #print("\nNo se encontró archivo de respaldo existente\n")
        return None
    except Exception as e:
        #print("Fallo al intentar leer el archivo: \n\n{e}")
        return None
    

#solo se ejecuta cuando es el programa principal, no al importar el archivo
if __name__ == "__main__":
    if consulta_bcv()!=None and obtener_euro_bcv()!=None:

        tasa_euro = obtener_euro_bcv()
        TasaBcv, TasaPll, TasaPrm, fecha= consulta_bcv()

        round(tasa_euro, 2)
        round(TasaBcv,2)
        round(TasaPll, 2)
        round(TasaPll, 2)

        GuardarTasas(TasaBcv, TasaPll, TasaPrm, tasa_euro, fecha)
        print(f"""\n\nPrecio oficial {TasaBcv:.2f} Bs.S\n
        Precio euro {tasa_euro:.2f}\n
        Precio paralelo {TasaPll:.2f} Bs.S\n
        Precio Promedio {TasaPrm:.2f} Bs.S\n
        Última actualizacion del dolar: {fecha[0:10] } a las {fecha[11:19]}\n\t
        """)
        
        
    else:    
        print("\nNo hay conexion con las páginas\n\n")
        TasaBcv, tasa_euro, TasaPll, TasaPrm, fecha=ConsultaTasasGuardadas()

        print(f"""\n\nPrecio oficial {TasaBcv:.2f} Bs.S\n
        Precio euro {tasa_euro:.2f}\n
        Precio paralelo {TasaPll:.2f} Bs.S\n
        Precio Promedio {TasaPrm:.2f} Bs.S\n
        Última actualizacion del dolar: {fecha[0:10] } a las {fecha[11:19]}\n\t
        """)
        




