from readSheetExpert import eleves_to_savoirs, ALLITEMS

SAVOIRS_AND_COMPETENCES = ALLITEMS
QUESTIONS = []
SAVOIRS = []

for e in SAVOIRS_AND_COMPETENCES:
    if e.startswith("q"):
        QUESTIONS.append(e)
    else:
        SAVOIRS.append(e)

sizeS = len(SAVOIRS)

with open('genie_bnn/learning_file_last.txt', 'w'):
    pass

with open("genie_bnn/learning_file_last.txt", "w") as f:
    f.write(" ".join(ALLITEMS) + "\n")
    for eleve in list(eleves_to_savoirs.values()):
        eleveS = eleve[0:sizeS]
        eleveQ = eleve[sizeS:]

        for i in range(len(eleveS)):
            if eleveS[i] == 1:
                f.write(SAVOIRS[i] + "_oui ")
            else:
                f.write(SAVOIRS[i] + "_non ")

        for i in range(len(eleveQ) - 1):
            f.write("q" + str(i) + "_r" + str(eleveQ[i]) + " ")
        f.write("q" + str(len(eleveQ) - 1) +
                "_r" + str(eleveQ[len(eleveQ) - 1]))
        f.write("\n")
