from flask import Blueprint, jsonify,render_template, request
from .models import Reservation, Client, Chambre
from .forms import ReservationForm, AjoutClientForm, ChambreForm
from .database import db
from datetime import datetime


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# ajouter Client

@main.route('/api/clients', methods=['POST'])
def ajouter_client():
    data = request.get_json()
    nom = data['nom']
    email = data['email']
    client = Client(nom=nom, email=email)
    db.session.add(client)
    db.session.commit()
    return jsonify({"success": True, "message": "Client est ajouté avec succes."})

# ajouter une chambre
@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
    data = request.get_json()
    numero = data['numero']
    type = data['type']
    prix = data['prix']
    chambre = Chambre(numero=numero, type=type, prix=prix)
    db.session.add(chambre)
    db.session.commit()
    return jsonify({"success": True, "message": "Chambre est ajouté avec succes."})


#la recharche d'une chambre
@main.route('/api/chambres/disponibles', methods=['GET'])
def chambres_disponible():
    date_arrivee = request.args.get('date_arrivee')
    date_depart = request.args.get('date_depart')
    date_arrivee = datetime.strptime(date_arrivee)
    date_depart = datetime.strptime(date_depart)

    chambres_disponibles = Chambre.query.filter(
        Chambre.reservations.any(
            (Reservation.date_arrivee < date_depart) &
            (Reservation.date_depart > date_arrivee)
        )
    ).all()

    chambres_disponibles = [
        {"id": chambre.id, "numero": chambre.numero, "type": chambre.type, "prix": chambre.prix}
        for chambre in chambres_disponibles
    ]
    return jsonify(chambres_disponibles)

#la creation d'une reservation

@main.route('/api/reservations', methods=['POST'])
def creer_reservation():
    data = request.get_json()
    
    if 'id_client' not in data or 'id_chambre' not in data or 'date_arrivee' not in data or 'date_depart' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    try:
        date_arrivee = datetime.strptime(data['date_arrivee'], "%d %B, %Y")
        date_depart = datetime.strptime(data['date_depart'], "%d %B, %Y")
    except ValueError:
        return jsonify({'success': False, 'message': 'Format de date invalide. Utilisez dd-MM-yyyy.'}), 400

    chambre = Chambre.query.get(data['id_chambre'])
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    reservations_existantes = Reservation.query.filter(
        (Reservation.id_chambre == data['id_chambre']) &
        ((Reservation.date_arrivee < date_depart) & (Reservation.date_depart > date_arrivee))
    ).all()

    if reservations_existantes:
        return jsonify({'success': False, 'message': 'La chambre est déjà réservée pour les dates spécifiées.'}), 409

    nouvelle_reservation = Reservation(
        id_client=data['id_client'],
        id_chambre=data['id_chambre'],
        date_arrivee=date_arrivee,
        date_depart=date_depart
    )

    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation créée avec succès.'}), 201


#l'annulation d'une reservation
@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annuler_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"success": True, "message": "Réservation annulée avec succès."})

# la mise a jour d'une reservation

main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    chambre = Chambre.query.get_or_404(id)
    return jsonify({"success": True, "message": "Chambre mise à jour avec succès."})


# annuler une chambre par son id
@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    chambre = Chambre.query.get_or_404(id)
    db.session.delete(chambre)
    db.session.commit()
    return jsonify({"success": True, "message": "Chambre supprimée avec succès."})
