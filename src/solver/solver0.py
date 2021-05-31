def separation_chiffre(n, m):
    res = []
    for i in range(1, n):
        if i > res[m-1]:
            res[m] = i
            rest = n-i
            if rest == 0 and m > 1:
                for j in range(1, m):
                    if res[m] < 10:
                        print(res[j])
                print("\n")
            else:
                separation_chiffre(rest, m+1)
            res[m] = 0


def test(n):
    while 0 < n < 45:
        separation_chiffre(n, 1)


test(5)





