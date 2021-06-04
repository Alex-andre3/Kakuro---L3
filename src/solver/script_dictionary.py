def creer_dictionnaire():
    d = {}

    for i in range(1, 2**9):
        addition = []
        nb_de_chiffres = 0
        total_chiffres = 0
        chiffre_i = 1
        for c in bin(i)[:1:-1]:
            if c == '1':
                addition.append(chiffre_i)
                nb_de_chiffres += 1
                total_chiffres += chiffre_i
            chiffre_i += 1
        if nb_de_chiffres >= 1:
            if total_chiffres in d:
                if nb_de_chiffres in d[total_chiffres]:
                    d[total_chiffres][nb_de_chiffres].append(addition)
                else:
                    d[total_chiffres][nb_de_chiffres] = [addition]
            else:
                d[total_chiffres] = {nb_de_chiffres: [addition]}

    return d


print(creer_dictionnaire()[5][1])