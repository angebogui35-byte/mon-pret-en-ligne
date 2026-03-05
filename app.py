from flask import Flask, render_template, request, session
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'cle_de_secours_123'

# --- CONFIGURATION EMAIL ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'angebogui35@gmail.com'
app.config['MAIL_PASSWORD'] = 'xdtegafoyfdttltg' # Sans espaces
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
    # On sauvegarde tout ce qui vient de l'étape 1
    session['nom'] = request.form.get('nom')
    session['prenom'] = request.form.get('prenom')
    session['lieu'] = request.form.get('lieu') 
    return render_template('etape2.html')

@app.route('/etape3', methods=['POST'])
def etape3():
    # 1. On récupère le numéro
    session['telephone'] = request.form.get('telephone')
    
    # 2. On prépare l'email
    msg = Message("🚀 Nouvelle demande de prêt !",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    
    msg.body = f"Nouveau client : {session.get('nom')} {session.get('prenom')}\nContact : {session.get('telephone')}"
    
    # 3. On envoie l'email SANS bloquer la page
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Erreur email : {e}")
    
    # 4. On affiche la page de succès QUOI QU'IL ARRIVE
    return render_template('succes.html')
