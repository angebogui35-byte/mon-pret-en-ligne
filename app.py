from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_longue_et_aleatoire'

# --- CONFIGURATION EMAIL ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'TON_EMAIL@gmail.com' # Remplace par ton Gmail
app.config['MAIL_PASSWORD'] = 'TON_CODE_16_LETTRES' # Ton mot de passe d'application Google
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
    return render_template('etape2.html')

@app.route('/etape3', methods=['POST'])
def etape3():
    session['telephone'] = request.form.get('telephone')
    
    # Préparation du mail avec toutes les infos de la session
    msg = Message("🚀 Nouvelle demande de prêt !",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']]) # Tu t'envoies le mail à toi-même
    
    msg.body = f"""
    Nouvelle demande reçue !
    
    Nom : {session.get('nom')}
    Prénom : {session.get('prenom')}
    Montant demandé : {session.get('montant')} FCFA
    Téléphone : {session.get('telephone')}
    """
    
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

    return render_template('succes.html')

if __name__ == '__main__':
    app.run(debug=True)
