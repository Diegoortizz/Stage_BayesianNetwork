import re

VAR_SAVOIRS = "SAVOIRS"
VAR_SF = "SAVOIR-FAIRE"
VAR_COMPETENCES = "COMPETENCES"
VAR_SPLITER_SF = '(SF[0-9]{1,2}) | \\| '
VAR_SPLITER_COMPETENCE = '(C[0-9]{1,2}) | \\| '


def recuperer_txt(fic):
    """ Récupère toutes les lignes du fichier donné en paramètre en retirant les lignes vides
    Arguments:
        fic : Fichier texte

    Returns:
        lignes -- Listes de string aka toutes les lignes du fichier
    """

    lignes = []
    with open(fic, "r", encoding="utf-8") as f:
        data = f.readlines()
        for ligne in data:
            if ligne != '\n':
                lignes.append(ligne.strip())
    return lignes


def get_packets(data):
    """ Récupère les différentes paquets du fichier savoirs, dans notre cas il y a 3 paquets : les savoirs (VAR_SAVOIRS), les compétences (VAR_COMPETENCES) et les savoir-faire (VAR_SF)

    Arguments:
        data : Liste de ligne (voir le retour de la fonction recuperer_txt(fic))

    Returns:
        S_SF_C : Liste qui contient autant d'élements de paquets (3 dans notre cas)
    """

    L = []
    keywords = [VAR_SAVOIRS, VAR_COMPETENCES, VAR_SF]
    for i in range(len(data)):
        if data[i] in keywords:
            L.append(i)

    S_SF_C = []
    for i in range(len(L) - 1):
        S_SF_C.append(data[L[i]: L[i+1]])
    S_SF_C.append(data[L[-1]:])
    return S_SF_C


def split_savoirs(ligne):
    """ A partir d'une ligne donée en paramètre, extrait et décompose le savoir et la compétence associée

    Arguments:
        ligne : un des lignes du paquet SAVOIRS

    Returns:
        code, savoir : deux strings, éponyme
    """
    return list(filter(None, re.split('([C|M][0-9]{1,2}_[0-9])', ligne)))


def critere_tri(e):
    """ Fonction qui va permettre de définir notre propre ordre de tri :

    CHAPITRE > PARAGRAPHE > CONNAISSANCE > METHODE

    """

    g, d = e.split("_")
    second = g[0]  # lettre
    third = g[1:]  # après le _
    first = d  # entre la lettre et le _
    return int(first), second, int(third)


def get_savoirs_codes(lignes):
    """ Récupère la liste de tout les savoirs et de tous les codes des savoirs
    Arguments:
        ligne : un des lignes du paquet SAVOIRS

    Returns:
        savoirs, codes : 2 listes
    """

    savoirs = []
    codes = set()
    for ligne in lignes:
        code, savoir = split_savoirs(ligne)
        if savoir != '':
            savoirs.append(savoir)
        if code != '':
            codes.add(code)
    return sorted(list(codes), key=critere_tri), savoirs[1:]


def build_dico_savoirs_codes(lignes):
    """ Crée un dictionnaire K,V de la forme suivante : K = code du savoir, V = savoir associé

    Arguments:
        ligne : un des lignes du paquet SAVOIRS


    Returns:
        Dictionnaire K, V
    """

    code_to_question = dict()
    for ligne in lignes:
        code, label = split_savoirs(ligne)
        code_to_question[code] = label
    return code_to_question


def spliteur(e, delimiteur):
    # id, label, savoirs associés
    return list(filter(None, re.split(delimiteur, e)))


def build_dico_sf(lignes, delimiteur):
    sf_label = dict()  # K = id, V = label
    sf_codes = dict()  # K = id, V = codes
    for ligne in lignes:
        if delimiteur == VAR_SPLITER_COMPETENCE:
            code, label, savoirs = spliteur(ligne, delimiteur)
            sf_label[code] = label
            sf_codes[code] = [e.strip() for e in savoirs.split(",")]
        else:
            code, label = spliteur(ligne, delimiteur)
            sf_label[code] = label

    if delimiteur == VAR_SPLITER_COMPETENCE:
        return sf_label, sf_codes
    return sf_label


data = recuperer_txt("text_input/savoirs.txt")
SAVOIRS_paquet, SF_paquet, COMPETENCES_paquet = get_packets(data)
codes_listes, savoirs_liste = get_savoirs_codes(SAVOIRS_paquet[1:])
dico_compID_to_sflabel, dico_compID_to_savoirID = build_dico_sf(
    COMPETENCES_paquet[1:], VAR_SPLITER_COMPETENCE)
