import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Table Employés
cursor.execute("""
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    date_naissance DATE,
    poste TEXT,
    categorie TEXT
)
""")

# Table Paie
cursor.execute("""
CREATE TABLE IF NOT EXISTS paie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    mois TEXT NOT NULL,
    salaire_brut REAL,
    retenue REAL,
    prime REAL,
    salaire_net REAL,
    FOREIGN KEY(employee_id) REFERENCES employee(id)
)
""")

conn.commit()
conn.close()
print("Base de données initialisée.")