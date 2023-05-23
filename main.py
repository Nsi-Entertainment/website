# This is a sample Python script.
from flask import Flask, render_template, request
from time import strftime
from datetime import datetime, timedelta

forum = Flask(__name__)

#Creation de la liste d'actuel message et des messages stockés
messages = []
old_message=[]
#On vérifie que le fichier "discussion.txt" existe (sinon on le créé)
file = open("discussion.txt", "a")
file.close()
#On récupère tous les anciens messages et on incrémente la liste "old_message"
file = open("discussion.txt", "r")
old_message = file.read()
if len(old_message) !=0:
    old_message = eval(old_message)
file.close()



@forum.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html',messages=messages)

@forum.route('/index',methods=['GET','POST'])
def index_():
    return render_template('index.html',messages=messages)


@forum.route('/forum',methods=['GET','POST'])
def chat():

    global messages
    global old_message
    #on réincrémente la liste "old_message" pour éviter tout bug lors du refresh de la page.
    file = open("discussion.txt", "r")
    old_message = file.read()
    if len(old_message) !=0:
        old_message = eval(old_message)
    file.close()
    messages = list(old_message)
    #Quand un utilisateur envoie un message on récupère : le pseudo, le message et l'heure
    if request.method == 'POST':
        heure_actuelle = datetime.now()
        nouvelle_heure = heure_actuelle + timedelta(hours=2) #je rajoute 2h car la machine qui heberge doit être 2h en retard
        format_heure = "%d-%m-%Y %H:%M:%S"
        heure_str = nouvelle_heure.strftime(format_heure)
        if len(request.form["message"]) == 0 or len(request.form["pseudo"]) == 0:
            return render_template('forum.html', messages=messages)
        new_message = [request.form["message"], request.form["pseudo"], heure_str]
        messages+= [new_message]
        #On stocke les données relatives au message envoyé
        file = open("discussion.txt", "a")
        file.write(str(new_message)+ ",")
        file.close()
        #On envoie le message
        return render_template('forum.html',messages=messages)
    else:
        #envoie des anciens messages lors du chargement de la page
        return render_template('forum.html',messages=messages)


@forum.route('/jeux',methods=['GET','POST'])
def jeux():
    return render_template('jeux.html',messages=messages)


if __name__ == "__main__":
    forum.run()
