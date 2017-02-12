import os
import sys
from consts import *

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


def process_file(filename):
    with open(filename, 'rb') as f:
        elf_file = ELFFile(f)

        dynsym_name = '.dynsym'
        dynsym = elf_file.get_section_by_name(dynsym_name) # type: SymbolTableSection

        # Get all the functions names we want to override:
        func_names = []
        blacklist = ["_init", "_fini", "__fpending"]
        for symbol in dynsym.iter_symbols():
            print(symbol.name)
            if symbol.name not in blacklist:
                func_names.append(symbol.name)
        return func_names


def generate_fake_lib(func_names):
    print("Generating wrapper lib source...")

    with open("fake_lib.s", "w") as f:
        f.write(macros)
        for name in filter(None, func_names):
            f.write(handler.format(name, len(name)+1)) # +1 for \n
        f.write("section .data")
        for name in filter(None, func_names):
            f.write(data.format(name))

    print("done.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename:
            func_names = process_file(filename)
            generate_fake_lib(func_names)

            print("Compiling wrapper lib...")
            os.system("nasm -f elf64 fake_lib.s")
            os.system("gcc -shared fake_lib.o -o libfake.so -ldl")
            print("done.")

            print(" STACKTRACE ".center(50, "v"))
            os.system("LD_PRELOAD=$PWD/libfake.so %s" % " ".join(sys.argv[1:]))

            os.system("rm fake_lib.o fake_lib.s libfake.so 2>/dev/null")
