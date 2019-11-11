open Printf

type lattice = {
    set: char * string list;
    ordering: (string -> string -> int);
}

(* TODO: Define *)
type environment = []

(* TODO: Define *)
type transfer_function = environment -> environment

(* TODO: Define *)
let generate_graph lattice = 0

(* TODO: Define *)
let generate_AST path = 0

(* TODO: Define *)
let find_fixpoint graph ast transfer_functions: char list = []

(* TODO: Define *)
let apply_fixpoint fixpoint ast : string = ""

(* TODO: Define *)
let pretty_print transformed_program : string = ""

(* TODO: Define *)
let parse_lattice input: lattice * transfer_function list = 
    {} * []

(* TODO: Define *)
let parse_program path : string = ""

let analyze (lattice:lattice * transfer_functions:transfer_function list) (program:string) : string =
    let graph = generate_graph lattice in
    let ast = generate_AST program in 
    let found_fixpoint = find_fixpoint graph ast transfer_functions in
    let transformed = apply_fixpoint found_fixpoint ast in
    let pretty = pretty_print transformed in 
    pretty


let () =
    let lattices, transfer_functions = Array.get Sys.argv 0 |> parse_lattice in 
    let program = Array.get Sys.argv 3 |> parse_program in
  
    (* TODO: Implement folding over lattices, generating programs *)
    let output = "" 
    output
