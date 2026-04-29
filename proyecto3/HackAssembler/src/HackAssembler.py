"""
/*********
* HackAssembler.py - Ensambla archivos .asm de Hack a .hack en una sola fuente.
* Autor 1: Samuel Montoya
* Autor 2: Andrés Mazo
*********/
"""

import os
import re
import sys


TABLA_DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

TABLA_JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

TABLA_COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
    # Corrimiento extendido
    "D>>": "0000011",
    "D>>1": "0000011",
    "A>>": "0100011",
    "A>>1": "0100011",
    "M>>": "1000011",
    "M>>1": "1000011",
    "D<<": "0101001",
    "D<<1": "0101001",
    "A<<": "0001001",
    "A<<1": "0001001",
    "M<<": "1001001",
    "M<<1": "1001001",
}

SIMBOLOS_PREDEFINIDOS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}
for indice in range(16):
    SIMBOLOS_PREDEFINIDOS["R" + str(indice)] = indice

REGEX_SIMBOLO = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class ErrorEnsamblador(Exception):
    def __init__(self, numero_linea, mensaje):
        super().__init__(mensaje)
        self.numero_linea = numero_linea
        self.mensaje = mensaje

    def __str__(self):
        return "Error en línea " + str(self.numero_linea) + ": " + self.mensaje


def es_etiqueta(comando):
    return comando.startswith("(") and comando.endswith(")")


def is_a_instruction(comando):
    return comando.startswith("@")


def simbolo_valido(simbolo):
    return REGEX_SIMBOLO.match(simbolo) is not None


def normalizar_dest(destino):
    if destino == "":
        return ""

    permitidos = {"A", "D", "M"}
    vistos = []
    for caracter in destino:
        if caracter not in permitidos or caracter in vistos:
            return None
        vistos.append(caracter)

    grupo = set(vistos)
    if grupo == {"A"}:
        return "A"
    if grupo == {"D"}:
        return "D"
    if grupo == {"M"}:
        return "M"
    if grupo == {"A", "D"}:
        return "AD"
    if grupo == {"A", "M"}:
        return "AM"
    if grupo == {"D", "M"}:
        return "MD"
    if grupo == {"A", "D", "M"}:
        return "AMD"
    return None


def parse_c_instruction(comando):
    if comando.count("=") > 1 or comando.count(";") > 1:
        return None, None, None

    if "=" in comando:
        partes = comando.split("=", 1)
        destino = partes[0].strip()
        comp_y_salto = partes[1]
    else:
        destino = ""
        comp_y_salto = comando

    if ";" in comp_y_salto:
        partes = comp_y_salto.split(";", 1)
        comp = partes[0].strip().replace(" ", "")
        salto = partes[1].strip()
    else:
        comp = comp_y_salto.strip().replace(" ", "")
        salto = ""

    destino = normalizar_dest(destino)
    if destino is None:
        return None, None, None

    return destino, comp, salto


def load_commands(ruta_entrada):
    comandos = []
    with open(ruta_entrada, "r", encoding="utf-8") as archivo_entrada:
        lineas_crudas = archivo_entrada.readlines()

    numero_linea = 1
    for linea_cruda in lineas_crudas:
        linea_limpia = linea_cruda.split("//", 1)[0].strip()
        if linea_limpia != "":
            comandos.append((numero_linea, linea_limpia))
        numero_linea += 1

    return comandos


def primera_pasada(comandos, simbolos):
    direccion_rom = 0
    for numero_linea, comando in comandos:
        if es_etiqueta(comando):
            etiqueta = comando[1:-1].strip()
            if etiqueta == "" or not simbolo_valido(etiqueta):
                raise ErrorEnsamblador(numero_linea, "etiqueta inválida: '" + etiqueta + "'")
            if etiqueta in simbolos:
                raise ErrorEnsamblador(numero_linea, "etiqueta duplicada o reservada: '" + etiqueta + "'")
            simbolos[etiqueta] = direccion_rom
        else:
            direccion_rom += 1


def segunda_pasada(comandos, simbolos):
    lineas_salida = []
    siguiente_ram = 16

    for numero_linea, comando in comandos:
        if es_etiqueta(comando):
            continue

        if is_a_instruction(comando):
            simbolo = comando[1:].strip()
            if simbolo == "":
                raise ErrorEnsamblador(numero_linea, "instrucción A vacía")

            if simbolo.isdigit():
                valor = int(simbolo)
                if valor < 0 or valor > 32767:
                    raise ErrorEnsamblador(numero_linea, "constante fuera de rango: " + str(valor))
            else:
                if not simbolo_valido(simbolo):
                    raise ErrorEnsamblador(numero_linea, "símbolo inválido: '" + simbolo + "'")
                if simbolo not in simbolos:
                    simbolos[simbolo] = siguiente_ram
                    siguiente_ram += 1
                valor = simbolos[simbolo]

            lineas_salida.append(format(valor, "016b"))
            continue

        destino, comp, salto = parse_c_instruction(comando)
        if destino is None:
            raise ErrorEnsamblador(numero_linea, "instrucción C inválida: '" + comando + "'")

        bits_comp = TABLA_COMP.get(comp)
        bits_destino = TABLA_DEST.get(destino)
        bits_salto = TABLA_JUMP.get(salto)

        if bits_comp is None:
            raise ErrorEnsamblador(numero_linea, "comp inválido: '" + comp + "'")
        if bits_destino is None:
            raise ErrorEnsamblador(numero_linea, "dest inválido: '" + destino + "'")
        if bits_salto is None:
            raise ErrorEnsamblador(numero_linea, "jump inválido: '" + salto + "'")

        lineas_salida.append("111" + bits_comp + bits_destino + bits_salto)

    return lineas_salida


def ensamblar(ruta_entrada):
    if not ruta_entrada.endswith(".asm"):
        raise ValueError("El archivo de entrada debe tener extensión .asm")

    ruta_salida = os.path.splitext(ruta_entrada)[0] + ".hack"

    comandos = load_commands(ruta_entrada)
    simbolos = dict(SIMBOLOS_PREDEFINIDOS)

    primera_pasada(comandos, simbolos)
    lineas_maquina = segunda_pasada(comandos, simbolos)

    with open(ruta_salida, "w", encoding="utf-8") as archivo_salida:
        for linea in lineas_maquina:
            archivo_salida.write(linea + "\n")


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 HackAssembler.py Prog.asm")
        return 1

    ruta_entrada = sys.argv[1]
    ruta_salida = os.path.splitext(ruta_entrada)[0] + ".hack"

    try:
        ensamblar(ruta_entrada)
    except (ErrorEnsamblador, OSError, ValueError) as error:
        if os.path.exists(ruta_salida):
            os.remove(ruta_salida)
        print(str(error))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())