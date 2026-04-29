# Diseño

## Diagrama de clases (Assembler + Disassembler)

```mermaid
classDiagram
    class HackAssembler {
      +cargar_comandos(ruta_entrada)
      +primera_pasada(comandos, simbolos)
      +segunda_pasada(comandos, simbolos)
      +ensamblar(ruta_entrada)
    }

    class ErrorEnsamblador {
      +numero_linea
      +mensaje
      +__str__()
    }

    class HackDisassembler {
      +COMP_TABLE
      +DEST_TABLE
      +JUMP_TABLE
      +translate()
      -_build_output_path()
      -_read_input_lines()
      -_translate_instruction(bits, line_number)
      -_translate_a_instruction(bits)
      -_translate_c_instruction(bits, line_number)
      -_write_output(translated_lines)
    }

    HackAssembler ..> ErrorEnsamblador : usa
```

## Resumen de funcionamiento

### Ensamblador (`HackAssembler.py`)
- Lee un `.asm`.
- Hace dos pasadas para resolver etiquetas/símbolos.
- Traduce A/C a binario y genera `.hack`.
- Si hay error, informa línea y elimina salida parcial.

### Desensamblador (`HackDisassembler.py`)
- Lee un `.hack`.
- Valida formato de línea (16 bits, solo 0/1).
- Traduce instrucciones A/C a `.asm`.
- Genera salida `<nombre>Dis.asm`.
- Si hay error, informa línea y elimina salida parcial.
