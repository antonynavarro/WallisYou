from fltk import *

class Game :

    def __init__(self,fichier):
        self.fichier = fichier
        self.map = []
        self.info = []
        self.donjon = []
        self.info_dragon = {}
        self.nombre_tresor = 3
        self.pose_tresor = False

    def charger(self):
        """
        Ouvre le fichier self.fichier 
        Divise les données entre les 6 premières lignes (les données du donjon)
        et les autres lignes (Dragon et chevalier)

        Ajoute les données du fichier dans la liste map
        Ajoute les données du personnage dans la liste info
        Ajoute les données du dragon dans le dictionnaire info dragon
        """
    
        file = open(self.fichier,encoding="utf8")
        
        for i, line in enumerate(file):
            if i <6:
                self.map.append(line.rstrip())
            elif i >= 6:
                ligne_info = line.rstrip()
                self.info.append(ligne_info.split())
        print(self.info)

        get_dragon = self.info[1:]
        for d in get_dragon:
            self.info_dragon[(int(d[1]),int(d[2]))] = int(d[3])

        
            
        file.close()
   
    def liste_cases(self):
        """
        Pour chaque element de self.map on associe
        dans la liste self donjon le tuple qui correspond
        """

        dico_tuples = {
            '═' : (False,True,False,True),
            '║' : (True,False,True,False),
            '╔' : (False,True,True,False),
            '╗' : (False,False,True,True),
            '╚' : (True,True,False,False),
            '╝' : (True,False,False,True),
            '╠' : (True,True,True,False),
            '╣' : (True,False,True,True),
            '╦' : (False,True,True,True),
            '╩' : (True,True,False,True),
            '╨' : (True,False,False,False),
            '╡' : (False,False,False,True),
            '╥' : (False,False,True,False),
            '╞' : (False,True,False,False),
            '╬' : (True,True,True,True),
        }

        for ligne in self.map:
            l = []
            for case in ligne:
                l.append(dico_tuples[case])
            self.donjon.append((l))


    def afficher(self):
        """
        Affiche le donjon en dessinant tout d'abord des croix
        sur les coins de chaque salle
        Puis affiche un mur pour chaque coté de la salle où la valeur associé est True

        Affiche également les information du bas de la fenetre
        """

        efface("case")

        xa,ya = -25,-10
        xb,yb = 25,10

        xxa,yya = -10,-25
        xxb,yyb = 10,25
        
        
        a=0
        b=19
        for p in range(7):
            for pp in range(6):
                image(a,b, 'media/floor3.png',largeur=135, hauteur=135,ancrage='sw', tag='floor')
                a+=100
                
            a=0
            b+=100
        
        
        for i in range(7):
            for j in range (7):

                
                rectangle(xa,ya,xb,yb,couleur='black',remplissage='black')
                xa += 100
                xb += 100

                rectangle(xxa,yya,xxb,yyb,couleur='black',remplissage='black')
                xxa += 100
                xxb += 100

            ya += 100
            yb += 100
            xa = -25
            xb = 25

            yya += 100
            yyb += 100
            xxa = -10
            xxb = 10


        xa,ya = -25,0
        xb,yb = 25,10

        xxa,yya = -10,-25
        xxb,yyb = 10,25
        
        l = -1
        c = -1
        for ligne in self.donjon:
            l += 1
            for case in ligne:
                c +=1

                if case[0] == False:
                    rectangle(xa+50,ya,xb+50,yb,remplissage='black', tag = "case")
            
                if case[1] == False:
                    rectangle(xxa+100,yya+50,xxb+90,yyb+50,remplissage='black',tag = "case")
                
                if case[2] == False:
                    rectangle(xa+50,ya+90,xb+50,yb+92,remplissage='black',tag = "case")
                    
                if case[3] == False:
                    rectangle(xxa+10,yya+50,xxb,yyb+50,remplissage='black',tag = "case")
                
                xa += 100
                xb += 100

                xxa += 100
                xxb += 100

            c = -1

            ya += 100
            yb += 100
            xa = -25
            xb = 25

            yya += 100
            yyb += 100
            xxa = -10
            xxb = 10

        rectangle(0,602,600,625,remplissage='black')


        efface("txt")
        texte(10,650,"Back",couleur="black",tag="txt")
        texte(480,650,"Restart",couleur="black",tag="txt")

        image(250, 670, 'media/treasure.png',largeur=85, hauteur=85)
        efface("numtresor")
        texte(280, 650, str(self.nombre_tresor)+"/ 3", couleur = "black",tag="numtresor")


    def pivoter(self,position):
        """
        Effectue une rotation des valeurs vers la droite pour une position donnée dans le donjon.

        Paramètres :
        - position : tuple représentant la position dans le donjon.

        Retour :
        Aucun retour. La méthode modifie directement le donjon.

        Description :
        - La méthode récupère les valeurs de la case à la position donnée dans le donjon.
        - Elle crée une nouvelle liste `a` avec quatre éléments initialisés à False.
        - À l'aide d'une boucle, elle parcourt les valeurs de la case d'origine `b` et les décale vers la droite
        en les affectant à la liste `a`. La dernière valeur devient la première et les autres sont décalées.
        - Enfin, la méthode met à jour la case dans le donjon avec la nouvelle liste `a`, convertie en tuple.
        """
        
        b = self.donjon[position[0]][position[1]]
        a = [False,False,False,False]
        for i in range(len(b)):
            a[i] = b[i-1]

        self.donjon[position[0]][position[1]] = tuple(a)


