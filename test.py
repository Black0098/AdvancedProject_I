ez_squarex = [-5, -5, 5, 5, -5]
ez_squarey = [-5, 5, 5, -5, -5]


def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts

for i in range(5):
    ez_squarex[i] = mmtocounts(ez_squarex[i])

print(ez_squarex)