import numpy as np
import math
import structs

def find_player_attack(max_health):
    switcher = {
        5:  1,
        8:  3,
        10: 5,
        15: 7,
        20: 9,
        30: 11,
    }
    return switcher[max_health]

def is_weaker_player_near(player, other_players):
    near = False
    other_position = structs.Point(0, 0)
    for other_p in other_players:
        if structs.Point.Distance(structs.Point(), p1=player.Position, p2=other_p.Position) == 1:
             if find_player_attack(other_p.MaxHealth) <= find_player_attack(player.MaxHealth) and other_p.Health <= player.Health:
                near = True
                other_position = other_p.Position

    return (near, other_position)

def establish_surroundings(player, deserialized_map):
    around = []
    x = player.Position.X
    y = player.Position.Y
    around.append(deserialized_map[x+1][y].Content)
    around.append(deserialized_map[x-1][y].Content)
    around.append(deserialized_map[x][y+1].Content)
    around.append(deserialized_map[x][y-1].Content)
    return around

def choose_action(player, other_players, deserialized_map):
    surroundings = establish_surroundings(player, deserialized_map)

    action = structs.ActionTypes.DefaultAction
    target = structs.Point()
    (near, other_p_pos) = is_weaker_player_near(player, other_players)
    #if low_health and potion
    # if near:
    #     action = structs.ActionTypes.AttackAction
    #     target = other_p_pos
    if structs.TileContent.Resource in surroundings and player.CarryingCapacity > player.CarriedRessources:
        action = structs.ActionTypes.CollectAction
        target = [surroundings == structs.TileContent.Resource][0]
    # elif structs.TileContent.Shop in surroundings and player.CarriedRessources >= 5000:
    #     action = structs.ActionTypes.PurchaseAction
    #     target = [surroundings == structs.TileContent.Shop][0]
    elif structs.TileContent.House in surroundings: #Ajouter 2e condition
        action = structs.ActionTypes.UpgradeAction
        target = [surroundings == structs.TileContent.Shop][0]
    else:
        target = move(player, deserialized_map)
        action = structs.ActionTypes.MoveAction
    return (action, target)

def move(player, deserialized_map):
    target = structs.Point()
    #if player.CarriedRessources == 5000:
        #target = find_nearest(player.Position, deserialized_map, structs.TileContent.Shop)
    if player.CarriedRessources == player.CarryingCapacity:
        target = find_nearest(player.Position, deserialized_map, structs.TileContent.House)
    else:
        target = find_nearest(player.Position, deserialized_map, structs.TileContent.Resource)
    return target

def find_nearest(player_position, deserialized_map, desired_type):
    nearest = structs.Point(0, 0)
    min_dist = 99999
    for i in range(20):
        for j in range(20):
            tile = deserialized_map[i][j]
            dist = structs.Point.Distance(nearest, structs.Point(tile.X, tile.Y), player_position)
            if tile.Content == desired_type and dist < min_dist:
                nearest = structs.Point(tile.X, tile.Y)
                min_dist = dist
    return nearest