def affiche_victoire(moves,time,L):
    
    rectangle(150,200,450,550,couleur='white',remplissage='black')
    texte(240, 210, "You Won !", couleur="red", taille=20)

    texte(200, 250, "Moves : "+ str(moves), couleur="white", taille=15)
    texte(200, 300, 'Time : '+str(time)+'s', couleur="white", taille=15)

    rectangle(250,360,350,390,couleur='red',remplissage='white' )
    texte(275,365,"Menu", couleur="black", taille=15)

    if len(L) == 0:
        texte(260, 400, "Records:", couleur="red", taille=15)
        texte(155, 440, "1st : Moves : N/A Time : N/A", couleur="gold", taille=15)
        texte(155, 480, "2nd : Moves : N/A Time : N/A", couleur="silver", taille=15)
        texte(155, 520, "3rd : Moves : N/A Time : N/A", couleur="brown", taille=15)
    elif len(L) == 1:
        texte(260, 400, "Records:", couleur="red", taille=15)
        texte(155, 440, "1st : Moves : " + str(L[0][0]) + "  Time : " + str(L[0][1])+'s', couleur="gold", taille=15)
        texte(155, 480, "2nd : Moves : N/A Time : N/A", couleur="silver", taille=15)
        texte(155, 520, "3rd : Moves : N/A Time : N/A", couleur="brown", taille=15)
    elif len(L) == 2:
        texte(260, 400, "Records:", couleur="red", taille=15)
        texte(155, 440, "1st : Moves : " + str(L[0][0]) + "  Time : " + str(L[0][1])+'s', couleur="gold", taille=15)
        texte(155, 480, "2nd : Moves : " + str(L[1][0]) + "  Time : " + str(L[1][1])+'s', couleur="silver", taille=15)
        texte(155, 520, "3rd : Moves : N/A Time : N/A", couleur="brown", taille=15)
    else:
        texte(260, 400, "Records:", couleur="red", taille=15)
        texte(155, 440, "1st : Moves : " + str(L[0][0]) + "  Time : " + str(L[0][1])+'s', couleur="gold", taille=15)
        texte(155, 480, "2nd : Moves : " + str(L[1][0]) + "  Time : " + str(L[1][1])+'s', couleur="silver", taille=15)
        texte(155, 520, "3rd : Moves : " + str(L[2][0]) + "  Time : " + str(L[2][1])+'s', couleur="brown", taille=15)


def affiche_defaite():
    """
    Affiche le message de defaite
    """
    rectangle(150,200,450,400,couleur='white',remplissage='black')
    texte(215, 210, "You Died !", couleur="red", taille=30)

    rectangle(250,300,350,330,couleur='red',remplissage='white' )
    texte(275,305,"Retry", couleur="black", taille=15)

    rectangle(250,360,350,390,couleur='red',remplissage='white' )
    texte(275,365,"Menu", couleur="black", taille=15)



def cle_tri(L):
    return (L[0],L[1])
        
            