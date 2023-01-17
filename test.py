import pm4py

import pandas as pd

log = pm4py.read_xes('./example_files/running-example.xes')

net, im, fm  = pm4py.discover_petri_net_heuristics(log)

# pm4py.view_petri_net(net,im,fm)
pm4py.save_vis_petri_net(net, im, fm, "net.svg")