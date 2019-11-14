open Printf
open Analysis

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
let parse_analyses (input:string): Analysis.analysis list = 
    let analyses = String.split_on_char ':' input in 
    let module Analyzer =
        (val match Linkage.load "example.cma" with
         | Ok (Analysis.AnalysisPlugin m) -> m
         | e -> Linkage.raise_error e) in
    [analyzer]

(* TODO: Define reading program from given .imp/.c file *)
let parse_program path : string = ""

let analyze (analysis:analysis) (program:string) : string =
    let graph = generate_graph analysis in
    let ast = generate_AST program in 
    let fixpoint = find_fixpoint graph ast analysis in
    let transformed = apply_fixpoint fixpoint ast in
    let pretty = pretty_print transformed in 
    pretty

let () =
    let analyses = Array.get Sys.argv 0 |> parse_analyses in 
    let program = Array.get Sys.argv 3 |> parse_program in
    let out : string = List.fold_left (fun acc analysis -> analyze analysis acc) program analyses in
    printf "%s" out