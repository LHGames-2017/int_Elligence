"""Main"""
#pylint: disable=C0111,C0103,W0614,W0611,W0401

import json
import numpy
from flask import Flask, request
from structs import *
from random import randint

import DQN

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(40)] for y in range(40)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]),p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    otherPlayers = []

    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info})

    #Pour ce projet, nous implémentons l'algorithme du q learning
    
    #On centre la carte sur notre personnage
    x = x-10
    y = y-10
    
    #Ajuste Q max
    gamma = 0.5
    
    r = DQN.build_r(deserialized_map) #construit r
    q = numpy.zeros_like(r) #construit q et initialise tout à 0
    
    action = DQN.choisir_action(x,y,r)    #Donne prochaine action à exécuter
   
    #Donne next State
    nextPosX = x
    nextPosY = y
    
    # modifie le prochain états (les pos. en x et y) pour trouver qmax
    if (action == 0):
        nextPosX = x-1
    elif (action == 1):
        nextPosX = x+1
    elif (action == 2):
        nextPosY = y-1
    elif (action == 3):
        nextPosY = y+1
    
    
    maxQ = DQN.findMaxQ(nextPosX, nextPosY, q) #DonneLa prochaine action pour le prochain état.
    
    q[x][y][action] = r[x][y][action] + gamma*maxQ #update q.C'est la formule de Bell
    
    #On met l'état suivant comme l'état présent pour le prochain tour
    x=nextPosX
    y=nextPosY
    # On décentre la carte du joueur pour ne pas causer prob. avec serveur
    x = x+10
    y=y+10
    
    print(x,y,action,player.CarriedRessources)
    
    if(action < 4):
        return create_move_action(Point(x, y))
    elif (action == 4):
        return create_collect_action(Point(x-1,y))
    elif (action == 5):
        return create_collect_action(Point(x+1,y))
    elif (action == 6):
        return create_collect_action(Point(x,y-1))
    elif (action == 7):
        return create_collect_action(Point(x,y+1))

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
