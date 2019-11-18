transfer_functions = [
    (lambda e: e)
]

def order(a, b):
    if (a == "bottom" and b == "top"): return -1
    if (a == "bottom" and b == "0"): return -1
    if (a == "bottom" and b == "!0"): return -1
    if (a == "bottom" and b == "bottom"): return 0
    if (a == "top" and b == "bottom"): return 1
    if (a == "top" and b == "0"): return 1
    if (a == "top" and b == "!0"): return 1
    if (a == "top" and b == "top"): return 0
    if (a == "0" and b == "!0"): return 0
    if (a == "0" and b == "top"): return -1
    if (a == "0" and b == "bottom"): return 1
    if (a == "0" and b == "0"): return 0
    if (a == "!0" and b == "0"): return 0
    if (a == "!0" and b == "top"): return -1
    if (a == "!0" and b == "bottom"): return 1
    if (a == "!0" and b == "!0"): return 0
    
    else: 
        raise NameError()

from datatypes import Lattice, Analysis

lattice = Lattice(symbols=[
        ("bottom", "unknown"),
        ("top", "is either zero or not zero"),
        ("0", "must be zero"),
        ("!0", "may be not zero")
    ],
    ordering=order)

analysis = Analysis(lattice=lattice, transfer_functions=transfer_functions)