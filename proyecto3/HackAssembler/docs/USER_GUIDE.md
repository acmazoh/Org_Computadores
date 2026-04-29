# Guía de uso

## Requisitos
- Python 3

---

## 1) Ensamblador 

### Comando
Desde `proyecto3/HackAssembler/src`:

```bash
python3 HackAssembler.py Prog.asm
```

### Qué necesitas
- `Prog.asm` debe existir antes de ejecutar.

### Resultado esperado
- Genera `Prog.hack`.
- Si todo sale bien, no imprime nada.
- Si hay error, muestra línea y mensaje.

---

## 2) Desensamblador 

### Comando
Desde `proyecto3/HackAssembler/src`:

```bash
python3 HackDisassembler.py -d Prog.hack
```

### Qué necesitas
- `Prog.hack` debe existir antes de ejecutar.

### Resultado esperado
- Genera `ProgDis.asm`.
- Si todo sale bien, no imprime nada.
- Si hay error de formato o archivo, muestra el error y se detiene.

---
