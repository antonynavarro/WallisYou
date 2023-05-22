from fltk import *
import time

class Aventurier:

    def __init__(self, position):
        """
        self.position est un tuple (x,y)
        self.niveau indique le niveau du joueur
        self.est_est mort est a False si joueur est en vie
        """

        self.position = position[1:]
        self.niveau = 1
        self.est_mort = False

    def affiche_perso(self):
        """
        Affiche le chevalier sur la position self.position si il n'est pas mort
        Sinon on affiche une tombe
        """
        y=int(self.position[0])
        x=int(self.position[1])

        if self.est_mort == False:
            image(x*100+50, y*100+50, 'media/Knight_ss.png',largeur=116, hauteur=116, tag='player') #personnage
            rectangle(x*100+70, y*100+20,x*100+80, y*100+35,remplissage="white",tag='back_lv') #case blanche derière le niveau
            texte(x*100+72, y*100+22,str(self.niveau),taille=10,tag='lv') # niveau du joueur
            self.position = (y,x) 
        else:
            image(x*100+50, y*100+50, 'media/tombe.png',largeur=80, hauteur=80, tag='player') # la tombe lorsque le joueur meurt

    def deplacement(self,chemin):
        """
        Pour chaque position du chemin 
        -le personnage prend la position et est affiché
        -le personnage lmarque un arret de 0.2 second sur la case
        -puis on efface tout les element du personnage 
        ainsi que la ligne qui est derière lui
        """
        i = 0
        for (x,y) in chemin:
            self.position = (x,y)
            self.affiche_perso()
            time.sleep(0.2)
            mise_a_jour()
            efface("player")
            efface("lv")
            efface("back_lv")
            efface("chemin"+str(i))
            i+=1



class Dragon:

    def __init__(self,info):
        """
        self.info est un dictionnaire de forme :
        {(position): niveau, ...}
        """
        self.info = info

    def affiche_dragon(self):
        """
        Pour chaque position de dragons dans le dictionnaire self.info
        si le niveau du dragon n'est pas 99 on affiche l'image du dragon avec son niveau
        si le niveau est 99, il s'agit alors d'un tresor

        """
        for pos in self.info:

            y=pos[0]
            x=pos[1]
            niveau = self.info.get(pos) 
            
            if niveau!= 99:
                image(x*100+50, y*100+50, 'media/dragon.png',largeur=55, hauteur=55, tag='dragon') # image du dragon
                rectangle(x*100+70, y*100+20,x*100+80, y*100+35,remplissage="white",tag='back_lv') # case blanche derriere le niveau
                texte(x*100+72, y*100+22,str(niveau),taille=10,tag='lv') # niveau du dragon

            else:
                image(x*100+50, y*100+50, 'media/treasure.png',largeur=85, hauteur=85, tag="tresor") #tresor


    def placer_tresor(self,positon):
        """
        affiche une image du tresor sur position 
        et ajoute dans le dictionnaire self.info la position avec le niveau 99
        """
        y,x = positon
        self.info[positon]=99
        image(x*100+50, y*100+50, 'media/treasure.png',largeur=85, hauteur=85, tag="tresor")
       

    def efface_dragon(self,position):
        """
        Efface tout les dragons à la fin de la partie si le joueur meurt en
        supprimant tout les elements du dictionnaire self.info
        Cette fonction à été crée pour eviter un bug en fin de partie car
        on effacait le dragon mais le joueur ne mourrait pas
        """
        r = dict(self.info)
        del r[position]
        self.info = r
        
        

