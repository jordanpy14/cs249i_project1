import json
import ipaddress
from collections import Counter, defaultdict
import networkx as nx
from tqdm import tqdm


def load_as_names(file_path):
    as_names = {}

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                asn = data['asn']
                name = data['name']
                as_names[asn] = name
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    return as_names

    
def find_peers_updated(file_path, as_names, target_asns):
    peers = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'entries' in data:
                    for entry in data['entries']:
                        if 'path_attributes' in entry:
                            for attribute in entry['path_attributes']:
                                if attribute['type'] == 2 and 'as_paths' in attribute:
                                    for path in attribute['as_paths']:
                                        if 'asns' in path:
                                            # Find the index of Stanford's ASN (32) in the AS path
                                            as_path = path['asns']
                                            for asn in target_asns:
                                                if asn in as_path:
                                                    index_of_asn = as_path.index(asn)
                                                    # Skip any consecutive occurrences of the same ASN after 32
                                                    for next_asn_index in range(index_of_asn + 1, len(as_path)):
                                                        if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                            peers.add(as_path[next_asn_index])
                                                            break
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON
    for asn in target_asns:
        if asn in peers:
            peers.remove(asn)
    print(peers)
    peer_names = {asn: as_names.get(asn, 'Unknown') for asn in peers}
    # Write the output to a file
    with open('peers_updated.txt', 'w') as file:
        for asn, name in peer_names.items():
            file.write(f"ASN: {asn}, Name: {name}\n")
    return peer_names

def find_peers(file_path, as_names):
    peers = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'entries' in data:
                    for entry in data['entries']:
                        if 'path_attributes' in entry:
                            for attribute in entry['path_attributes']:
                                if attribute['type'] == 2 and 'as_paths' in attribute:
                                    for path in attribute['as_paths']:
                                        if 'asns' in path:
                                            # Find the index of Stanford's ASN (32) in the AS path
                                            as_path = path['asns']
                                            if 32 in as_path:
                                                # index_of_32 = path['asns'].index(32)
                                                # # Check if there is an ASN after 32 and add it to the peers set
                                                # if index_of_32 < len(path['asns']) - 1:
                                                #     peers.add(path['asns'][index_of_32 + 1])
                                                index_of_32 = as_path.index(32)
                                                # Skip any consecutive occurrences of the same ASN after 32
                                                for next_asn_index in range(index_of_32 + 1, len(as_path)):
                                                    if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                        peers.add(as_path[next_asn_index])
                                                        break  
                                            if 29957 in path['asns']:
                                                # index_of_29957 = path['asns'].index(29957)
                                                # if index_of_29957 < len(path['asns']) - 1:
                                                #     peers.add(path['asns'][index_of_29957 + 1])
                                                index_of_29957 = as_path.index(29957)
                                                # Skip any consecutive occurrences of the same ASN after 29957
                                                for next_asn_index in range(index_of_29957 + 1, len(as_path)):
                                                    if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                        peers.add(as_path[next_asn_index])
                                                        break
                                            if 36306 in path['asns']:
                                                # index_of_36306 = path['asns'].index(36306)
                                                # if index_of_36306 < len(path['asns']) - 1:
                                                #     peers.add(path['asns'][index_of_36306 + 1])
                                                index_of_36306 = as_path.index(36306)
                                                # Skip any consecutive occurrences of the same ASN after 36306
                                                for next_asn_index in range(index_of_36306 + 1, len(as_path)):
                                                    if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                        peers.add(as_path[next_asn_index])
                                                        break
                                            if 46749 in path['asns']:
                                                # index_of_46749 = path['asns'].index(46749)
                                                # if index_of_46749 < len(path['asns']) - 1:
                                                #     peers.add(path['asns'][index_of_46749 + 1])
                                                index_of_46749 = as_path.index(46749)
                                                # Skip any consecutive occurrences of the same ASN after 46749
                                                for next_asn_index in range(index_of_46749 + 1, len(as_path)):
                                                    if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                        peers.add(as_path[next_asn_index])
                                                        break
                                            if 46750 in path['asns']:
                                                # index_of_46750 = path['asns'].index(46750)
                                                # if index_of_46750 < len(path['asns']) - 1:
                                                #     peers.add(path['asns'][index_of_46750 + 1])
                                                index_of_46750 = as_path.index(46750)
                                                # Skip any consecutive occurrences of the same ASN after 46750
                                                for next_asn_index in range(index_of_46750 + 1, len(as_path)):
                                                    if as_path[next_asn_index] != as_path[next_asn_index - 1]:
                                                        peers.add(as_path[next_asn_index])
                                                        break
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON
    if 32 in peers:
        peers.remove(32)
    if 29957 in peers:
        peers.remove(29957)
    if 36306 in peers:
        peers.remove(36306)
    if 46749 in peers:
        peers.remove(46749)
    if 46750 in peers:
        peers.remove(46750)
    print(peers)
    peer_names = {asn: as_names.get(asn, 'Unknown') for asn in peers}
    # Write the output to a file
    with open('peers.txt', 'w') as file:
        for asn, name in peer_names.items():
            file.write(f"ASN: {asn}, Name: {name}\n")
    return peer_names


