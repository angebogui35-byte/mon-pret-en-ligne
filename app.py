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
    # On récupère TOUT ce qui vient de l'étape 1
    session['nom'] = request.form.get('nom')
    session['prenom'] = request.form.get('prenom')
    session['date_naissance'] = request.form.get('date_naissance')
    session['lieu'] = request.form.get('lieu') # Très important pour ton email !
    return render_template('etape2.html')

@app.route('/etape3', methods=['POST'])
def etape3():
    try:
        session['telephone'] = request.form.get('telephone')
        
        msg = Message("🚀 Nouvelle demande de prêt !",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])
        
        msg.body = f"Nouveau client : {session.get('nom')} - Tel: {session.get('telephone')}"
        
        print("Tentative d'envoi de l'email...") # Apparaîtra dans tes logs Render
        mail.send(msg)
        print("Email envoyé avec succès !")
        return render_template('succes.html')
    except Exception as e:
        print(f"ERREUR DÉTECTÉE : {str(e)}")
        return f"Détail de l'erreur : {str(e)}"
