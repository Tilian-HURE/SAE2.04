/*Modification des tables existantes*/

--Table Article
ALTER TABLE Article
DROP COLUMN prixVente;
ALTER TABLE Article
RENAME CONSTRAINT SYS_C00345037 TO ck_article_numcategorie;
ALTER TABLE Article
RENAME CONSTRAINT SYS_C00345038 TO ck_article_codetype;

--Table Commande
ALTER TABLE Commande
DROP COLUMN MontantHT;
ALTER TABLE Commande
DROP COLUMN MontantTTC;
ALTER TABLE Commande
RENAME CONSTRAINT SYS_C00345032 TO ck_commande_numclient;

--Table DetailCommande
ALTER TABLE DetailCommande
ADD CONSTRAINT ck_detailcommande_qtecommandee CHECK (quantiteCommandee > 0);
ALTER TABLE DetailCommande
RENAME CONSTRAINT SYS_C00345047 TO ck_detailcommande_numcommande;
ALTER TABLE DetailCommande
RENAME CONSTRAINT SYS_C00345048 TO ck_detailcommande_numarticle;

--Table TypeArticle
ALTER TABLE TypeArticle
DROP CONSTRAINT SYS_C00345022;


/*Ajout des nouvelles tables*/

--Table Client
DROP TABLE Client CASCADE CONSTRAINTS; --Suppression de la table existante
CREATE TABLE Client (
	numPersonne NUMBER,
	nomPersonne VARCHAR(50),
	adrRuePersonne VARCHAR(50),
	adrCodePostalPersonne VARCHAR(50),
	adrVillePersonne VARCHAR(50),
	adrPaysPersonne VARCHAR(50),
	telephonePersonne CHAR(12),
	mailPersonne VARCHAR(50),
	nomContact1 VARCHAR(50),
	TelephoneContact1 CHAR(12),
	FonctionContact1 VARCHAR(50),
	nomContact2 VARCHAR(50),
	TelephoneContact2 CHAR(12),
	FonctionContact2 VARCHAR(50),
	codeEtiquette CHAR(2),
	codeListe CHAR(1),
	CONSTRAINT pk_client PRIMARY KEY (numPersonne),
	CONSTRAINT fk_client_codeetiquette FOREIGN KEY (codeEtiquette) REFERENCES Etiquette(codeEtiquette),
	CONSTRAINT fk_client_codeliste FOREIGN KEY (codeListe) REFERENCES ListePrix(codeListe),
	CONSTRAINT ck_client_codeetiquette CHECK (codeEtiquette IS NOT NULL),
	CONSTRAINT ck_client_codeliste CHECK (codeListe IS NOT NULL)
);

--Table Fournisseur
CREATE TABLE Fournisseur (
	numPersonne NUMBER,
	nomPersonne VARCHAR(50),
	adrRuePersonne VARCHAR(50),
	adrCodePostalPersonne VARCHAR(50),
	adrVillePersonne VARCHAR(50),
	adrPaysPersonne VARCHAR(50),
	telephonePersonne CHAR(12),
	mailPersonne VARCHAR(50),
	nomContact1 VARCHAR(50),
	TelephoneContact1 CHAR(12),
	FonctionContact1 VARCHAR(50),
	nomContact2 VARCHAR(50),
	TelephoneContact2 CHAR(12),
	FonctionContact2 VARCHAR(50),
	codeEtiquette CHAR(2),
	codeListe CHAR(1),
	CONSTRAINT pk_fournisseur PRIMARY KEY (numPersonne),
	CONSTRAINT fk_fournisseur_codeetiquette FOREIGN KEY (codeEtiquette) REFERENCES Etiquette(codeEtiquette),
	CONSTRAINT fk_fournisseur_codeliste FOREIGN KEY (codeListe) REFERENCES ListePrix(codeListe),
	CONSTRAINT ck_fournisseur_codeetiquette CHECK (codeEtiquette IS NOT NULL),
	CONSTRAINT ck_fournisseur_codeliste CHECK (codeListe IS NOT NULL)
);

--Table DetailArticle
CREATE TABLE DetailArticle (
	codeArticle CHAR(1),
	quantiteMax NUMBER,
	quantiteStock NUMBER,
	seuilMin NUMBER,
	taille NUMBER,
	numArticle NUMBER,
	CONSTRAINT pk_detailarticle PRIMARY KEY (codeArticle),
	CONSTRAINT fk_detailarticle_numarticle FOREIGN KEY (numArticle) REFERENCES Article(numArticle),
	CONSTRAINT ck_detailarticle_numarticle CHECK (numArticle IS NOT NULL),
	CONSTRAINT ck_detailcommande_quantitemax CHECK (quantiteMax > 0)
);

--Table Proposer
CREATE TABLE Proposer (
	numPersonne NUMBER,
	codeArticle CHAR(1),
	prixAchat NUMBER,
	delaiLivraison NUMBER,
	CONSTRAINT pk_proposer PRIMARY KEY (numPersonne, codeArticle),
	CONSTRAINT fk_proposer_numpersonne FOREIGN KEY (numPersonne) REFERENCES Fournisseur(numPersonne),
	CONSTRAINT fk_proposer_codearticle FOREIGN KEY (codeArticle) REFERENCES DetailArticle(codeArticle)
);
