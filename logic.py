def get_total_similarity(a, b):
    key = "name"
    compare1 = "skill"
    compare2 = "pref"
    score = "score"

    for i in range(len(b)):
        cnt = 0
        for v in a[compare1]:
            if v in b[i][compare1]:
                cnt += 1
        b[i][score] = cnt / len(a[compare1]) / 2

        cnt = 0
        for j in range(len(a[compare2])):
            if a[compare2][j] in b[i][compare2]:
                cnt += abs(j - b[i][compare2].index(a[compare2][j]))
            else:
                cnt += len(a[compare2])
        b[i][score] += (1 - cnt / (len(a[compare2]) * len(a[compare2]))) / 2

    return sorted(b, key=lambda x: x[score], reverse=True)
