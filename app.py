from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from weasyprint import HTML

app = Flask(__name__)
DB_NAME = "db.sqlite"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

# Liste des employés
@app.route('/employees')
def employees():
    db = get_db()
    emps = db.execute("SELECT * FROM employee").fetchall()
    return render_template("employees.html", employees=emps)

# Ajouter un employé
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        poste = request.form['poste']
        categorie = request.form['categorie']

        db = get_db()
        db.execute("""
            INSERT INTO employee (nom, prenom, date_naissance, poste, categorie)
            VALUES (?, ?, ?, ?, ?)
        """, (nom, prenom, date_naissance, poste, categorie))
        db.commit()
        return redirect(url_for('employees'))
    return render_template("add_employee.html")

# Générer un bulletin PDF
@app.route('/bulletin/<int:employee_id>')
def generate_bulletin(employee_id):
    db = get_db()
    emp = db.execute("SELECT * FROM employee WHERE id=?", (employee_id,)).fetchone()
    paie = db.execute("SELECT * FROM paie WHERE employee_id=? ORDER BY mois DESC LIMIT 1", (employee_id,)).fetchone()

    if not paie:
        return "Aucun bulletin disponible."

    html_content = render_template("bulletin.html", emp=emp, paie=paie)
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    filename = f"bulletin_{employee_id}.pdf"
    with open(filename, "wb") as f:
        f.write(pdf)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)