open Printf

let bin_to_hex h =
  match h with
  | '0' -> [0;0;0;0]
  | '1' -> [0;0;0;1]
  | '2' -> [0;0;1;0]
  | '3' -> [0;0;1;1]
  | '4' -> [0;1;0;0]
  | '5' -> [0;1;0;1]
  | '6' -> [0;1;1;0]
  | '7' -> [0;1;1;1]
  | '8' -> [1;0;0;0]
  | '9' -> [1;0;0;1]
  | 'A' -> [1;0;1;0]
  | 'B' -> [1;0;1;1]
  | 'C' -> [1;1;0;0]
  | 'D' -> [1;1;0;1]
  | 'E' -> [1;1;1;0]
  | 'F' -> [1;1;1;1]
  | _   -> [];;

let get_input filename =
  let file = open_in filename in
  let hex = input_line file in 
    close_in file;
  let rec parse_file h = 
    match (String.length h) with
    | 0 -> []
    | _ -> bin_to_hex (String.get h 0) :: parse_file (String.sub h 1 ((String.length h) - 1)) in
  List.flatten (parse_file hex);;

(****************************************************************************)
(* Part 1 *)

let pow_2 n =
  let rec helper n p =
    match n with
    | 0 -> p
    | _ -> helper (n - 1) 2 * p in
  helper n 1;;

let decode bits length = 
  let rec combine b len pow2 total = 
    if len == length then
      total
    else
      combine (List.tl b) (len + 1) (pow2 / 2) (total + pow2 * (List.hd b)) in
  combine bits 0 (pow_2 (length - 1)) 0;;

let rec eat_numbers bits = 
  match bits with
  | 1::_::_::_::_::t -> eat_numbers t
  | 0::_::_::_::_::t -> t
  | _ -> bits;;

let rec chop_n bits n =
  match n with
  | 0 -> bits
  | _ -> chop_n (List.tl bits) (n - 1);;

let rec max_bit bits =
  match bits with
  | []   -> 0
  | 1::_ -> 1
  | _::t -> max_bit t;;

let version_sum bits =
  let rec helper bits sum =
    if (max_bit bits) == 1 then
      let version = decode bits 3 in
      let bits_no_version = chop_n bits 3 in
      let type_id = decode bits_no_version 3 in
      let param_bits = chop_n bits_no_version 3 in
      if type_id == 4 then
        helper (eat_numbers param_bits) (sum + version)
      else
        let length_type_id = List.hd param_bits in
        if length_type_id == 1 then
          helper (chop_n param_bits 12) (sum + version)
        else
          helper (chop_n param_bits 16) (sum + version)
    else
      sum in
  helper bits 0;;

(****************************************************************************)
(* Part 2 *)

(* type expr = 
  | Expression of {
      packet : op; 
      length : int; 
      length_type : int; 
      expression : expr
    }
  | Literal of {value : int} *)

type op =
  | Sum
  | Product
  | Minimum
  | Maximum
  | GreaterThan
  | LessThan
  | EqualTo

type len_type =
  | BitLength
  | SubPacketCount

type token =
  | Operation of {
      op_type : op;
      length_type : len_type;
      length : int;
  }
  | Literal of {
      value : int;
  }

exception LexError of string

let num_to_len_type id = 
  match id with
  | 0 -> BitLength
  | 1 -> SubPacketCount
  | _ -> raise (LexError "Invalid length")

let num_to_op type_id =
  match type_id with
  | 0 -> Sum
  | 1 -> Product
  | 2 -> Minimum
  | 3 -> Maximum
  | 5 -> GreaterThan
  | 6 -> LessThan
  | 7 -> EqualTo
  | _ -> raise (LexError "Invalid operator")

let literal bits = 
  let rec combine bits =
    match bits with
    | 1::a::b::c::d::t -> List.append [a;b;c;d] (combine t)
    | 0::a::b::c::d::t -> [a;b;c;d]
    | _ -> [] in
  let num = combine bits in
  decode num (List.length num);;

(* let parse_bits program length =
  let rec helper bits ip = 
    if ip < length then  *)

let parse program =
  let rec helper bits =
    if (max_bit bits) == 1 then
      let no_version = chop_n bits 3 in
      let type_id = decode no_version 3 in
      let params = chop_n no_version 3 in
      if type_id == 4 then
        let trimmed = eat_numbers params in
        Literal {value = literal params} :: helper trimmed
      else
        let length_id = List.hd params in
        if length_id == 1 then
          Operation {op_type = num_to_op type_id; length_type = num_to_len_type (decode params 1); 
            length = decode (List.tl params) 11} :: helper (chop_n params 12)
        else
          Operation {op_type = num_to_op type_id; length_type = num_to_len_type (decode params 1); 
            length = decode (List.tl params) 15} :: helper (chop_n params 16)
    else
      [] in
  helper program;;

(* let version_sum bits =
  let rec helper bits sum =
    if (max_bit bits) == 1 then
      let version = decode bits 3 in
      let bits_no_version = chop_n bits 3 in
      let type_id = decode bits_no_version 3 in
      let param_bits = chop_n bits_no_version 3 in
      if type_id == 4 then
        helper (eat_numbers param_bits) (sum + version)
      else
        let length_type_id = List.hd param_bits in
        if length_type_id == 1 then
          helper (chop_n param_bits 12) (sum + version)
        else
          helper (chop_n param_bits 16) (sum + version)
    else
      sum in
  helper bits 0;; *)


(* let rec lex bits =
  if (max_bit bits) == 1 then
    let expr = chop_n bits 3 in
    let type_id = decode expr 3 in
    let params = chop_n expr 3 in
    let length_type_id = List.hd params in
    let chop_len = if length_type_id == 1 then 11 else 15 in
    let new_len = decode (List.tl params) chop_len in
    match type_id with
    | 0 -> Expression {packet = Sum; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 1 -> Expression {packet = Product; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 2 -> Expression {packet = Minimum; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 3 -> Expression {packet = Maximum; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 5 -> Expression {packet = GreaterThan; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 6 -> Expression {packet = LessThan; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | 7 -> Expression {packet = EqualTo; length = new_len; length_type = length_type_id; expression = lex (chop_n params (chop_len+1))}
    | _ -> Literal {value = literal params}
  else
    Literal {value = 0};; *)

let () =
  let bits = get_input "inputs/test.in" in
  printf "%d\n" (List.length (bits));;