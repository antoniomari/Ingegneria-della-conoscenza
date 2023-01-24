p(A, B) :- c(A, B).
c(a, b).
c(a, g).
c(c, d).
c(e, f).
num_of_c(C, N) :- findall(S, p(C, S), L), length(L,N).
