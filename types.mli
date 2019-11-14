module type Types

(* TODO: Define environment type *)
type environment = []

(* TODO: Define function definition *)
type transfer_function = environment -> environment

type lattice = {
    set: (string * string) list;
    ordering: (string -> string -> int);
}

type analysis = {
    lattice: lattice;
    transfer_functions: transfer_function list;
}