#! /usr/bin/env python3
import hw_1_1

L = "ACDQDCGFDERAE"
S = "EECDACWERGARF"
#L = ("ACCGFDERAE", "ACDCGFERAE")
#S = ("ECDACEGARF", "ECDACERGAF", "EECDACGARF", "EECDACRGAF")

def get_LIST(L, S):
    """
    Function that computes M and return a LIST of the characters must be removed from L 
    """

    occurence_L, occurence_S = (hw_1_1.get_hist(L), hw_1_1.get_hist(S))
    chars = set(occurence_L.keys()).union(set(occurence_S.keys()))
    M = {c: min([occurence_L.get(c, 0), occurence_S.get(c, 0)]) for c in chars}
    LIST = []
    for c in set(L):
        n_remove = occurence_L.get(c, 0) - M[c]
        if n_remove > 0:
            LIST.extend([c] * n_remove)
    return (M, LIST)

    
def min_dist_rem(L, S):
    """
    Functions to solve the MinDistRem problem and return a tuple of the 2 resulting strings.
    """
    
    if len(L) < len(S):
        L, S = (S, L)
    L = remove_from_L(L, S)
    
    if len(L) < len(S):
        L, S = (S, L)
        L = remove_from_L(L, S)

    return (L, S)

def remove_from_L(L, S):
    """
    Functions representing a pass of step 2 to 10
    """
    M, LIST = get_LIST(L, S)

    L_list, S_list = (list(L), list(S))
    p, q, q_prime = (0, -1, -1)
    while p < len(S) and len(LIST) > 0:
        X = S[p]
        try:
            q_prime = L_list.index(X, p)
        except ValueError:
            pass
        else:
            for idx in range(q + 1, q_prime):
                if L_list[idx] in LIST:
                    LIST.remove(L_list[idx])
                    L_list[idx] = None
            q = q_prime
        finally:
            p += 1
    if len(LIST) > 0:
        for idx in range(len(L_list), -1, -1):
            if L_list[idx] in LIST:
                LIST.remove(L_list[idx])
                L_list[idx] = None

    return ''.join([c for c in L_list if c is not None]) 

            

if __name__ == "__main__":
    for (L, S) in [("ABCCBCD", "ACBAD"), ("ACDQDCGFDERAE", "EECDACWERGARF")]:
        print("L = {L}\nS = {S}".format(**locals()))
        print("(S1, S2) = {0}".format(min_dist_rem(L, S)))
