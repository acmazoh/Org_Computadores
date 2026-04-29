# Changelog - HackAssembler

##  Proyecto 3

- Implementación del ensamblador Hack en:
  - `proyecto3/HackAssembler/src/HackAssembler.py`
- Soporte de traducción `.asm` -> `.hack` con:
  - instrucciones tipo A,
  - instrucciones tipo C,
  - etiquetas y resolución de símbolos en dos pasadas.
- Soporte de corrimientos extendidos en `comp`:
  - `<<` y `>>`.
- Manejo de errores con línea (`ErrorEnsamblador`) y eliminación de salida parcial en fallos.
- Documentación del ensamblador:
  - `proyecto3/HackAssembler/README.md`
  - `proyecto3/HackAssembler/docs/API.md`
  - `proyecto3/HackAssembler/docs/DESIGN.md`
  - `proyecto3/HackAssembler/docs/USER_GUIDE.md`
- Script de pruebas básicas:
  - `proyecto3/HackAssembler/test/HackAssemblerTest.py`

### Verified
- Ejecución manual desde `src`:
  - `python3 HackAssembler.py Prog.asm`
- Ejecución de pruebas:
  - `python3 proyecto3/HackAssembler/test/HackAssemblerTest.py`
