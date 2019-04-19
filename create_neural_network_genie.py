from lecture_feuille_competence import dico_compID_to_savoirID
from lecture_google_sheet import dico_idquestions_to_idsavoir
from lxml import etree
import xml.etree.ElementTree as ET


COMPETENCES_A_EVALUER = ['C7']


def remove_savoirs_unused(dico_compID_to_savoirID, dico_idquestions_to_idsavoir):
    """ Il se peut que les compétences décrits dans la feuille de compétence et les compétences évalués par les questions ne soient pas toutes présentes. 
    Ainsi si cette fonction va retirer les compétences (sf, connaissances, compétences, méthodes) qui ne sont pas évalués dans les questions.

    Arguments:
        dico_compID_to_savoirID {[type]} -- [description]
        dico_idquestions_to_idsavoir {[type]} -- [description]

    Returns:
       Le nouveau dictionnaire de compétence où on a retirer les savoirs non évalués
    """

    # set des compétences évalués dans la feuille des questions
    s = set([item for items in dico_idquestions_to_idsavoir.values()
             for item in items])
    d = {}
    for k, v in dico_compID_to_savoirID.items():
        savoirs = v
        # on ne garde que les compétences présente dans les comps de la feuille de question
        d[k] = [savoir for savoir in savoirs if savoir in s]
    return d


def remove_competences_unused(dico_compID_to_savoirID, dico_idquestions_to_idsavoir):
    """ Pareil que si desssus, sauf que cette fois on retire les compétences et non pas les savoirs
    Arguments:
        dico_compID_to_savoirID {[type]} -- [description]
        dico_idquestions_to_idsavoir {[type]} -- [description]

    Returns:
    Le nouveau dictionnaire de compétence où on a retiré les compétences non évalués
    """

    # set des compétences évalués dans la feuille des questions
    s = set([item for items in dico_idquestions_to_idsavoir.values()
             for item in items])
    d = {}
    for k, v in dico_compID_to_savoirID.items():
        savoirs = v
        # on ne garde que les compétences présente dans les comps de la feuille de question
        d[k] = [savoir for savoir in savoirs if savoir in s]
    return d


def create_node_question(num, number_of_states=4):

    p = (str(1 / number_of_states) + " ") * number_of_states

    r = ET.Element('cpt', {"id": num})
    states = []

    for e in range(number_of_states):
        cur = ET.SubElement(r, 'state', {"id": num + "_r" + str(e)})
        states.append(cur)

    proba = ET.SubElement(r, 'probabilities')
    proba.text = p
    # ET.dump(r)
    return r


def create_node_competence(num):

    r = ET.Element('cpt', {"id": num})
    states = []

    cur = ET.SubElement(r, 'state', {"id": num + "_oui"})
    states.append(cur)
    cur = ET.SubElement(r, 'state', {"id": num + "_non"})
    states.append(cur)

    proba = ET.SubElement(r, 'probabilities')
    proba.text = "0.5 0.5"
    # ET.dump(r)
    return r


def build_dict_parents_savoirs_sf(dico_compID_to_savoirID, dico_idquestions_to_idsavoir):
    # Key = SAVOIRS / METHODE (C1_1 ou M2_1) VALUE = (a,b) avec a = nb de questions associés, b nombre de compétences associés
    dict_parents_savoirs_sf = {}
    z = {**dico_compID_to_savoirID, **dico_idquestions_to_idsavoir}
    for key, value in z.items():
        for e in value:
            try:
                dict_parents_savoirs_sf[e].append(key)
            except KeyError:
                dict_parents_savoirs_sf[e] = [key]
    return dict_parents_savoirs_sf


def create_node_savoirs(num, parents):
    nb_questions = len(
        [x for x in parents if x.startswith(tuple(["test", "q"]))])
    nb_comp = len([x for x in parents if x.startswith("C")])

    n = (4**(nb_questions) * 2**(nb_comp)) * 2
    p = (str("0.5") + " ") * n

    r = ET.Element('cpt', {"id": num})

    cur = ET.SubElement(r, 'state', {"id": num + "_oui"})
    cur = ET.SubElement(r, 'state', {"id": num + "_non"})

    family = ET.SubElement(r, 'parents')
    family.text = " ".join(parents)

    proba = ET.SubElement(r, 'probabilities')
    proba.text = p

    # ET.dump(r)
    return r


