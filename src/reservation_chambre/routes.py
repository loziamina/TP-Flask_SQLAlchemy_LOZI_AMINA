import datetime
from flask import Blueprint, jsonify,render_template, request
from .models import Reservation, Client, Chambre
from .forms import ReservationForm, AjoutClientForm, ChambreForm
from .database import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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
    id_client = data['id_client']
    id_chambre = data['id_chambre']
    date_arrivee = datetime.strptime(data['date_arrivee'])
    date_depart = datetime.strptime(data['date_depart'])
    
    chambre_disponible = Chambre.query.filter(
        Chambre.id == id_chambre,
        Chambre.reservations.any(
            (Reservation.date_arrivee < date_depart) &
            (Reservation.date_depart > date_arrivee)
        )
    ).first()

    if chambre_disponible:
        nouvelle_reservation = Reservation(
            id_client=id_client,
            id_chambre=id_chambre,
            date_arrivee=date_arrivee,
            date_depart=date_depart,
            statut='confirmée'
        )
        db.session.add(nouvelle_reservation)
        db.session.commit()
        return jsonify({"success": True, "message": "Réservation créée avec succès."})
    else:
        return jsonify({"success": False, "message": "Chambre non disponible pour les dates sélectionnées."})



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
