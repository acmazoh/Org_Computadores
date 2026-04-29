"""
/*********
* HackAssemblerTest.py - Pruebas básicas para validar el ensamblador Hack.
* Autor 1: Samuel Montoya
* Autor 2: Andrés Mazo
*********/
"""

import os
import shutil
import sys


RUTA_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if RUTA_SRC not in sys.path:
    sys.path.insert(0, RUTA_SRC)

import HackAssembler  


def escribir_archivo(ruta, contenido):
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def leer_lineas(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo.readlines() if linea.strip()]


def test_traduccion_basica(carpeta):
    print("\n[TEST 1] Traducción básica con shift")

    asm = """@2
DM=D+1
D=M<<1
AM=D>>1
(LOOP)
@LOOP
0;JMP
"""

    ruta_asm = os.path.join(carpeta, "Prog.asm")
    ruta_hack = os.path.join(carpeta, "Prog.hack")
    escribir_archivo(ruta_asm, asm)

    HackAssembler.ensamblar(ruta_asm)

    if not os.path.exists(ruta_hack):
        print("FALLO: No se creó Prog.hack")
        return False

    resultado = leer_lineas(ruta_hack)
    esperado = [
        "0000000000000010",
        "1110011111011000",
        "1111001001010000",
        "1110000011101000",
        "0000000000000100",
        "1110101010000111",
    ]

    if resultado == esperado:
        print("CORRECTO")
        return True

    print(" FALLO: El contenido generado no coincide con el esperado")
    print("Esperado:", esperado)
    print("Obtenido:", resultado)
    return False


def test_error_etiqueta_reservada(carpeta):
    print("\n[TEST 2] Error por etiqueta reservada")

    asm = """(SP)
@0
D=A
"""

    ruta_asm = os.path.join(carpeta, "Bad.asm")
    escribir_archivo(ruta_asm, asm)

    try:
        HackAssembler.ensamblar(ruta_asm)
        print(" FALLO: Debió lanzar ErrorEnsamblador y no lo hizo")
        return False
    except HackAssembler.ErrorEnsamblador:
        print(" CORRECTO")
        return True


def main():
    carpeta_pruebas = os.path.join(os.path.dirname(__file__), "tmp_test")

   
    if os.path.exists(carpeta_pruebas):
        shutil.rmtree(carpeta_pruebas)
    os.makedirs(carpeta_pruebas, exist_ok=True)

    ok1 = test_traduccion_basica(carpeta_pruebas)
    ok2 = test_error_etiqueta_reservada(carpeta_pruebas)

    print("\n========================")
    if ok1 and ok2:
        print(" TODOS LOS TESTS PASARON")
        codigo = 0
    else:
        print(" ALGÚN TEST FALLÓ")
        codigo = 1

   
    if os.path.exists(carpeta_pruebas):
        shutil.rmtree(carpeta_pruebas)

    return codigo


if __name__ == "__main__":
    raise SystemExit(main())