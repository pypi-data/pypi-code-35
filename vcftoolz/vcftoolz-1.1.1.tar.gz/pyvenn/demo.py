# coding: utf-8

# ipython notebook requires this
# %matplotlib inline

# python console requires this
import matplotlib
matplotlib.use('Agg')

import itertools
import matplotlib.pyplot as plt
import random
import venn

persist_to_files = True

def random_set(population_size, sample_size):
    samples = random.sample(range(population_size), sample_size)
    return set(samples)

sets = [random_set(700, 600) for i in range(6)]
names = ["Tokyo", "New York", "London", "Paris", "Beijing", "Sydney"]
draw_funcs = [venn.venn2, venn.venn3, venn.venn4, venn.venn5, venn.venn6]
file_names = ["venn2.png", "venn3.png", "venn4.png", "venn5.png", "venn6.png"]
fill = [["logic", "number", "percent"]]
fill += [x for x in itertools.combinations(["logic", "number", "percent"], 2)]
fill += [["number"]]
name_colors = ['black' for i in range(6)]

for num_sets in range(2, 1+len(sets)):
    idx = num_sets - 2
    labels = venn.get_labels(sets[0:num_sets], fill=fill[idx])
    fig, ax = draw_funcs[idx](labels, names[0:num_sets], name_colors=name_colors)
    if persist_to_files:
        fig.savefig(file_names[idx], bbox_inches='tight')
        plt.close()
    else:
        plt.show()        