def find_private_iBGP(file_path, as_names):
    iBGP = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'entries' in data:
                    for entry in data['entries']:
                        if 'path_attributes' in entry:
                            for attribute in entry['path_attributes']:
                                if attribute['type'] == 2 and 'as_paths' in attribute:
                                    for path in attribute['as_paths']:
                                        if 'asns' in path:
                                            # Find the index of Stanford's ASN (32) in the AS path
                                            as_path = path['asns']
                                            for asn in as_path:
                                                if as_names.get(asn, 'Unknown') == "-Private Use AS-":
                                                    iBGP.add(asn)
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON
    iBGP_names = {asn: as_names.get(asn, 'Unknown') for asn in iBGP}
    # Write the output to a file
    with open('iBGP.txt', 'w') as file:
        for asn, name in iBGP_names.items():
            file.write(f"ASN: {asn}, Name: {name}\n")
    return iBGP_names, iBGP

def count_non_matching_as_paths(file_path, target_asns):
    non_matching_count = 0
    unique_prefixes = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'entries' in data:
                    for entry in data['entries']:
                        if 'path_attributes' in entry:
                            for attribute in entry['path_attributes']:
                                if attribute['type'] == 2 and 'as_paths' in attribute:
                                    for path in attribute['as_paths']:
                                        if 'asns' in path and path['asns']:
                                            # Check if the last ASN is not in the target list
                                            if path['asns'][-1] not in target_asns:
                                                non_matching_count += 1
                                                unique_prefixes.add(path['asns'][-1])
                                                # add prefix to set
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    return non_matching_count, len(unique_prefixes)

def question_3():
    as_names_file_path = 'as_names.json'
    as_names = load_as_names(as_names_file_path)

    file_path = 'table.json'
    # target_asns = {32, 29957, 36306, 46749, 46750, 3671, 54531, 65400, 65105}
    # non_matching_count, set_size = count_non_matching_as_paths(file_path, target_asns)
    # print(f"Number of routes not ending with specified ASNs: {non_matching_count}, no copies: {set_size}")
    
    iBGP_names, iBGP = find_private_iBGP(file_path, as_names)
    print(iBGP)
    iBGP.add(32)
    iBGP.add(29957)
    iBGP.add(36306)
    iBGP.add(46749)
    iBGP.add(46750)
    stanford_peers = find_peers_updated(file_path, as_names, iBGP)

# def question_3():
#     as_names_file_path = 'as_names.json'
#     as_names = load_as_names(as_names_file_path)

#     file_path = 'table.json'
#     stanford_peers = find_peers(file_path, as_names)


def count_prefixes(file_path):
    prefixes = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'prefix' in data:
                    prefixes.add(data['prefix']['prefix'])
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    return len(prefixes)

def count_external_prefixes(file_path, stanford_prefixes):
    external_prefixes = set()

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if 'prefix' in data:
                    prefix = data['prefix']['prefix']
                    if not any(ipaddress.ip_network(prefix).overlaps(ipaddress.ip_network(stanford_prefix)) for stanford_prefix in stanford_prefixes):
                        external_prefixes.add(prefix)
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    return len(external_prefixes)


def question1():
    file_path = 'table.json'
    stanford_prefixes = ['3.5.218.0/24', '212.48.130.0/24', '177.75.40.0/24', '64.40.147.0/24', '103.48.16.0/22', '186.32.66.0/24']  # Replace with actual Stanford prefixes

    total_prefixes = count_prefixes(file_path)
    print(f"Total routed prefixes: {total_prefixes}")

    external_prefix_count = count_external_prefixes(file_path, stanford_prefixes)
    print(f"Routed prefixes outside of Stanford: {external_prefix_count}") 
   
