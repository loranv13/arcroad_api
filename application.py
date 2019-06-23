from arcroad import application,db
import arcroad


'''
L'architecture de l'application est la suivante:

-- Les objets sont accessible sous forme d'api rest, l'url étant le type d'objet mis au pluriel
    -- projet   -> /projets
    -- serveur  -> /serveurs
    -- rglfw    -> /rglfws

-- Les formulaires de création des objets sont appelés avec l'url de type /objet en GET (au singulier). Cette route est dans le main.py.
Elle fait appel au formulaire classes.formulaire.NewObjetForm et au template templates.NewObjetTpl.html.
La requête est interceptée la requête envoyé en ajax à /objets en POST



'''
