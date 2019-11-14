module ExampleAnalysis = struct

type symbol = 
    | Bottom
    | Top
    | Zero
    | Not_zero

let string_to_union s = 
    match s with 
    | "bottom" -> Bottom
    | "top" -> Top
    | "0" -> Zero
    | "!0" -> Not_zero
    | _ -> raise Not_found

let transfer_functions = [
    fun e -> e
]

let order a b = 
    let a_u = string_to_union a in 
    let b_u = string_to_union b in 
    match a_u, b_u with 
    | Bottom, Top -> -1
    | Bottom, Zero -> -1
    | Bottom, Not_zero -> -1
    | Bottom, Bottom -> 0
    | Top, Bottom -> 1
    | Top, Zero -> 1
    | Top, Not_zero -> 1
    | Top, Top -> 0
    | Zero, Not_zero -> 0
    | Zero, Top -> -1
    | Zero, Bottom -> 1
    | Zero, Zero -> 0
    | Not_zero, Zero -> 0
    | Not_zero, Top -> -1
    | Not_zero, Bottom -> 1
    | Not_zero, Not_zero -> 0

let lattice = {
    set = [
        ("bottom", "unknown"); 
        ("top", "is either zero or not zero"); 
        ("0", "must be zero"); 
        ("!0", "may be not zero")
    ];
    ordering = order;
}

let analysis = {
    lattice = lattice;
    transfer_functions = transfer_functions;
}
end

;;
Linkage.provide (Analysis.AnalysisPlugin (module ExampleAnalysis))