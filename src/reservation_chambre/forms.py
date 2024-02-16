from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField,IntegerField,SelectField,FloatField,DateTimeLocalField
from wtforms.validators import DataRequired


class AjoutClientForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class ChambreForm(FlaskForm):
    numero = IntegerField('Numéro de la chambre', validators=[DataRequired()])
    type = SelectField('Type de chambre', choices=[('simple', 'Simple'), ('double', 'Double'), ('suite', 'Suite')], validators=[DataRequired()])
    prix = FloatField('Prix ', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class ReservationForm(FlaskForm):
    id_client = IntegerField('ID du Client', validators=[DataRequired()])
    id_chambre = IntegerField('ID de la Chambre', validators=[DataRequired()])
    date_arrivee = DateTimeLocalField('Date de arrivée',  validators=[DataRequired()])
    date_depart = DateTimeLocalField('Date de départ', validators=[DataRequired()])
    statut = SelectField('Statut de la réservation', choices=[('confirmée', 'Confirmée'), ('annulée', 'Annulée')], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')