from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_au_choix_123'

# --- CONFIGURATION EMAIL ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'angebogui35@gmail.com' # Ton adresse Gmail
app.config['MAIL_PASSWORD'] = 'xdtegafoyfdttltg' # Ton code de 16 lettres
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/etape1', methods=['POST'])
def etape1():
    session['montant'] = request.form.get('montant')
    return render_template('etape1.html')

@app.route('/etape2', methods=['POST'])
def etape2():
    session['nom'] = request.form.get('nom')
    session['prenom'] = request.form.get('prenom')
    session['lieu'] = request.form.get('lieu') # <--- AJOUTE CETTE LIGNE
    return render_template('etape2.html')

@app.route('/etape3', methods=['POST'])
def etape3():
    # 1. On récupère le téléphone envoyé
    session['telephone'] = request.form.get('telephone')
    
    # 2. On prépare l'email avec toutes les infos stockées
    msg = Message("🚀 Nouvelle demande de prêt !",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    
    msg.body = f"""
    Nouvelle demande reçue :
    - Client : {session.get('nom')} {session.get('prenom')}
    - Ville : {session.get('lieu')}
    - Montant : {session.get('montant')} FCFA
    - Contact : {session.get('telephone')}
    """
    
    # 3. On envoie l'email
    try:
        mail.send(msg)
        return render_template('succes.html')
    except Exception as e:
        return f"Erreur lors de l'envoi : {str(e)}"

