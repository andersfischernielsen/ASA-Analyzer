from typing import Callable

environment = []

class Lattice:
    symbols: [(str, str)]

    def __init__(self, symbols):
        self.symbols = symbols

class Analysis:
    lattice: Lattice
    transfer_functions: [Callable[[list, str, str], list]]

    def __init__(self, lattice, transfer_functions):
        self.lattice = lattice
        self.transfer_functions = transfer_functions

    def get_lattice(self):
        return self.lattice
    
    def get_transfer_functions(self):
        return self.transfer_functions