import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def initLink(sheetName="Feuille expert"):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'json_files/client_secrets.json', scope)
    client = gspread.authorize(credentials)
    ws = client.open(sheetName).sheet1
    return ws


def readValues(ws):
    # il faut donner le nombre de ligne et le nombre de colonne de la feuille gs
    lines = ws.row_count
    eleves_to_savoirs = {}
    ALLITEMS = list(filter(None, ws.row_values(1)))
    ALLITEMS = [e.split(":")[0].strip() if len(
        e.split(":")) > 1 else e for e in ALLITEMS]
    for i in range(2, lines + 1):
        values_list = ws.row_values(i)
        M = []
        id_number, id, *M = values_list
        if M != []:
            eleves_to_savoirs[id.strip().lower()] = list(map(int, M))
    return eleves_to_savoirs, ALLITEMS


ws = initLink()
eleves_to_savoirs, ALLITEMS = readValues(ws)
# print(eleves_to_savoirs)
# print(ALLITEMS)