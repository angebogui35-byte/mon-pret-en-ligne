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
    session['telephone'] = request.form.get('telephone')
    
    msg = Message("🚀 Nouvelle demande de prêt !",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    
    # On utilise .get() avec une valeur par défaut pour éviter les plantages
    msg.body = f"""
    Nouvelle demande :
    - Montant : {session.get('montant', 'Non précisé')}
    - Client : {session.get('nom', '')} {session.get('prenom', '')}
    - Ville : {session.get('lieu', 'Non précisée')}
    - Contact : {session.get('telephone', 'Non précisé')}
    """
    
    try:
        mail.send(msg)
        return render_template('succes.html')
    except Exception as e:
        return f"Erreur technique : {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
