# HackAssembler

Ensamblador en Python para pasar de `.asm` a `.hack`.
Incluye soporte normal de Hack y corrimientos.

## Estructura
- `docs/`: documentación
- `src/`: código
  - `HackAssembler.py`

## Uso rápido
```bash
cd src
python3 HackAssembler.py Prog.asm
```

# HackDisassembler

Este proyecto contiene un programa en Python que lee un archivo `.hack` y lo convierte a código ensamblador Hack.

## Ejecutar

1. Copia o mueve el archivo `.hack` a la carpeta `proyecto3`.
2. Ejecuta:

```bash
python HackDisassembler.py -d Prog.hack
```

3. El programa generará un archivo llamado `ProgDis.asm` en la misma carpeta.

## Notas

- El archivo de entrada debe tener una instrucción binaria de 16 bits por línea.
- Si hay un error en alguna línea, el programa mostrará el mensaje de error con el número de línea y no dejará un archivo de salida incompleto.
- Si todo está bien, no muestra mensajes en pantalla.
