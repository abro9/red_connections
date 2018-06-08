#!./venv/bin/python3

import json
from math import log10, log1p

input_file = './data/big_files/popular_2000_0_pairs_comb.json'
output_path = './pcap_export.json'
max_nodes = 100

sub_list = []
g_items_dict = {}

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)

import_dict = import_dict['total']
pair_list = [k for k in sorted(import_dict, key=import_dict.get, reverse=True)]
for pair in pair_list:
    split = pair.split('-')
    s1, s2 = split[0], split[1]
    if s1 not in sub_list:
        sub_list.append(s1)
    if s2 not in sub_list:
        sub_list.append(s2)
    if len(sub_list) >= max_nodes:
        break

sub_list = sorted(sub_list)
print(sub_list)
node_list = []
for sub in sub_list:
    node_list.append({'name': sub, 'group':1})

num_nodes = len(node_list)
links_list = []

for start, sub1 in enumerate(sub_list):
    for sub2_index in range(start, num_nodes):
        sub2 = sub_list[sub2_index]
        pair_key = '{}-{}'.format(sub1, sub2)
        
        #if sub1 != sub2:
        if pair_key in pair_list:
            value = import_dict[pair_key]
            #value = log1p(import_dict[pair_key])
            #value = log10(1 + import_dict[pair_key])
            links_list.append({'source': start, 'target': sub2_index, 'value': value, 'draw': True})

links_list_by_values = sorted(links_list, key=lambda link: link['value'], reverse=True)
#print(links_list_by_values)
node_connection_dict = {}
remove_set_tuples = set()
for link in links_list_by_values:
    link['value'] = link['value']
    source = link['source']
    target = link['target']

    if source not in node_connection_dict.keys():
        node_connection_dict[source] = 0
    if target not in node_connection_dict.keys():
        node_connection_dict[target] = 0

    if node_connection_dict[source] < 5 and node_connection_dict[target] < 5:
        node_connection_dict[source] += 1
        node_connection_dict[target] += 1
    elif node_connection_dict[source] < 15 and node_connection_dict[source] >= 5:
        node_connection_dict[source] += 1
        link['draw'] = False
        link['value'] = link['value']/2
    elif node_connection_dict[target] < 15 and node_connection_dict[target] >= 5:
        node_connection_dict[target] += 1
        link['draw'] = False
        link['value'] = link['value']/2
    else:
        remove_set_tuples.add((source, target))
        link['draw'] = False
        link['value'] = link['value']/100

remove_set = set()
for s, t in remove_set_tuples:
    for i, link in enumerate(links_list):
        if link['source'] == s and link['target'] == t:
            remove_set.add(i)

filtered_links_list = []
for ind, link in enumerate(links_list):
    if ind not in remove_set:
    #if ind not in remove_set or link['value'] > 10:
        link['lval'] = 300 / log10(link['value'])
        if link['lval'] < 20 and link['draw'] == False:
            link['lval'] = 20
        elif link['lval'] < 50 and link['draw'] == True:
            link['lval'] = 50
        elif link['lval'] > 500:
            link['lval'] = 500
        filtered_links_list.append(link)

g_items_dict = {'links': filtered_links_list, 'nodes': node_list}
#g_items_dict = {'links': links_list, 'nodes': node_list}

with open(output_path, 'w+') as f:
    json.dump(g_items_dict, f, sort_keys=True, indent=1)

