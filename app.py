from datetime import datetime
from turtle import clear
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
###############################################################
# configuration de la base de données et de l'app Flask
#
###############################################################

mdp = gedeon
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@localhost:5432/minip'.format(mdp)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db=SQLAlchemy(app)

###############################################################
#
# Declaration de la classe Categorie constructeur et methodes
#
###############################################################   
    
class Categorie(db.Model):
    __tablename__='categories'
    idcat=db.Column(db.Integer, primary_key=True)
    libelle=db.Column(db.String(50), nullable=False)
    categories=db.relationship('livres', backref='categories', lazy=True)
    
    
    def __init__(self, idcat, libelle):
        self.idcat=idcat
        self.libelle=libelle       
    
    
    def insert(self):
            db.session.add(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 
        
    def format_cat(self):
        return jsonify({
            'idcat': self.idcat,
            'libelle':self.libelle
            })    
        
        
###############################################################
#
# Declaration de la classe Livre constructeur et methodes
#
###############################################################        
class Livre(db.Model):
    
    __tablename__ = 'livres'
    id=db.Column(db.Integer, primary_key=True)
    isbn=db.Column(db.Integer, unique=True, nullable=False)
    titre=db.Column(db.String(50), nullable=False)  
    datePub=db.Column(db.DateTime, nullable=False)
    auteur=db.Column(db.String(50), nullable=False)
    editeur=db.Column(db.String(50), nullable=False)
    idcateg=db.Column(db.Integer, db.ForeignKey('categories.idcat'), nullable=False)
    


    def __init__(self, id, isbn, titre, datePub, auteur, editeur, idcateg):
        self.id=id
        self.isbn=isbn
        self.titre=titre
        self.datePub=datePub
        self.auteur=auteur
        self.editeur=editeur
        self.idcateg=idcateg
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))    
        
    def insert(self):
            db.session.add(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
            
    def format_li(self):
        return jsonify({
            'id': self.id,
            'isbn': self.isbn,
            'Titre': self.titre,
            'datePub': self.datePub,
            'auteur': self.auteur,
            'editeur': self.editeur,
            'idcateg': self.idcateg
            })

db.create_all()
###############################################################
#
#  Liste des tous les categories de livres
#
###############################################################

@app.route('/categories' ,methods=['GET'])
def get_all_categories():
    categories=Categorie.query.all()
    formated_categorie=[ categorie.format() for categorie in categories]
    return jsonify({
        'success' : True,
        'categorie' : formated_categorie,
        'total' : len(Categorie.query.all())
    })
###############################################################
#
# Ajouter un nouveau categorie de livre
#
###############################################################
    
@app.route('/categories', methods=['POST'])
def add_categorie():
    body=request.get_json()
    new_id = body.get('idcat', None)
    new_lib = body.get('libelle', None)
    categorie = Categorie(idcat=new_id, libelle=new_lib)
    categorie.insert()
    categories = Categorie.query.all()
    categorie_formated = [categorie.format() for categorie in categories]
    return jsonify({
        'created_id':categorie.idcat,
        'success':True,
        'total':len(Categorie.query.all()),
        'categorie':categorie_formated
    })
    
###############################################################
#
#  Liste des tous les livres
#
###############################################################   
@app.route('/livres' ,methods=['GET'])
def get_all_livres():
    livres=Livre.query.all()
    formated_livre=[ livre.format() for livre in livres]
    return jsonify({
        'success' : True,
        'categorie' : formated_livre,
        'total' : len(Livre.query.all())
    })
    
###############################################################
#
# Ajouter un nouveau livre
#
###############################################################
    
@app.route('/livres', methods=['POST'])
def add_livres():
    body=request.get_json()
    new_isbn = body.get('isbn', None)
    new_titre = body.get('titre', None)
    new_datePub = body.get('datePub', None)
    new_auteur = body.get('auteur', None)
    new_editeur = body.get('editeur', None)
    new_idcateg = body.get('idcateg', None)
    livre=Livre(isbn=new_isbn, titre=new_titre, datePub=new_datePub, auteur=new_auteur, editeur=new_editeur, idcateg=new_idcateg)
    livre.insert()
    livres=Livre.query.all()
    livres_formated = [livre.format() for livre in livres]
    return jsonify({
        'created_id' : livre.id,
        'success' : True,
        'total' : len(Livre.query.all()),
        'livre' : livres_formated,
    })
###############################################################
#
#Selectionner une categorie
#
###############################################################

@app.route('/categories/<int:idcat>', methods=['GET'])
def get_one_categorie(idcat):
    try:
        categorie = Categorie.query.get(idcat)
        if categorie is None:
            abort(404)
        else:
            return jsonify({
                'success' : True,
                'selected_id' : idcat,
                'selected_categorie' : categorie.format()
            })
    except:
        abort(400)

###############################################################
#
#Selectionner un livre
#
###############################################################        
@app.route('/livres/<int:id>', methods=['GET'])
def get_one_livre(id):
    try:
        livre=Livre.query.get(id)
        if livre is None:
            abort(404)
        else:
            return jsonify({
                'success' : True,
                'selected_id' : id,
                'selected_livre' : livre.format()
            })
    except:
        abort(400)

###############################################################
#
#Supprimer une categorie
#
###############################################################       
@app.route('/categories/<int:idcat>', methods=['DELETE'])
def delete_one_categorie(idcat):
    categorie = Categorie.query.get(idcat)
    if categorie is None:
        abort(404)
    else:
        categorie.delete()
        return jsonify({
            'success': True,
            'deleted_id': idcat,
            'deleted_categorie': categorie.format(),
            'total': Categorie.query.count()
        })
        
###############################################################
#
#Supprimer un livre
#
###############################################################
        
@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_one_livre(id):
    livre = Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        livre.delete()
        return jsonify({
            'success': True,
            'deleted_id': id,
            'deleted_livre': livre.format(),
            'total': Livre.query.count()
        })
        
###############################################################
#
#Modifier une categorie
#
###############################################################       
@app.route('/categories/<int:idcat>', methods=['PATCH'])
def update_categorie(idcat):
    #get data from json
    body=request.get_json()
    #get Categorie Book from database
    categorie = Categorie.query.get(idcat)
    #populate Categorie Book object
    categorie.libelle = body.get('libelle', None)
    if categorie.libelle is None:
        abort(400)
    else:
        categorie.update()
        return jsonify({
            'success': True,
            'updated_categorie': idcat,
            'new_categorie': categorie.format()
        })
        
###############################################################
#
#Modifier un livre
#
###############################################################        
@app.route('/livres/<int:id>', methods=['PATCH'])
def update_livre(id):
    #get data from json
    body=request.get_json()
    #get Book from database
    livre=Livre.query.get(id)
    #populate Book object
    livre.isbn = body.get('isbn', None)
    livre.titre = body.get('titre', None)
    livre.datePub = body.get('datePub', None)
    livre.auteur = body.get('auteur', None)
    livre.editeur = body.get('editeur', None)
    livre.idcateg = body.get('idcateg', None)
    if livre.isbn is None or livre.titre is None or livre.datePub is None or livre.auteur is None or livre.editeur is None:
        abort(400)
    else:
        livre.update()
        return jsonify({
            'success': True,
            'updated_Book': id,
            'new_Book': livre.format()
        })
###############################################################
#
#   capturer la liste des erreurs
#
###############################################################

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
    
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "----Internal server error----"
        }), 500
    
    
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400


if __name__=='__main__':
    app.run(debug=True)