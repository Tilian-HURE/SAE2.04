## Fonction utiles

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])


def incrementer_hexa(hexa, pas):
    """Incrémente des nombres hexadécimaux.
    :param: hexa : nombre hexadécimal à incrémenter
    :param: pas : pas d'incrémentation
    :return: un nombre hexadécimal"""
    nombreNum = min(max(int(hexa.replace('#', ''), 16)+pas, 0), int(len(hexa)*'F', 16))
    nombreHexa = hex(nombreNum).replace('0x', '')
    return nombreHexa.upper()


def generer_degrade_couleur_hexa(couleur, etapes, pas):
    """Génère une liste de couleurs hexadécimales dégradées.
    :param: couleur : couleur de départ du dégradé
    :param: etapes : nombre d'étapes du dégradé
    :param: pas : pas de dégradé (écart entre les couleurs)
    :return: une liste de couleurs hexadécimales (string)"""    
    listeCouleurs = [couleur]
    for i in range(etapes-1):
        lastCouleur = listeCouleurs[-1] ##.replace('#', '')
        ##pairesHexa = [lastCouleur[i:i+2] for i in range(0, 6, 2)]
        couleurSup = ""
        ##for paire in pairesHexa:            
        nombreHexa = color_variant(lastCouleur, pas).upper().replace('#', '') ##incrementer_hexa(paire, pas)
        couleurSup =  '#'+(6-len(nombreHexa))*'0'+nombreHexa
        listeCouleurs.append(couleurSup) ##'#'+(6-len(couleurSup))*'0'+couleurSup)
    return listeCouleurs


print(generer_degrade_couleur_hexa('#0088FE', len(donnees), -5))



## Chiffres d'affaires par client

# Requête SQL-LID
curseur.execute(
    "SELECT ROUND(SUM(CO.montantTTC)) AS Chiffres_affaires, C.nomClient \
    FROM Client C, Commande CO \
    WHERE C.numClient = CO.numClient \
    GROUP BY C.numClient, C.nomClient \
    ORDER BY Chiffres_affaires DESC")


# Récupération des données
donnees = list(curseur)[:] # copie du curseur
chiffresAffaires = [ca[0] for ca in donnees]
nomClients = [nom[1] for nom in donnees]
    ##print(donnees, chiffresAffaires, nomClients)

    
# Définition des propriétés visuelles de la tarte graphique
explodes = [0.065, 0.065, 0.065] + [0 for i in range(10)] # 'explosures' de la tarte
colormap = plt.get_cmap('Spectral') # palette de couleurs
colors = [colormap(i) for i in np.linspace(0, 1, len(donnees))] # couleurs des parts de la tarte
    ##print(colors)

colormap = plt.get_cmap('Spectral') # palette de couleurs
colors = [colormap(i) for i in np.linspace(0, 1, len(donnees))] # couleurs des parts de la tarte
    ##print(colors)

    
# Initialisation de la tarte graphique
fig, pie1 = plt.subplots(figsize=(7, 7)) # création du schéma
pie1.pie(chiffresAffaires, wedgeprops={'linewidth':0, 'edgecolor':"white"},
         autopct='%1.1f%%', shadow=False, startangle=90,
         colors=colors, pctdistance=1.15, explode=explodes) #création de la tarte

pie1.set_title("Chiffres d'affaires par client") # titre du schéma
legend = pie1.legend(title="$\\bf{Clients}$", loc="center",
                     prop={'size':10}, labels=nomClients, bbox_to_anchor=(1, 0, 0.8, 1),
                     fontsize=50, labelspacing=1.5) # légende du schéma


# Sauvegarde et affichage du schéma
    ##plt.savefig("graphics/pie1.svg", bbox_extra_artists=(legend,), bbox_inches='tight', transparent=True)
plt.show()


## Commandes défectueuses

# Requêtes SQL-LID
curseur.execute(
    "SELECT TO_CHAR(dateCommande, 'MONTH') AS Mois, COUNT(numCommande) AS Nb_commandes_defectueuses \
    FROM Commande \
    WHERE numCommande IN ( \
        SELECT numCommande \
        FROM Detail_Commande \
        WHERE quantiteLivree = 0 \
        OR quantiteLivree < quantiteCommandee \
        OR quantiteLivree > quantiteCommandee) \
    GROUP BY TO_CHAR(dateCommande, 'MONTH'), TO_CHAR(dateCommande, 'mm') \
    ORDER BY TO_CHAR(dateCommande, 'mm') ASC") # Nombre de commandes défectueuses par mois
donnees = list(curseur)[:] # copie du curseur

curseur.execute(
    "SELECT TO_CHAR(dateCommande, 'MONTH') AS Mois, COUNT(DISTINCT numCommande) AS Nb_commandes_total \
    FROM Commande \
    GROUP BY TO_CHAR(dateCommande, 'MONTH'),TO_CHAR(dateCommande, 'mm') \
    ORDER BY TO_CHAR(dateCommande, 'mm') ASC") # Nombre total de commandes par mois
donnees2 = list(curseur)[:] # copie du curseur


# Récupération des données
mois = [mon[0].replace(' ', '') for mon in donnees]
nbCommandes = [cmd[1] for cmd in donnees]  
nbTotalCmd = [tcmd[1] for tcmd in donnees2]
    ##print(donnees, mois, nbCommandes, nbTotalCmd)


# Définition des propriétés visuelles du diagramme en bâton
colormap = plt.get_cmap('Spectral') # palette de couleurs
colors = [colormap(i) for i in np.linspace(0, 1, len(donnees))]


# Initialisation du diagramme en bâton
plt.subplots(figsize=(7, 7)) # création du schéma
plt.ylim(0, 15)
X_axis = np.arange(len(mois))
plt.xticks(X_axis, mois)

plt.bar(X_axis-0.2, nbCommandes, 0.4, label='Commandes défectueuses') # création du diagramme en bâton  color=['#cb334d']
plt.bar(X_axis+0.2, nbTotalCmd, 0.4, label='Total de commandes') ## color=['#3a7eb8']

plt.title("Commandes défectueuses sur les trois derniers mois") # titre et légende du schéma
plt.legend(labelspacing=1.5, loc='upper center')
plt.xlabel("Mois")
plt.ylabel("Nombres de commandes")

for i, nbCmd in enumerate(nbCommandes): # pourcentages des bâtons
    pourcentage = str(round((nbCmd/nbTotalCmd[i])*100, 1)) + '%'
    plt.text(i-0.308, nbCmd+0.5, pourcentage)
    plt.text(i+0.1, nbTotalCmd[i]+0.5, '100%')


# Sauvegarde et affichage du schéma
    ##plt.savefig("graphics/baton1.svg", bbox_extra_artists=(legend,), bbox_inches='tight', transparent=True)
plt.show()