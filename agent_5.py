
import random

import algorithm as a
import constants as c
import graph_operations as g


#   Init to 1 at predator's location
#   loop
#       survey
#       prob update 1
#       agent move
#       prob update 2
#       pred move
#       prob update 3


def agent_5():
    is_alive = True
    is_win = False

    new_belief = init_belief() #   Init to 1 at predator's location
    old_belief = new_belief.copy()

    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win: #   loop
        max_poss_of_pred = get_node_with_max_poss(new_belief)

        if new_belief[max_poss_of_pred] != 1:
            if survey(max_poss_of_pred): #       survey
                new_belief = [0 for _ in range(c.SIZE)] #       prob update 1
                new_belief[max_poss_of_pred] = 1
                c.PRED_CAUGHT_NUM += 1
            else:
                new_belief = update_belief(new_belief, max_poss_of_pred) #       prob update 1
        old_belief = new_belief.copy()

        max_poss_of_pred = get_node_with_max_poss(new_belief)
        c.AGENT_POS = g.movement(c.AGENT_POS, c.PREY_POS.position, max_poss_of_pred) #       agent move
        is_alive = g.check_if_alive()
        is_win = g.check_if_win()
        if not is_alive:
            print("You walked into a trap!!!")
            # break
            return False
        elif is_alive and is_win:
            print("You win!!!")
            # break
            return True
        elif c.STEPS == c.TIME_OUT_STEPS:
            print("Too slow to catch")
            return False

        new_belief = update_belief(new_belief, c.AGENT_POS) #       prob update 2
        old_belief = new_belief.copy()

        is_win = c.PREY_POS.movement() #       prey move
        if is_win and is_alive:
            print("Lucky win!!!")
            # break
            return True

        is_alive = c.PREDATOR_POS.movement() #       pred move
        if not is_alive:
            print("You are dead now!!!")
            # break
            return False

        new_belief = predator_move_belief_update(old_belief) #       prob update 3
        old_belief = new_belief.copy()
    
    return False


def get_node_with_max_poss(new_belief):
    max_poss = [i for i, x in enumerate(new_belief) if x == max(new_belief)]
    dist_to_agent = {}
    for n in max_poss:
        dist_to_agent[n] = len(a.get_shortest_path(n, c.AGENT_POS))
    minimum = min(dist_to_agent, key=dist_to_agent.get)
    closest_to_agent = [i for i in dist_to_agent if i == dist_to_agent[minimum]]
    return random.choice(closest_to_agent)


def init_belief():
    belief = [0 for _ in range(c.SIZE)]
    belief[c.PREDATOR_POS.position] = 1
    return belief


def update_belief(new_belief, node):
    temp = 1 - new_belief[node]
    new_belief[node] = 0
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp
    return new_belief


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


def survey(survey_node):
    return survey_node == c.PREDATOR_POS.position
