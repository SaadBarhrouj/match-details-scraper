import requests  # Import the library to retrieve the HTML content of a web page.
from bs4 import BeautifulSoup  # Import the BeautifulSoup class from the bs4 module, necessary for parsing HTML content.
import csv  # Import the CSV module for writing data to CSV files.
import os  # Import the os module to handle directory operations

# Définir la date directement dans le code pour le test
date = "7/5/2024"  # Par exemple, le 1er juillet 2024

# Construct the URL using the date input
url = f"https://www.yallakora.com/match-center/?date={date}"

# Get the page content
page = requests.get(url)

def main(page):
    # Obtenir le contenu source de la page(byte code)
    src = page.content
    # Analyser le contenu avec BeautifulSoup
    soup = BeautifulSoup(src, "lxml")
    matches_details = []  # Initialiser une liste vide pour stocker les détails des matchs
    # Trouver toutes les divisions avec la classe 'matchCard', qui contiennent probablement les informations sur les matchs
    championships = soup.find_all("div", {'class': 'matchCard'})

    if not championships:
        print("Aucune carte de match trouvée. Sortie.")
        return

    def get_match_info(championship):
        # Extraire le titre du championnat depuis le deuxième enfant de la division championship
        championship_title = championship.contents[1].find("h2").text.strip()
        # Trouver tous les éléments de liste (li) contenant les informations individuelles sur les matchs
        all_matches = championship.contents[3].find_all("div", {'class': 'item'})
        number_of_matches = len(all_matches)
      
        for i in range(number_of_matches):
            # Obtenir les noms des équipes depuis les divs 'teamA' et 'teamB'
            team_A = all_matches[i].find('div', {'class': 'teamA'}).text.strip()
            team_B = all_matches[i].find('div', {'class': 'teamB'}).text.strip()
         
            # Obtenir le score du match depuis la div 'MResult'
            match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # Obtenir l'heure du match depuis la div 'MResult'
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()
          
            # Ajouter les détails du match à la liste matches_details sous forme de dictionnaire
            matches_details.append({
                "Championnat": championship_title,
                "Équipe A": team_A,
                "Équipe B": team_B,
                "Heure du match": match_time,
                "Score": score
            })

    # Itérer sur chaque championnat trouvé
    for championship in championships:
        get_match_info(championship)

    if not matches_details:
        print("Aucun détail de match trouvé. Sortie.")
        return

    # Définir un chemin de fichier valide
    output_dir = 'c:/Users/Lenovo/Documents'  # Utiliser un chemin valide sur votre système
    os.makedirs(output_dir, exist_ok=True)  # Créer le répertoire s'il n'existe pas

    output_file_path = os.path.join(output_dir, 'matchesdetails.csv')

    # Écrire les détails des matchs dans un fichier CSV
    keys = matches_details[0].keys()  # Extraire les clés (en-tête) du premier dictionnaire dans matches_details
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        # Créer un objet DictWriter CSV
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()  # Écrire la ligne d'en-tête (clés)
        dict_writer.writerows(matches_details)  # Écrire toutes les lignes (détails des matchs)
        print("Fichier CSV créé avec succès.")

main(page)
