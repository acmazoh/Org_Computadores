<<<<<<< HEAD
"""
/***
* "HackDisassembler.py" - Lee un archivo .hack y traduce su contenido a assembler Hack.
* Autor 1: Samuel Montoya
* Autor 2: Andrés Mazo
***/
"""

import argparse
import os
import sys
from pathlib import Path


class HackDisassembler:

    COMP_TABLE = {
        "0101010": "0",
        "0111111": "1",
        "0111010": "-1",
        "0001100": "D",
        "0110000": "A",
        "1110000": "M",
        "0001101": "!D",
        "0110001": "!A",
        "1110001": "!M",
        "0001111": "-D",
        "0110011": "-A",
        "1110011": "-M",
        "0011111": "D+1",
        "0110111": "A+1",
        "1110111": "M+1",
        "0001110": "D-1",
        "0110010": "A-1",
        "1110010": "M-1",
        "0000010": "D+A",
        "1000010": "D+M",
        "0010011": "D-A",
        "1010011": "D-M",
        "0000111": "A-D",
        "1000111": "M-D",
        "0000000": "D&A",
        "1000000": "D&M",
        "0010101": "D|A",
        "1010101": "D|M",
    }

    DEST_TABLE = {
        "000": "",
        "001": "M",
        "010": "D",
        "011": "DM",
        "100": "A",
        "101": "AM",
        "110": "AD",
        "111": "ADM",
    }

    JUMP_TABLE = {
        "000": "",
        "001": "JGT",
        "010": "JEQ",
        "011": "JGE",
        "100": "JLT",
        "101": "JNE",
        "110": "JLE",
        "111": "JMP",
    }

    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        self.output_path = self._build_output_path()

    def _build_output_path(self) -> Path:
        stem = self.input_path.stem
        if self.input_path.suffix.lower() == ".hack":
            return self.input_path.with_name(f"{stem}Dis.asm")
        return self.input_path.with_suffix("Dis.asm")

    def translate(self) -> None:
        lines = self._read_input_lines()
        self._write_output(lines)

    def _read_input_lines(self) -> list[str]:
        if not self.input_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo {self.input_path}")

        with self.input_path.open("r", encoding="utf-8") as source:
            raw_lines = source.readlines()

        translated_lines = []
        for index, raw_line in enumerate(raw_lines, start=1):
            line = raw_line.strip()
            if not line:
                raise SyntaxError(f"Error en la línea {index}: línea vacía o espacios en blanco")
            if len(line) != 16:
                raise SyntaxError(
                    f"Error en la línea {index}: cada línea debe tener exactamente 16 caracteres, se encontraron {len(line)}"
                )
            if any(char not in "01" for char in line):
                raise SyntaxError(f"Error en la línea {index}: caracteres inválidos, solo se permiten 0 y 1")
            translated_lines.append(self._translate_instruction(line, index))

        return translated_lines

    def _translate_instruction(self, bits: str, line_number: int) -> str:
        if bits[0] == "0":
            return self._translate_a_instruction(bits)

        if bits[:3] != "111":
            raise SyntaxError(f"Error en la línea {line_number}: instrucción C inválida, los primeros tres bits deben ser 111")

        return self._translate_c_instruction(bits, line_number)

    @staticmethod
    def _translate_a_instruction(bits: str) -> str:
        value = int(bits, 2)
        return f"@{value}"

    def _translate_c_instruction(self, bits: str, line_number: int) -> str:
        comp_bits = bits[3:10]
        dest_bits = bits[10:13]
        jump_bits = bits[13:16]

        comp = self.COMP_TABLE.get(comp_bits)
        if comp is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo comp inválido '{comp_bits}'")

        dest = self.DEST_TABLE.get(dest_bits)
        if dest is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo dest inválido '{dest_bits}'")

        jump = self.JUMP_TABLE.get(jump_bits)
        if jump is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo jump inválido '{jump_bits}'")

        parts = []
        if dest:
            parts.append(f"{dest}=")
        parts.append(comp)
        if jump:
            parts.append(f";{jump}")

        return "".join(parts)

    def _write_output(self, translated_lines: list[str]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", encoding="utf-8") as target:
            for line in translated_lines:
                target.write(f"{line}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HackDisassembler: traduce un archivo .hack a assembler Hack"
    )
    parser.add_argument(
        "-d",
        dest="input_path",
        required=True,
        help="Archivo .hack de entrada",
    )

    args = parser.parse_args()
    disassembler = HackDisassembler(args.input_path)

    try:
        disassembler.translate()
    except (FileNotFoundError, SyntaxError) as exc:
        if disassembler.output_path.exists():
            try:
                disassembler.output_path.unlink()
            except OSError:
                pass
        print(exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
=======
"""
/***
* "HackDisassembler.py" - Lee un archivo .hack y traduce su contenido a assembler Hack.
* Autor 1: Samuel Montoya
* Autor 2: Andrés Mazo
***/
"""

import argparse
import os
import sys
from pathlib import Path


class HackDisassembler:

    COMP_TABLE = {
        "0101010": "0",
        "0111111": "1",
        "0111010": "-1",
        "0001100": "D",
        "0110000": "A",
        "1110000": "M",
        "0001101": "!D",
        "0110001": "!A",
        "1110001": "!M",
        "0001111": "-D",
        "0110011": "-A",
        "1110011": "-M",
        "0011111": "D+1",
        "0110111": "A+1",
        "1110111": "M+1",
        "0001110": "D-1",
        "0110010": "A-1",
        "1110010": "M-1",
        "0000010": "D+A",
        "1000010": "D+M",
        "0010011": "D-A",
        "1010011": "D-M",
        "0000111": "A-D",
        "1000111": "M-D",
        "0000000": "D&A",
        "1000000": "D&M",
        "0010101": "D|A",
        "1010101": "D|M",
    }

    DEST_TABLE = {
        "000": "",
        "001": "M",
        "010": "D",
        "011": "DM",
        "100": "A",
        "101": "AM",
        "110": "AD",
        "111": "ADM",
    }

    JUMP_TABLE = {
        "000": "",
        "001": "JGT",
        "010": "JEQ",
        "011": "JGE",
        "100": "JLT",
        "101": "JNE",
        "110": "JLE",
        "111": "JMP",
    }

    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        self.output_path = self._build_output_path()

    def _build_output_path(self) -> Path:
        stem = self.input_path.stem
        if self.input_path.suffix.lower() == ".hack":
            return self.input_path.with_name(f"{stem}Dis.asm")
        return self.input_path.with_suffix("Dis.asm")

    def translate(self) -> None:
        lines = self._read_input_lines()
        self._write_output(lines)

    def _read_input_lines(self) -> list[str]:
        if not self.input_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo {self.input_path}")

        with self.input_path.open("r", encoding="utf-8") as source:
            raw_lines = source.readlines()

        translated_lines = []
        for index, raw_line in enumerate(raw_lines, start=1):
            line = raw_line.strip()
            if not line:
                raise SyntaxError(f"Error en la línea {index}: línea vacía o espacios en blanco")
            if len(line) != 16:
                raise SyntaxError(
                    f"Error en la línea {index}: cada línea debe tener exactamente 16 caracteres, se encontraron {len(line)}"
                )
            if any(char not in "01" for char in line):
                raise SyntaxError(f"Error en la línea {index}: caracteres inválidos, solo se permiten 0 y 1")
            translated_lines.append(self._translate_instruction(line, index))

        return translated_lines

    def _translate_instruction(self, bits: str, line_number: int) -> str:
        if bits[0] == "0":
            return self._translate_a_instruction(bits)

        if bits[:3] != "111":
            raise SyntaxError(f"Error en la línea {line_number}: instrucción C inválida, los primeros tres bits deben ser 111")

        return self._translate_c_instruction(bits, line_number)

    @staticmethod
    def _translate_a_instruction(bits: str) -> str:
        value = int(bits, 2)
        return f"@{value}"

    def _translate_c_instruction(self, bits: str, line_number: int) -> str:
        comp_bits = bits[3:10]
        dest_bits = bits[10:13]
        jump_bits = bits[13:16]

        comp = self.COMP_TABLE.get(comp_bits)
        if comp is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo comp inválido '{comp_bits}'")

        dest = self.DEST_TABLE.get(dest_bits)
        if dest is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo dest inválido '{dest_bits}'")

        jump = self.JUMP_TABLE.get(jump_bits)
        if jump is None:
            raise SyntaxError(f"Error en la línea {line_number}: campo jump inválido '{jump_bits}'")

        parts = []
        if dest:
            parts.append(f"{dest}=")
        parts.append(comp)
        if jump:
            parts.append(f";{jump}")

        return "".join(parts)

    def _write_output(self, translated_lines: list[str]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", encoding="utf-8") as target:
            for line in translated_lines:
                target.write(f"{line}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HackDisassembler: traduce un archivo .hack a assembler Hack"
    )
    parser.add_argument(
        "-d",
        dest="input_path",
        required=True,
        help="Archivo .hack de entrada",
    )

    args = parser.parse_args()
    disassembler = HackDisassembler(args.input_path)

    try:
        disassembler.translate()
    except (FileNotFoundError, SyntaxError) as exc:
        if disassembler.output_path.exists():
            try:
                disassembler.output_path.unlink()
            except OSError:
                pass
        print(exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
>>>>>>> 8bb2470e3f64adcef530f808d72b61ceaf8dda7a
