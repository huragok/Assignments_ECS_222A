#! /usr/bin/env python3
import sys
INF = sys.maxsize

S1 = "CBADA"
S2 = "ABDCA"

def get_hist(S):
    """
    Function used to count the number of appearances of each character in the string S, return a dictionary with characters as keys and count as values.
    """
    hist = dict();
    for c in S:
        hist[c] = hist.get(c, 0) + 1
    return hist

class UnequalOccurence(Exception):
    pass

def count_inversion(Q, start, end):
    """
    Basically merge sort plus counting inversion across the left and the right segment.
    """
    if end - start > 1:
        mid = int((start + end) / 2)
        countInvLeft = count_inversion(Q, start, mid)
        countInvRight = count_inversion(Q, mid, end)
        QLeft, QRight = (Q[start : mid], Q[mid : end])
        idxLeft, idxRight = (0, 0)
        countInvCross = 0
        QLeft, QRight = (QLeft + [INF], QRight + [INF])
        for idx in range(start, end):
            if QLeft[idxLeft] < QRight[idxRight]:
                Q[idx] = QLeft[idxLeft]
                idxLeft += 1
                countInvCross += idxRight
            else:
                Q[idx] = QRight[idxRight]
                idxRight += 1
        return countInvLeft + countInvRight + countInvCross
    else:
        return 0

def get_kendall_tau_dist(str1, str2):
    """
    get kendall tau distance between str1 and str2
    """
    h = get_hist(str1)
    n = len(str1)
    if h != get_hist(str2):
        raise UnequalOccurence("Not every character has the same number of occurence in both strings!")
    
    # Construct index sequence Q
    tau2_dict = dict()
    for idx, c in enumerate(str2):
        tau2_dict.setdefault(c, list()).append(idx)
    Q = [0] * n
    for idx, c in enumerate(str1):
        Q[idx] = tau2_dict[c].pop(0)
    Q0 = Q[:]
    #print(Q)

    # Count the inversion in Q
    return (count_inversion(Q, 0, len(Q)), Q0)

def transform_by_transpose(str1, Q):
    """
    Transform str1 to str2 according to index sequence Q computed by get_kendall_tau_dist() function
    """
    n = len(str1)
    assert n == len(Q), "str1 and Q must have the same length!"
    
    count_transpose = 0
    print("{0}: {1}".format(count_transpose, tuple(str1)))
    str_zipped = list(zip(list(str1), Q))
    for i in range(n - 1, -1, -1):
        for j in range(0, i):
            if str_zipped[j][1]  > str_zipped[j + 1][1]:
                str_zipped[j + 1], str_zipped[j] = (str_zipped[j], str_zipped[j + 1])
                count_transpose += 1 
                print("{0}: {1}".format(count_transpose, list(zip(*str_zipped))[0]))

    str_sorted = list(zip(str_zipped))
    return str(str_sorted[0])

if __name__ == "__main__":
    print("S1 is: {0}".format(S1))
    print("S2 is: {0}".format(S2))
    (D, Q) = get_kendall_tau_dist(S1, S2)
    print("Q is: {0}".format(Q))
    print("D(S1, S2) is: {0}".format(D))
    transform_by_transpose(S1, Q)