def analyze_asns(file_path, as_names):
    asns = set()
    originating_asns = set()
    transit_origin_asns = set()
    prefix_counts = Counter()
    ip_counts = Counter()
    transit_ip_counts = Counter()

    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            try:
                data = json.loads(line)
                as_path = data['entries'][0]['path_attributes'][1]['as_paths'][0]['asns']
                asns.update(as_path)
                originating_asn = as_path[-1]
                # transit_origin_asns.update(as_path[:-1])
                transit_origin_asns.update(ASn for ASn in as_path if ASn != originating_asn)
                originating_asns.add(originating_asn)
                prefix_counts[originating_asn] += 1
                
                num_ips = ipaddress.ip_network(data['prefix']['prefix']).num_addresses
                ip_counts[originating_asn] += num_ips
                for asn in as_path:
                    transit_ip_counts[asn] += num_ips
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    transit_asns = asns - originating_asns
    top_10_prefix_asns = prefix_counts.most_common(10)
    top_10_prefix_asns = [(as_names.get(asn, 'Unknown'), count) for asn, count in top_10_prefix_asns]
    top_10_ip_asns = ip_counts.most_common(10)
    top_10_ip_asns = [(as_names.get(asn, 'Unknown'), count) for asn, count in top_10_ip_asns]
    top_15_transit_ip_asns = transit_ip_counts.most_common(15)
    top_15_transit_ip_asns = [(as_names.get(asn, 'Unknown'), count) for asn, count in top_15_transit_ip_asns]
    
    last_mile_asns = originating_asns - transit_origin_asns
    last_mile_prefix_counts = {asn: prefix_counts[asn] for asn in last_mile_asns}
    last_mile_ip_counts = {asn: ip_counts[asn] for asn in last_mile_asns}
    top_10_last_mile_prefix_asns = sorted(last_mile_prefix_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_10_last_mile_prefix_asns = [((as_names.get(asn, 'Unknown'), asn), count) for asn, count in top_10_last_mile_prefix_asns]
    top_10_last_mile_ip_asns = sorted(last_mile_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_10_last_mile_ip_asns = [((as_names.get(asn, 'Unknown'), asn), count) for asn, count in top_10_last_mile_ip_asns]

    return len(asns), len(originating_asns), len(transit_asns), top_10_prefix_asns, top_10_ip_asns, top_15_transit_ip_asns, len(last_mile_asns), top_10_last_mile_prefix_asns, top_10_last_mile_ip_asns

def question3_3_5():
    
    as_names_file_path = 'as_names.json'
    as_names = load_as_names(as_names_file_path)
    
    file_path = 'table.json'
    total_asns, originating_asns, transit_asns, top_10_prefix_asns, top_10_ip_asns, top_15_transit_ip_asns, total_last_mile, top_10_last_mile_prefix_asns, top_10_last_mile_ip_asns = analyze_asns(file_path, as_names)

    print(f"Total ASNs: {total_asns}\n")
    print(f"Originating ASNs: {originating_asns}\n")
    print(f"Transit ASNs with not originate routes: {transit_asns}\n")
    print(f"Top 10 ASNs by prefix count: {top_10_prefix_asns}\n")
    print(f"Top 10 ASNs by IP count: {top_10_ip_asns}\n")
    print(f"Top 15 ASNs by transit IP count: {top_15_transit_ip_asns}\n")
    print(f"Total last mile ASNs: {total_last_mile}\n")
    print(f"Top 10 last mile ASNs by prefix count: {top_10_last_mile_prefix_asns}\n")
    print(f"Top 10 last mile ASNs by IP count: {top_10_last_mile_ip_asns}\n")

def count_peers(file_path):
    peer_counts_dic = defaultdict(set)

    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            try:
                data = json.loads(line)
                as_path = data['entries'][0]['path_attributes'][1]['as_paths'][0]['asns']
                for i, asn in enumerate(as_path):
                    if i < len(as_path) - 1:
                        peer_counts_dic[asn].add(as_path[i + 1])
                        peer_counts_dic[as_path[i + 1]].add(asn)
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON
    peer_counts = Counter()
    for asn, peers in peer_counts_dic.items():
        peer_counts[asn] = len(peers)
    return peer_counts

def question3_6():
    as_names_file_path = 'as_names.json'
    as_names = load_as_names(as_names_file_path)
    
    file_path = 'table.json'
    peer_counts = count_peers(file_path)
    top_10_most_connected_asns = peer_counts.most_common(10)
    top_10_most_connected_asns = [((as_names.get(asn, 'Unknown'), asn), count) for asn, count in top_10_most_connected_asns]
    print(f"Top 10 most connected ASNs: {top_10_most_connected_asns}")

def build_graph(file_path):
    G = nx.Graph()
    total_lines = sum(1 for _ in open(file_path, 'r'))  # Count total lines for progress bar

    with open(file_path, 'r') as file:
        next(file)  # Skip the first line
        for line in tqdm(file, total=total_lines - 1):  # Adjust total count
            try:
                data = json.loads(line)
                as_path = data['entries'][0]['path_attributes'][1]['as_paths'][0]['asns']
                for i in range(len(as_path) - 1):
                    G.add_edge(as_path[i], as_path[i + 1])
            except json.JSONDecodeError:
                continue  # Skip lines that are not valid JSON

    return G


# def compute_best_connected_asns(G):
#     path_lengths = nx.all_pairs_shortest_path_length(G)
#     avg_path_lengths = {asn: sum(lengths.values()) / len(lengths) for asn, lengths in path_lengths}
#     best_connected_asns = sorted(avg_path_lengths, key=avg_path_lengths.get)[:10]
def compute_best_connected_asns(G):
    avg_path_lengths = {}
    nodes = list(G.nodes())
    for node in tqdm(nodes, desc="Computing shortest paths"):
        lengths = nx.single_source_shortest_path_length(G, node)
        avg_path_lengths[node] = sum(lengths.values()) / len(lengths)
    best_connected_asns = sorted(avg_path_lengths, key=avg_path_lengths.get)[:10]

    return best_connected_asns

    return best_connected_asns
def question3_7():
    file_path = 'table.json'
    G = build_graph(file_path)
    best_connected_asns = compute_best_connected_asns(G)
    print(f"Best connected ASNs: {best_connected_asns}")
    
if __name__ == '__main__':
    # question1()
    # question_3()
    # question3_3_5()
    # question3_6()
    question3_7()
    

