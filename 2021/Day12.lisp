; Reads lines from a file up to line number "line-count"
(defun read-file (file line-count &optional lst)
    (if (> line-count 0) 
        (read-file file (- line-count 1) (append (list (read-line file)) lst)) 
        lst))

; splits a string with two words separated by a "-" into two substrings
(defun split (str &optional (idx 0))
    (if (string= (aref str idx) "-") 
        (list (subseq str 0 idx) (subseq str (+ 1 idx)))
        (split str (+ 1 idx))))

; Split into pairs
(defun split-all (lst)
    (if (null lst) 
        '() 
        (append (split-all (cdr lst)) (list (split (car lst))))))


; Count unique paths from curr-node to the end
(defun count-paths (curr-node pairs search-pairs &optional visited (num-unique 0))
    (cond
        ((string= curr-node "end") 1)
        ((member (string-downcase curr-node) visited :test #'string=) 0)
        (t (+ num-unique (leave curr-node pairs pairs visited num-unique)))))

; Leave a node counting the paths from it to the end visiting a small cave at most once
(defun leave (curr-node pairs search-pairs visited num-unique)
    (cond
        ((null search-pairs) num-unique)
        ((string= curr-node (caar search-pairs)) 
            (+ (leave curr-node pairs (cdr search-pairs) visited num-unique) 
                (count-paths (cadar search-pairs) pairs pairs (append (list curr-node) visited) num-unique)))
        ((string= curr-node (cadar search-pairs)) 
            (+ (leave curr-node pairs (cdr search-pairs) visited num-unique) 
                (count-paths (caar search-pairs) pairs pairs (append (list curr-node) visited) num-unique)))
        (t (leave curr-node pairs (cdr search-pairs) visited num-unique))))

; Count paths while able to visit a single small cave twice
(defun count-paths-2 (curr-node pairs search-pairs &optional visited (num-unique 0))
    (cond
        ((string= curr-node "end") 1)
        ((and (string= curr-node "start") 
            (member "start" visited :test #'string=)) 0)
        ((= 1 (count (string-downcase curr-node) visited :test #'string=)) 
            (+ num-unique (leave curr-node pairs pairs visited num-unique)))
        (t (+ num-unique (leave-2 curr-node pairs pairs visited num-unique)))))

; Leave a node counting the paths from it to the end while able to visit a single small cave twice, and other small caves at most once
(defun leave-2 (curr-node pairs search-pairs visited num-unique)
    (cond
        ((null search-pairs) num-unique)
        ((string= curr-node (caar search-pairs)) (+ (leave-2 curr-node pairs (cdr search-pairs) visited num-unique) (count-paths-2 (cadar search-pairs) pairs pairs (append (list curr-node) visited) num-unique)))
        ((string= curr-node (cadar search-pairs)) (+ (leave-2 curr-node pairs (cdr search-pairs) visited num-unique) (count-paths-2 (caar search-pairs) pairs pairs (append (list curr-node) visited) num-unique)))
        (t (leave-2 curr-node pairs (cdr search-pairs) visited num-unique))))

(print (count-paths "start" (split-all (read-file (open "inputs/Day12.in") 22)) (split-all (read-file (open "inputs/Day12.in") 22))))
(print (count-paths-2 "start" (split-all (read-file (open "inputs/Day12.in") 22)) (split-all (read-file (open "inputs/Day12.in") 22))))
