# Création et apprentissage d'un réseau bayésien avec GeNie


## Mode d'emploi


  - Mode d'emploi
    - Prérequis
    - Création du réseau de neurone
        - Ressources
        - Execution
    - Apprentissage du réseau de neurone
        - Ressources
        - Execution
  - Description des fichiers
  - Ressources utilisés


# Mode d'emploi

## Prérequis

Il faut installer via la console windows et pip les différents packages.

```bash
$ pip install gspread
$ pip install oauth2client
$ pip install lxml
```

## Création du réseau de neurone
### Ressouces

| Type   | Fichier                                                                                                             | Description                                                                                                                                                                                                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Donnée | [savoirs.txt](text_input/savoirs.txt)                                                                               | Décrit les savoirs, savoir-faire, compétences                                                                                                                                                                                                                                                 |
| Donnée | [Feuille questions](https://docs.google.com/spreadsheets/d/1OP4lLVf3_oUxLsasizt3YPP34-qkQUL_uNtcnuUE_eI/edit#gid=0) | Liste les savoirs associés aux questions                                                                                                                                                                                                                                                      |
| Script | [lecture_feuille_competence.py](lecture_feuille_competence.py)                                                      | Récupère les différentes items du fichier [savoirs.txt](text_input/savoirs.txt)                                                                                                                                                                                                               |
| Script | [lecture_google_sheet.py](lecture_google_sheet.py)                                                                  | récupére les liens de causalités entre les différentes questions, savoirs et compétences décrit dans la [feuille des questions](https://docs.google.com/spreadsheets/d/1OP4lLVf3_oUxLsasizt3YPP34-qkQUL_uNtcnuUE_eI/edit#gid=0)                                                               |
| Script | [create_neural_network_genie.py](create_neural_network_genie.py)                                                    | utilise les structures de données crées par les deux script ci dessus. À son exécution ce script [ce fichier](genie_bnn/temoin.xdsl) qui contient notre réseau de neurone décrit dans [savoirs.txt](text_input/savoirs.txt) et [lecture_feuille_competence.py](lecture_feuille_competence.py) |


### Execution
Ci-dessous les manipulations qu'il faut effectuer pour **créer le réseau de neurone au format de GeNie**
1. Modifier (ou non) [les savoirs]("text_input/savoirs.txt") et [les questions](https://docs.google.com/spreadsheets/d/1OP4lLVf3_oUxLsasizt3YPP34-qkQUL_uNtcnuUE_eI/edit#gid=0)
2. Exectuer [create_neural_network_genie.py](create_neural_network_genie.py), cette execution va créer un nouveau fichier : [temoin.xdsl](genie_bnn/temoin.xdsl) qui contient notre réseau de neurone
```sh
$ python create_neural_network_genie.py
```
3. Ouvrir [temoin.xdsl](genie_bnn/temoin.xdsl) avec GeNie
4. Selectionner tout les noeuds (ctrl+a), dans la barre des menus ouvrir Layout → Graph Layout → Parent ordering → Mettre le spacing à 100%


## Apprentissage du réseau de neurone
### Ressouces

| Type   | Fichier                                                                                                          | Description                                                                                                                                                                     |
|--------|------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Donnée | [feuille expert](https://docs.google.com/spreadsheets/d/1wurnMBQt-9XxKqzNrw2hqmmCB2RasvHhh_vEb6SaCZg/edit) | appréciation des compétences et résultats aux QCM des élèves                                                                                                                    |
| Script | [readSheetExpert.py](readSheetExpert.py)                                                                         | parse la [feuille de l'expert](https://docs.google.com/spreadsheets/d/1wurnMBQt-9XxKqzNrw2hqmmCB2RasvHhh_vEb6SaCZg/edit)                                                  |
| Script | [create_learning_data_genie.py](create_learning_data_genie.py)                                                   | crée le fichier d'apprentissage pour GeNie en fonction la [feuille de l'expert](https://docs.google.com/spreadsheets/d/1wurnMBQt-9XxKqzNrw2hqmmCB2RasvHhh_vEb6SaCZg/edit) |

### Execution
Ci-dessous les manipulations qu'il faut effectuer pour **faire apprendre le réseau de neurone**
Prérequis : il faut naturellement que le réseau soit déjà affiché dans GeNie
1. Modifier (ou non) la [feuille de l'expert](https://docs.google.com/spreadsheets/d/1OP4lLVf3_oUxLsasizt3YPP34-qkQUL_uNtcnuUE_eI/edit#gid=0)
2. Exectuer [create_learning_data_genie.py](create_learning_data_genie.py), cette execution va créer un nouveau fichier : [learning_file_last.txt](genie_bnn/learning_file_last.txt) qui contient notre réseau de neurone
```sh
$ python create_learning_data_genie.py
```
3. Dans genie, File → Open data file  → Selectionnner [learning_file_last.txt](genie_bnn/learning_file_last.txt)   → rédurie la table (ctrl + tab)  →  barre des menus  →  Learning  →  Learn Parameters  
