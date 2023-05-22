from fltk import *
from game import *
from perso import *
from map import *
from menu import *
from confettis import *
import time


cree_fenetre(600,700)

records = []
back=True

while back: # Affiche le menu et inicialise toutes les varable utiles au jeu
    
    ev = donne_ev()
    tev = type_ev(ev)
    
    level = menu()

    game = Game(level)
    game.charger()
    game.liste_cases()
    game.afficher() #affiche la map
    joueur = game.info[0]
    
    player = Aventurier(joueur)
    player.affiche_perso()

    dragon = Dragon(game.info_dragon)
    dragon.affiche_dragon()
    num_conf = 1
    
    moves = 0

    startTime = time.time()
    totalTime = 0
    temps_condition = None
    
    
    if tev == 'Quitte':  # on sort de la boucle
        back = False
        break
   
    while True:

        mise_a_jour()

        ev = donne_ev()
        tev = type_ev(ev)

        x = abscisse_souris()
        y = ordonnee_souris()
        
        # timer
        roundTime = float('%.1f' % (time.time() - startTime + totalTime))
        
        if fin_partie(player,dragon,game):

            if len(dragon.info) == 0:
                    
                    num_conf = display_confettis(num_conf,200,10)

                    if temps_condition is None:
                        temps_condition = roundTime
                        a = (moves,temps_condition)
                        records.append(a)
                        liste_triee = sorted(records, key=cle_tri)
                        affiche_victoire(moves,temps_condition,liste_triee)

                    if (tev == 'Touche' and touche(ev) == 'Escape')\
                    or (tev == "ClicGauche" and 250 <= x <= 350 and 360 <= y <= 390):
                        250,360,350,390
                        back = True
                        break

                    
            else: # Mort du joueur
                
                game.afficher()
                mort(player)

                affiche_defaite()

                # Bouton retour
                if (tev == 'Touche' and touche(ev) == 'Escape')\
                    or (tev == "ClicGauche" and 250 <= x <= 350 and 360 <= y <= 390):
                        250,360,350,390
                        back = True
                        break
                
                # Bouton restart
                if (tev == 'Touche' and touche(ev) == 'r')\
                    or(tev == "ClicGauche" and 250 <= x <= 350 and 300 <= y <= 330):
                    
                    game = Game(level)
                    game.charger()
                    game.liste_cases()
                    game.afficher() #affiche la map
                    joueur = game.info[0]
                    
                    player = Aventurier(joueur)
                    player.affiche_perso()

                    dragon = Dragon(game.info_dragon)
                    dragon.affiche_dragon()

                    num_conf = 1
            
                    moves = 0

                    startTime = time.time()
                    totalTime = 0
                    temps_condition = None

       
        else:

            if tev== "ClicDroit": # Poser le tresor

                if (roundup(y),roundup(x)) != player.position :

                    if (roundup(y),roundup(x)) in dragon.info:
                            
                            if dragon.info[(roundup(y),roundup(x))] == 99:
                                if game.nombre_tresor>=0:
                                    efface("tresor")
                                    game.nombre_tresor +=1

                                    efface("numtresor")
                                    texte(280, 650, str(game.nombre_tresor)+"/ 3", couleur = "black",tag="numtresor")

                                    dragon.efface_dragon((roundup(y),roundup(x)))
                                    game.pose_tresor = False
                                    affiche_chemin(game.donjon,player.position,dragon.info)

                    elif game.pose_tresor == False:
                            if game.nombre_tresor > 0:
                                if roundup(y) <= 5:
                                    dragon.placer_tresor((roundup(y),roundup(x)))
                                    game.nombre_tresor -= 1
                                    efface("numtresor")
                                    texte(280, 650, str(game.nombre_tresor)+"/ 3", couleur = "black",tag="numtresor")
                                    game.pose_tresor = True
                                    affiche_chemin(game.donjon,player.position,dragon.info)



            if tev == "ClicGauche": # Tourner une salle du donjon
                
                if y < 600: # pour ne pas faire d'erreur lorsque le clic est pas dans la zone du jeu
                    game.pivoter((roundup(y),roundup(x)))
                    game.afficher()
                    dragon.affiche_dragon()
                    player.affiche_perso()
                    affiche_chemin(game.donjon,player.position,dragon.info)

                    moves += 1


            if (tev == 'Touche' and touche(ev) == 'space'): # Faire deplacer le chevalier

                
                new_pos = affiche_chemin(game.donjon,player.position,dragon.info)

                if new_pos != None:
                    #player.position = new_pos[-1]
                    player.deplacement(new_pos)

                rencontre(player,dragon,game)
                game.afficher()
                dragon.affiche_dragon()

                

                player.affiche_perso()
                affiche_chemin(game.donjon,player.position,dragon.info)


        
        # Bouton retour
        if (tev == 'Touche' and touche(ev) == 'Escape')\
                or (tev == "ClicGauche" and 10 <= x <= 100 and 600 <= y <= 700):
            back = True
            break

        # Bouton restart
        if (tev == 'Touche' and touche(ev) == 'r')\
            or(tev == "ClicGauche" and 500 <= x <= 600 and 600 <= y <= 700):
            
            game = Game(level)
            game.charger()
            game.liste_cases()

            game.afficher() #affiche la map
            joueur = game.info[0]
            player = Aventurier(joueur)
            player.affiche_perso()

            dragon = Dragon(game.info_dragon)
            dragon.affiche_dragon()

            num_conf = 1
    
            moves = 0

            startTime = time.time()
            totalTime = 0
            temps_condition = None


        if tev == 'Quitte':  # on sort de la boucle
            back = False
            break
    
