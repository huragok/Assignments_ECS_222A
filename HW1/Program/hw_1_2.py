#! /usr/bin/env python3
import hw_1_1
import itertools

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

def min_dist_rem_BF(L, S):
    """
    Brute force to solve the minDistRem problem
    """
    S1s, S2s = get_all_S12(L, S)
    D = {(S1, S2): hw_1_1.get_kendall_tau_dist(S1, S2)[0] for S1 in S1s for S2 in S2s}
    #print(D)
    D_min = min(D.values())
    R = [key for key, value in D.items() if value == D_min]
    return R

def get_all_S12(L, S):
    """
    Return a tuple of all possible S1 and a tuple of all possible S2
    """
    
    chars_to_remove_L, chars_to_remove_S = get_char_to_remove(L, S)
    
    wheres_to_remove_L = itertools.product(*(itertools.combinations(chars_to_remove_L[c][1], chars_to_remove_L[c][0]) for c in chars_to_remove_L.keys()))
    S1s = set()
    for where_to_remove_L in wheres_to_remove_L:
        idxs_to_remove = [idx for idxs in where_to_remove_L for idx in idxs]
        S1s.add("".join([L[idx] for idx in range(len(L)) if idx not in idxs_to_remove]))

    wheres_to_remove_S = itertools.product(*(itertools.combinations(chars_to_remove_S[c][1], chars_to_remove_S[c][0]) for c in chars_to_remove_S.keys()))
    S2s = set()
    for where_to_remove_S in wheres_to_remove_S:
        idxs_to_remove = [idx for idxs in where_to_remove_S for idx in idxs]
        S2s.add("".join([S[idx] for idx in range(len(S)) if idx not in idxs_to_remove]))

    return S1s, S2s 
    

def get_char_to_remove(L, S):
    """
    Get 2 dict of characters, numbers to remove and possible possitions to remove for L and S respectively    
    """
    
    occurence_L, occurence_S = (hw_1_1.get_hist(L), hw_1_1.get_hist(S))
    chars = set(occurence_L.keys()).union(set(occurence_S.keys()))
    M = {c: min([occurence_L.get(c, 0), occurence_S.get(c, 0)]) for c in chars}
    
    chars_to_remove_L = dict()
    for c in set(L):
        n_remove = occurence_L.get(c, 0) - M[c]
        if n_remove > 0:
            chars_to_remove_L[c] = (n_remove, find(L, c))
    
    chars_to_remove_S = dict()
    for c in set(S):
        n_remove = occurence_S.get(c, 0) - M[c]
        if n_remove > 0:
            chars_to_remove_S[c] = (n_remove, find(S, c))
            
    return (chars_to_remove_L, chars_to_remove_S)
        
def find(s, c):
    """
    Generalization of the index function: find all indices of occurences of c in string s
    """
    return [i for i, ltr in enumerate(s) if ltr == c]

if __name__ == "__main__":
    for (L, S) in [("ABCCBCD", "ACBAD"), ("ACDQDCGFDERAE", "EECDACWERGARF")]:
        print("L = {L}\nS = {S}".format(**locals()))
        print("(S1, S2) = {0}".format(min_dist_rem(L, S)))

    L = "ACDQDCGFDERAE"
    S = "EECDACWERGARF"

    R_BF = min_dist_rem_BF(L, S)
    R = min_dist_rem(L, S)

    print("By the proposed algorithm: (S1, S2) = {0}, D = {1}".format(R, hw_1_1.get_kendall_tau_dist(*R)[0]))
    print("By exhaustive search: (S1, S2) = {0}, D = {1}".format(R_BF, hw_1_1.get_kendall_tau_dist(*(R_BF[0]))[0]))
    
