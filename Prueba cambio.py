
from rate_engine import obtener_euro_bcv, consulta_bcv, ConsultaTasasGuardadas, GuardarTasas

#consultabcv devuelve (TasaBcv, TasaPll, TasaPrm, fecha) en ese orden
#consultatasasguardadas devuelve (TasaBcv, tasa_euro, TasaPll, TasaPrm, fecha) en ese orden


teuro_dia=obtener_euro_bcv()
datos_bcv=consulta_bcv() #devuelve una lista

if teuro_dia and datos_bcv:
    #confirmar si tengo conexion primero
    tbcv_dia, tpll_dia, tprm_dia, fecha= datos_bcv
    tbcv_dia=round(tbcv_dia, 2)
    tpll_dia=round(tpll_dia, 2)
    tprm_dia=round(tprm_dia, 2)
    teuro_dia=round(teuro_dia, 2)
    GuardarTasas(tbcv_dia, tpll_dia, tprm_dia, teuro_dia, fecha)
    print(f"""
             BCV: {tbcv_dia}
             Euro: {teuro_dia}
             Promedio: {tprm_dia}
             Paralelo: {tpll_dia}
             Usando tasa oficial.

             """)
    
    
else:
    
    datos_guardados=ConsultaTasasGuardadas()
    if datos_guardados:
        tbcv_dia, teuro_dia, tpll_dia, tprm_dia, fecha= datos_guardados

        tbcv_dia=round(tbcv_dia, 2)
        tpll_dia=round(tpll_dia, 2)
        tprm_dia=round(tprm_dia, 2)
        teuro_dia=round(teuro_dia, 2)
        
        print(f"""
              BCV:{tbcv_dia}
             Euro:{teuro_dia}
             Promedio:{tprm_dia}
             Paralelo:{tpll_dia}
            Usando tasa oficial.

             """)
    
    else:
        print("no se pudo obtener ninguna tasa actual ni se encontró archivo de respaldo")
        exit()

while True:
    while True:
        try:
            entrada=input("\nIngrese un monto en usd:\t")
            precioref=float(entrada)
            if (precioref<=0 ):
                raise ValueError
            break
        except ValueError:
            print("\nValor invalido intente de nuevo\n")

    precioBs=round(tbcv_dia*precioref, 2)
    print(f"\nEl monto en bolivares es: {precioBs:.2f} Bs.S\n")