def create_node_question_css(num, pos):

    r = ET.Element('node', {"id": num})

    name = ET.SubElement(r, 'name')
    name.text = num
    if "_" in num or "SF" in num:
        interior = ET.SubElement(r, 'interior', {"color": "99cc00"})
    elif ("q" in num):
        interior = ET.SubElement(r, 'interior', {"color": "ff9900"})
    else:
        interior = ET.SubElement(r, 'interior', {"color": "99ccff"})
    outline = ET.SubElement(r, 'outline', {"color": "000080"})
    font = ET.SubElement(
        r, 'font', {"color": "000000", "name": "Arial", "size": "8"})

    position = ET.SubElement(r, 'position')
    position.text = pos
    # ET.dump(r)
    return r


def writeFile(dico_compID_to_savoirID, dico_idquestions_to_idsavoir, dict_parents_cpt, fic="genie_bnn/temoin.xdsl"):
    # Crée le fichier xdsl pour representer le BNN avec GeNIe
    lines = ['<?xml version="1.0" encoding="ISO-8859-1"?>', '<!-- This network was created in GeNIe Academic, which can be used for educational and research purposes only -->', '<smile version="1.0" id="Network2" numsamples="10000" discsamples="10000">',
             '<nodes>', '</nodes>', '<extensions>', '<genie version="1.0" app="GeNIe 2.3.3828.0 ACADEMIC" name="Network2" faultnameformat="nodestate">', '</genie>', '</extensions>', '</smile>']

    Lquestions = list(dico_idquestions_to_idsavoir.keys())
    Lcompetences = list(dico_compID_to_savoirID.keys())
    flatten = set()
    for e in dico_compID_to_savoirID.values():
        flatten.update(e)
    Lsavoirs = list(flatten)
    Ljoinnoeuds = Lquestions + Lcompetences + Lsavoirs

    Lquestions_noeuds = []
    Lcompetences_noeuds = []
    Lsavoirs_noeuds = []
    Lnoeuds_pos = []

    for question in Lquestions:
        newnode = create_node_question(question)
        xmlstr = ET.tostring(newnode, encoding='utf-8', method='xml')
        Lquestions_noeuds.append(xmlstr.decode("utf-8"))

    for competence in Lcompetences:
        newnode = create_node_competence(competence)
        xmlstr = ET.tostring(newnode, encoding='utf-8', method='xml')
        Lcompetences_noeuds.append(xmlstr.decode("utf-8"))

    for savoir in Lsavoirs:
        newnode = create_node_savoirs(savoir, dict_parents_cpt[savoir])
        xmlstr = ET.tostring(newnode, encoding='utf-8', method='xml')
        Lsavoirs_noeuds.append(xmlstr.decode("utf-8"))

    pos = [65, 61, 126, 112]
    for i in range(len(Ljoinnoeuds)):
        pos[0] += 10
        pos[1] += 10
        pos[2] += 10
        pos[3] += 10
        newnode2 = create_node_question_css(
            Ljoinnoeuds[i], " ".join(list(map(str, pos))))
        xmlstr2 = ET.tostring(newnode2, encoding='utf-8', method='xml')
        Lnoeuds_pos.append(xmlstr2.decode("utf-8"))

    Lnoeuds = Lquestions_noeuds + Lcompetences_noeuds + Lsavoirs_noeuds

    with open(fic, 'w'):
        pass

    with open(fic, "w") as f:
        for line in lines:
            f.write(line)
            if line == "<nodes>":
                f.write("\n")
                for e in Lnoeuds:
                    f.write(e)
                    f.write("\n")
            if "faultnameformat" in line:
                f.write("\n")
                for e in Lnoeuds_pos:
                    f.write(e)
                    f.write("\n")


def create_BNN_GeNIe(dico_compID_to_savoirID, dico_idquestions_to_idsavoir):
    # On retire les savoirs qui ne sont pas évalués dans les questions
    dico_compID_to_savoirID = remove_savoirs_unused(
        dico_compID_to_savoirID, dico_idquestions_to_idsavoir)

    # Dans notre cas précis, on ne veut tester que les savoirs en relation avec la compétence C7 (sur les déterminants)
    dico_compID_to_savoirID = {
        k: v for k, v in dico_compID_to_savoirID.items() if k in COMPETENCES_A_EVALUER}
    print(dico_compID_to_savoirID)

    dict_parents_cpt = build_dict_parents_savoirs_sf(
        dico_compID_to_savoirID, dico_idquestions_to_idsavoir)

    writeFile(dico_compID_to_savoirID,
              dico_idquestions_to_idsavoir, dict_parents_cpt)


create_BNN_GeNIe(dico_compID_to_savoirID, dico_idquestions_to_idsavoir)
