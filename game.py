from fltk import *
import math
from collections import deque


def connecte(donjon, position1, position2):
    """
    Vérifie si deux positions adjacentes sont connectées dans le donjon.

    Paramètres :
    - donjon : liste de listes représentant le donjon.
    - position1 : tuple représentant la première position.
    - position2 : tuple représentant la deuxième position.

    Retour :
    - True si les positions sont adjacentes et connectées, False sinon.
    """
     
    a1, b1 = position1
    a2, b2 = position2
    if abs(a1-a2) + abs(b1-b2) != 1: # les salles sont-elles adjacentes ?
        return False
    if a1 > a2:
        return donjon[a1][b1][0] and donjon[a2][b2][2]
    elif a1 < a2:
        return donjon[a1][b1][2] and donjon[a2][b2][0]
    elif b1 > b2:
        return donjon[a1][b1][3] and donjon[a2][b2][1]
    else:
        return donjon[a1][b1][1] and donjon[a2][b2][3]  



def intention(donjon, position, dragons):
    """
    Retourne le chemin le plus court menant au dragon de plus haut niveau.

    Args:
        donjon (list[list[int]]): Une matrice representant le donjon.
        position (tuple[int, int]): La position de depart.
        dragons (dict[tuple[int, int], int]): Un dictionnaire contenant les positions des dragons et leur niveau.

    Returns:
        list[tuple[int, int]]: Le chemin le plus court menant au dragon de plus haut niveau, ou None s'il n'y a aucun chemin.
    """

    queue = deque([(position, [])]) # queue contenant la position de départ et le chemin parcouru jusqu'à cette position
    visited = set() # ensemble des positions visitées
    max_level = -1 # niveau du dragon de plus haut niveau trouvé
    shortest_path = None # chemin le plus court trouvé pour l'instant

    while queue:
        pos, path = queue.popleft()
        
        if pos in dragons:
            level = dragons[pos]
            if level > max_level:
                max_level = level
                shortest_path = path + [pos]
            continue
        
        if pos in visited:
            continue
        
        visited.add(pos)
        
        for new_pos in [(pos[0]+1,pos[1]), (pos[0],pos[1]+1), (pos[0]-1,pos[1]), (pos[0],pos[1]-1)]:
            if not (0 <= new_pos[0] < len(donjon) and 0 <= new_pos[1] < len(donjon[0])):
                continue
            if not connecte(donjon, pos, new_pos):
                continue
            queue.append((new_pos, path + [pos]))
    
    return shortest_path




def affiche_chemin(donjon, position, dragons):
    """
    Si il n'y a pas de chemin on n'affiche rien (sinon erreur)
    Sinon pour chaque position du chemin on affiche un carre rouge
    """

    chemin = intention(donjon, position, dragons)
    
    for i in range(20):
        efface("chemin"+str(i))
    
    if chemin is None:
        pass
    else:
        for i in range(len(chemin) - 1):
            y1, x1 = chemin[i]
            y2, x2 = chemin[i+1]

            # Calculer les coordonnées réelles des points de départ et d'arrivée
            x1_pixel = x1 * 100 + 55
            y1_pixel = y1 * 100 + 55
            x2_pixel = x2 * 100 + 55
            y2_pixel = y2 * 100 + 55

            # Dessiner une ligne rouge entre les points de départ et d'arrivée
            ligne(x1_pixel, y1_pixel, x2_pixel, y2_pixel, couleur='red', epaisseur=5, tag="chemin"+str(i))

        return chemin

 

def roundup(x):
    """
    Pour arrondir la valeur x à l'unité inferieur
    exemple: roundup(233) --> 2     roundup(23) --> 0

    """
    return int(math.ceil(x / 100.0)) - 1



def rencontre(aventurier,dragons,game):
    """
    Verifie pour les positions de chaque dragon si c'est 
    la meme position que le joueur

    Si le niveau du dragon est 99 cela signifie que c'est un tresor
    Sinon si le niveau du dragon est superieur au niveau du joueur alors renvoir False
    Sinon on efface le dragon et le niveau du joueur augmente de 1
    """
  
    for pos in dragons.info:

        
        if pos == aventurier.position:

            if dragons.info[pos] == 99:
                dragons.efface_dragon(pos)
                game.pose_tresor = False
                

            elif dragons.info[pos] > aventurier.niveau:
                return False
            
            
            else:
                dragons.efface_dragon(pos)
                aventurier.niveau +=1
    


def fin_partie(aventurier,dragons,game):
  """
  Renvoie l'etat de la partie :
    - True si il n'y a plus de dragons
    ou si l'aventurier a rencontre un dragon de plus haut niveau
    - False sinon
  """
  if len(dragons.info) == 0:
    return True
  
  if rencontre(aventurier,dragons,game) == False:
    return True
  
  else:
      return False


def mort(aventurier):
    """
    Change le booleen est_mort de la class Aventurier
    pour afficher la tombe a la place du chevalier
    """
    aventurier.est_mort = True
    aventurier.affiche_perso()


"""
def intention(donjon, position, dragons, visited=set()):
    i, j = position

    if position in dragons:
        return ([position], dragons[position])

    if position in visited:
        
        return None

    visited.add(position)
    best_path = None  # pour stocker le meilleur chemin trouvé jusqu'à présent
    best_level = float('-inf')  # pour stocker le niveau du dragon accessible le plus fort trouvé jusqu'à présent
    
    # recherche récursive dans les 4 directions
    for new_pos in [(i+1,j), (i,j+1), (i-1,j), (i,j-1)]:
        # vérifier que la nouvelle position est valide (dans les limites du donjon)
        if not (0 <= new_pos[0] < len(donjon) and 0 <= new_pos[1] < len(donjon[0])):
            continue
        # vérifier que la nouvelle position est connectée à la position actuelle
        if not connecte(donjon, position, new_pos):
            continue
        # récursion pour obtenir le chemin à partir de la nouvelle position
        new_path = intention(donjon, new_pos, dragons, visited)
        
        # si on a trouvé un chemin depuis la nouvelle position
        if new_path:
            # récupérer le niveau du dragon accessible à partir de la nouvelle position
            new_level = new_path[1]
            # si le niveau du dragon accessible est plus fort que tout ce qu'on a trouvé jusqu'à présent
            if new_level > best_level:
                # mettre à jour le meilleur chemin et le niveau du dragon accessible
                best_path = [position] + new_path[0]
                best_level = new_level
    
    if best_path is None:
        # aucun chemin n'a été trouvé à partir de cette position
        return None
    else:
        # un chemin a été trouvé à partir de cette position
        return (best_path, best_level)
"""
    

