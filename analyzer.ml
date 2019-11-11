open Printf


(* TODO: Define CIL environment type *)
type environment = []

type transfer_function = environment -> environment

type lattice = {
    set: (string * string) list;
    ordering: (string -> string -> int);
}

type analysis = {
    lattice: lattice;
    transfer_functions: transfer_function list;
}

(* TODO: Define directed graph structure *)
type graph = int

(* TODO: Define graph parsing *)
let generate_graph lattice : graph = 0

(* TODO: Define EBA AST parsing *)
let generate_AST path = 0

let find_fixpoint graph ast transfer_functions: string list = 
    (* TODO: Define finding fixpoint *)
    let apply_transfer_functions graph ast transfer_functions: string list = [] in
    let rec rec_apply previous = 
        let res = apply_transfer_functions graph ast transfer_functions in
        if res == previous then res 
        else rec_apply res 
        in
    
    rec_apply (apply_transfer_functions graph ast transfer_functions)

(* TODO: Define applying fixpoint to AST resulting in a program *)
let apply_fixpoint fixpoint ast : string = ""

(* TODO: Define pretty-printing of AST application - might not be needed *)
let pretty_print transformed_program : string = ""

(* TODO: Define parsing lattices from user provided markup language file *)
let parse_analyses (input:string): analysis list = 
    let example = 
    {
        lattice = {
            set = [("constant", "is a constant")]; 
            ordering = (fun s1 s2 -> 0); 
        }; 
        transfer_functions = []
    } in 

    [example]

(* TODO: Define reading program from given .imp/.c file *)
let parse_program path : string = ""

let analyze (analysis:analysis) (program:string) : string =
    let graph = generate_graph analysis in
    let ast = generate_AST program in 
    let found_fixpoint = find_fixpoint graph ast analysis in
    let transformed = apply_fixpoint found_fixpoint ast in
    let pretty = pretty_print transformed in 
    pretty

let () =
    let lattices = Array.get Sys.argv 0 |> parse_analyses in 
    let program = Array.get Sys.argv 3 |> parse_program in
    let out : string = List.fold_left (fun acc lattice -> analyze lattice acc) program lattices in
    printf "%s" out