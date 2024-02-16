# TP-Flask_SQLAlchemy_LOZI_AMINA

# API de Réservation de Chambres d'Hôtel

## Routes Disponibles


### Ajouter Client
- **Endpoint:** `/api/clients`
- **Méthode:** POST
- **Description:** Ajoute un nouveau client à la base de données.
- **Corps de la Requête:** JSON contenant `nom` et `email`.

### Ajouter une Chambre
- **Endpoint:** `/api/chambres`
- **Méthode:** POST
- **Description:** Ajoute une nouvelle chambre à la base de données.
- **Corps de la Requête:** JSON contenant `numero`, `type`, et `prix`.

### Rechercher Chambres Disponibles
- **Endpoint:** `/api/chambres/disponibles`
- **Méthode:** GET
- **Description:** Retourne les chambres disponibles entre les dates spécifiées.
- **Paramètres de Requête:** `date_arrivee` et `date_depart` au format `YYYY-MM-DD`.

### Créer une Réservation
- **Endpoint:** `/api/reservations`
- **Méthode:** POST
- **Description:** Crée une nouvelle réservation pour un client.
- **Corps de la Requête:** JSON contenant `id_client`, `id_chambre`, `date_arrivee`, et `date_depart`.

### Annuler une Réservation
- **Endpoint:** `/api/reservations/<int:id>`
- **Méthode:** DELETE
- **Description:** Annule la réservation spécifiée par son ID.

### Modifier une Chambre
- **Endpoint:** `/api/chambres/<int:id>`
- **Méthode:** PUT
- **Description:** Met à jour les informations d'une chambre spécifiée par son ID.
- **Corps de la Requête:** JSON pouvant contenir `numero`, `type`, et `prix`.

### Supprimer une Chambre
- **Endpoint:** `/api/chambres/<int:id>`
- **Méthode:** DELETE
- **Description:** Supprime la chambre spécifiée par son ID.

## Utilisation

### pour tester les requète j'ai utiliser thunder client 

### pour lancer : 
- flask run --host=0.0.0.0
- le port utiliser 5002
- BDD utilisé : réservation_des_chambres

## Technologies Utilisées

- Flask
- SQLAlchemy
