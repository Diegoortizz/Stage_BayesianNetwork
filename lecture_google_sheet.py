import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


""" 
Ce script permet 
- de parser la feuille de question google sheet et de générer un JSON qui contient les différentes pour ensuite donner
ce json à la base de donnée de question endb.
- récupérer les différentes questions / savoirs associés dans la feuille google sheet de question (https://docs.google.com/spreadsheets/d/1OP4lLVf3_oUxLsasizt3YPP34-qkQUL_uNtcnuUE_eI/edit#gid=0)
- construire les structures de données necessaires à la création du réseau de neuronne au format GeNIe.
"""

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'json_files/client_secrets.json', scope)
client = gspread.authorize(credentials)

ws = client.open('Feuille de questions').sheet1


questions = []

for i in range(2, ws.row_count):
    if ws.row_values(i) == []:
        break
    questions.append(ws.row_values(i))

Qjs = []
dico_idquestions_to_idsavoir = {}
dico_idquestions_to_idreponse = {}

for question in questions:
    id, label, r1, r2, r3, r4, reponse, multiple, codes = question
    json_obj = {}
    json_obj["_id"] = id
    json_obj["lib"] = label

    temprep = []

    r = [r1, r2, r3, r4]

    for i in range(len(r)):
        temprep.append({"lib": r[i]})

    json_obj["answers"] = temprep

    if multiple.upper().strip() == "NON":
        json_obj["multiple"] = False
    else:
        json_obj["multiple"] = True

    json_obj["codes"] = [e.strip() for e in codes.split(",")]

    json_obj["alreadyIn"] = False

    json_obj["correct"] = int(reponse) - 1

    Qjs.append(json_obj)

    dico_idquestions_to_idsavoir[id] = [e.strip() for e in codes.split(",")]
    dico_idquestions_to_idreponse[id] = reponse


def writedbjson(questions):
    # création du json pour le server nodejs au format nedb
    with open('../questions_diego.json', 'w', encoding="utf-8") as f:
        json.dump(Qjs, f, ensure_ascii=False)


def build_dico_idsavoirs_to_idquestions(idquestion_to_idsavoirs):
    idsavoirs_to_idquestion = dict()

    for key in idquestion_to_idsavoirs:
        fils = idquestion_to_idsavoirs[key]
        for e in fils:
            try:
                idsavoirs_to_idquestion[e].append(key)
            except KeyError:
                idsavoirs_to_idquestion[e] = [key]
    return idsavoirs_to_idquestion

# BASE DE DONNEE
# print("start build db")
# writedbjson(Qjs)
# print("end build db")

# STRUCTURE DE DONNEE
# print(dico_idquestions_to_idsavoir)
# print(dico_idquestions_to_idreponse)
