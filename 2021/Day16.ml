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
  | 'E' -> [1;1;1;1]
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

let decode bits start length =
  let rec combine idx pow2 total = 
    if idx < start then total else (combine (idx - 1) (pow2 * 2) (total + pow2 * (List.nth bits idx))) in
  combine (start + length - 1) 1 0;;

let rec eat_numbers bits = 
  match bits with
  | 1::_::_::_::_::t -> eat_numbers t
  | _ -> bits;;

let version_sum bits =
    let rec helper ip sum =
      let version = decode bits = 

let () =
  let bits = get_input "inputs/Day16.in" in
    print_newline (print_int (version_sum bits));;
