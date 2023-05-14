
import constants as c
import graph_operations as g
import pandas as pd
import os.path

import agent_1 as a1
import agent_2 as a2
import agent_3 as a3
import agent_4 as a4
import agent_5 as a5
import agent_6 as a6
import agent_7 as a7
import agent_8 as a8
import agent_7a as a7a
import agent_8a as a8a
import agent_7b as a7b
import agent_8b as a8b



# for i in range(30):
#     c.GRAPH = g.generate_graph()
#     for j in range(100):
#         c.reset_constants()
#         g.init_characters()
#         output = a6.agent_6()

#         if output:
#             true_count+=1
#         else:
#             false_count+=1

# print("True count: ", true_count)
# print("False count: ", false_count)

agent_data = pd.DataFrame(columns = ["Graph No.", "Wins", "Losses", "Prey Found", "Predator Found"])  # DataFrame for data collection
for i in range(1,31):
    true_count = 0
    false_count = 0
    c.GRAPH = g.generate_graph()
    for j in range(100):
        c.PREY_CAUGHT_NUM = 0
        c.PRED_CAUGHT_NUM = 0
        c.STEPS = 0
        g.init_characters()
        output = a7.agent_7()

        if output:
            true_count+=1
        else:
            false_count+=1
        row = pd.DataFrame([{"Graph No.": i, "Wins": true_count, "Losses": false_count, "Prey Found": c.PREY_CAUGHT_NUM, "Predator Found": c.PRED_CAUGHT_NUM}])
        agent_data = pd.concat([agent_data, row], ignore_index=True)

agent_data.to_csv(os.path.join("data", "Agent7-Raw.csv"))