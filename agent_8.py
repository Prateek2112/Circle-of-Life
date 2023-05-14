
import random

import algorithm as a
import constants as c
import graph_operations as g


def agent_8():
    is_alive = True
    is_win = False

#   Init to 1 / 49
#   Init to 1 at predator's location
#   loop
#       survey
#       prob update 1
#       agent move
#       prob update 2
#       prey move
#       prob update 3
#       pred move
#       prob update 4


    prey_new_belief = prey_init_belief() #   Init to 1 / 49
    prey_old_belief = prey_new_belief.copy()

    pred_new_belief = pred_init_belief() #   Init to 1 at predator's location
    pred_old_belief = pred_new_belief.copy()

    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win: #   loop
        prey_max_poss = [i for i, x in enumerate(prey_new_belief) if x == max(prey_new_belief)]
        max_poss_of_prey = random.choice(prey_max_poss)
        
        max_poss_of_pred = get_node_with_max_poss(pred_new_belief)

        if pred_new_belief[max_poss_of_pred] != 1:
            if survey(0, max_poss_of_pred): #       survey
                pred_new_belief = [0 for _ in range(c.SIZE)] #       prob update 1
                pred_new_belief[max_poss_of_pred] = 1
                c.PRED_CAUGHT_NUM += 1
            else:
                pred_new_belief = update_belief(pred_new_belief, max_poss_of_pred) #       prob update 1
            pred_old_belief = pred_new_belief.copy()
        else:
            if survey(1, max_poss_of_prey): #       survey
                prey_new_belief = [0 for _ in range(c.SIZE)] #       prob update 1
                prey_new_belief[max_poss_of_prey] = 1
                c.PREY_CAUGHT_NUM += 1
            else:
                prey_new_belief = update_belief(prey_new_belief, max_poss_of_prey) #       prob update 1
            prey_old_belief = prey_new_belief.copy()

        prey_max_poss = [i for i, x in enumerate(prey_new_belief) if x==max(prey_new_belief)]
        max_poss_of_prey = random.choice(prey_max_poss)

        max_poss_of_pred = get_node_with_max_poss(pred_new_belief)

        c.AGENT_POS = g.movement_even(c.AGENT_POS, max_poss_of_pred, max_poss_of_prey) #       agent move
        is_alive = g.check_if_alive()
        is_win = g.check_if_win()
        if not is_alive:
            print("You walked into a trap!!!")
            return False
        elif is_alive and is_win:
            print("You win!!!")
            return True
        elif c.STEPS == c.TIME_OUT_STEPS:
            print("Too slow to catch")
            return False
        
        prey_new_belief = update_belief(prey_new_belief, c.AGENT_POS) #       prob update 2
        prey_old_belief = prey_new_belief.copy()

        pred_new_belief = update_belief(pred_new_belief, c.AGENT_POS) #       prob update 2
        pred_old_belief = pred_new_belief.copy()

        is_win = c.PREY_POS.movement() #       prey move
        if is_win and is_alive:
            print("Lucky win!!!")
            return True
        prey_new_belief = prey_redistribute_belief(prey_new_belief, prey_old_belief) #       prob update 3
        prey_old_belief = prey_new_belief.copy()
        
        is_alive = c.PREDATOR_POS.movement() #       pred move
        if not is_alive:
            print("You are dead now!!!")
            return False        

        pred_new_belief = predator_move_belief_update(pred_old_belief) #       prob update 4
        pred_old_belief = pred_new_belief.copy()
    
    return False


def prey_init_belief():
    belief = [( 1 / (c.SIZE-1) ) for _ in range(c.SIZE)]
    belief[c.AGENT_POS] = 0
    return belief


def pred_init_belief():
    belief = [0 for _ in range(c.SIZE)]
    belief[c.PREDATOR_POS.position] = 1
    return belief


def get_node_with_max_poss(new_belief):
    max_poss = [i for i, x in enumerate(new_belief) if x == max(new_belief)]
    dist_to_agent = {}
    for n in max_poss:
        dist_to_agent[n] = len(a.get_shortest_path(n, c.AGENT_POS))
    minimum = min(dist_to_agent, key=dist_to_agent.get)
    closest_to_agent = [i for i in dist_to_agent if i == minimum]
    return random.choice(closest_to_agent)



def update_belief(new_belief, node):
    temp = 1 - new_belief[node]
    new_belief[node] = 0
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp
    return new_belief


def prey_redistribute_belief(new_belief, old_belief):
    for i in range(c.SIZE):
        new_belief[i] = old_belief[i] / (len(c.GRAPH[i]) + 1)
        for neighbour in c.GRAPH[i]:
            new_belief[i] = new_belief[i] + (old_belief[neighbour] / (len(c.GRAPH[neighbour]) + 1))
    return update_belief(new_belief, c.AGENT_POS)


def predator_move_belief_update(old_belief):
    distracted_new_belief = [0 for _ in range(c.SIZE)]
    focused_new_belief = [0 for _ in range(c.SIZE)]
    final_new_belief = [0 for _ in range(c.SIZE)]

    for i in range(c.SIZE):
        for neighbour in c.GRAPH[i]:
            distracted_new_belief[i] = distracted_new_belief[i] + (old_belief[neighbour] / len(c.GRAPH[neighbour]))

        distracted_new_belief[i] = distracted_new_belief[i] * 0.4

    for i in range(c.SIZE):
        poss_movement = predator_move_sim(i)
        for j in poss_movement:
            focused_new_belief[j] = focused_new_belief[j] + old_belief[i]/len(poss_movement)

    for i in range(c.SIZE):
        focused_new_belief[i] = focused_new_belief[i] * 0.6
        final_new_belief[i] = focused_new_belief[i] + distracted_new_belief[i]
    return update_belief(final_new_belief, c.AGENT_POS)


def predator_move_sim(node):
    dist = {}
    for neighbour in c.GRAPH[node]:
        dist[neighbour] = len(a.get_shortest_path(node, c.AGENT_POS))

    next_node = min(dist, key=dist.get)
    poss_movement = []
    for i in dist:
        if dist[i] == dist[next_node]:
            poss_movement.append(i)
            
    return poss_movement


def survey(mode, survey_node):
    if mode == 0:
        return survey_node == c.PREDATOR_POS.position
    else:
        return survey_node == c.PREY_POS.position
