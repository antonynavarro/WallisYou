from fltk import *


def menu(var=0):

    choix = [0,1,2,3,4]
    move = choix.index(var) # Position dans choix de la variante
    maps =['maps/map_test.txt','maps/map1.txt','maps/map2.txt','maps/map3.txt','maps/map4.txt']

    efface_tout()
    image(-25,-20,'media/background2.png',largeur=800, hauteur=800,ancrage='nw',tag='bg')
    image(30,15,'images/wallisyou.png',largeur=600, hauteur=200,ancrage='nw',tag='menu')
    
    # Choix variante (flèches)
    polygone([(200,470),(225,450),(225,490)],remplissage='lightgray',couleur='white',tag='menu')
    polygone([(400,470),(375,450),(375,490)],remplissage='lightgray',couleur='white',tag='menu')
    texte(305,400,'Level :',ancrage='center',couleur='lightgray',tag='menu')
    texte(302,470,str(var),ancrage='center',couleur='lightgray',taille='40',tag='var')

    # Bouton jouer
    image(305,620,'images/play.png',largeur=350, hauteur=300,ancrage='center',tag='menu')

    


    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        x = abscisse_souris()
        y = ordonnee_souris()
        # Action dépendante du type d'événement reçu:

        # Flèche Gauche
        if (tev == 'Touche' and touche(ev) == 'Left')\
                or (tev == 'ClicGauche' and (200 <= x <= 225 and 450 <= y <= 490)):
            if move > 0:
                var = False
                move -= 1

        # Flèche Droite
        if (tev == 'Touche' and touche(ev) == 'Right')\
                or (tev == 'ClicGauche' and (375 <= x <= 400 and 450 <= y <= 490)):
            if move < len(choix)-1:
                var = False
                move += 1
        
        # Bouton jouer
        if (tev == 'Touche' and touche(ev) == 'Return')\
                or (tev == 'ClicGauche' and (200 <= x <= 400 and 525 <= y <= 625)):
            efface('var')
            efface('menu')
            efface('bg')

            return maps[var]

        if tev == 'Quitte': # on sort de la boucle
            exit()

        
        if not var:
            var = choix[move]
            efface('var')
            texte(302,470,var,ancrage='center',couleur='lightgrey',taille='40',tag='var')

        mise_a_jour()



    