
import algorithm as a
import constants as c
import graph_operations as g

import agent_1 as a1
import agent_2 as a2
import agent_3 as a3
import agent_4 as a4
import agent_5 as a5
# import agent_6 as a6
import agent_7 as a7
# import agent_8 as a8
import agent_7a as a7a
# import agent_8a as a8a
import agent_7b as a7b
# import agent_8b as a8b

c.GRAPH = g.generate_graph()
g.init_characters()

print("GRAPH", c.GRAPH)
print("Character position:")
print("Agent position: ", c.AGENT_POS)
print(c.PREDATOR_POS)
print(c.PREY_POS)
# a1.agent_1()
# a2.agent_2()
# a3.agent_3()
# a4.agent_4()
# a5.agent_5()
# a6.agent_6()
# a7.agent_7()
# a8.agent_8()
# a7a.agent_7a()
# a8a.agent_8a()
# a7b.agent_7b()
# a8b.agent_8b()
# print(a.shortest_path(0, 25))
# print("Actual:\n", a.get_shortest_path(0, 25, c.PREDATOR_POS.position))
# print("Trial:\n", a.get_shortest_path_trial(0, 25, c.PREDATOR_POS.position))
