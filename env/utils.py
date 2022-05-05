import colorsys
from functools import lru_cache
import math
import os
import pickle
import re
from joblib import Memory
from matplotlib import cm, colors as mc
import numpy as np
import torch
import random


memory = Memory('__pycache__', verbose=0)


def read_number(s, mode=int):
    try:
        return mode(s)
    except:
        return read_number(s, float) if mode == int else s

@lru_cache
def distance_between(a_x, a_y, b_x, b_y):
    xd = a_x - b_x
    yd = a_y - b_y
    return math.sqrt(xd * xd + yd * yd)

@lru_cache
def angle_between(a_x, a_y, b_x, b_y):
    return math.atan2(b_y - a_y, b_x - a_x)

@memory.cache
def read_instance(path):
    data = {}
    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                data[parts[0].strip()] = read_number(parts[1].strip())
            else:
                parts = line.split()
                parts = [read_number(part) for part in parts]
                if parts[0] == "NODE_COORD_SECTION":
                    data['NODE_COORD_SECTION'] = []
                elif parts[0] == "DEMAND_SECTION":
                    data['DEMAND_SECTION'] = []
                elif parts[0] == "STATIONS_COORD_SECTION":
                    data['STATIONS_COORD_SECTION'] = []
                elif parts[0] == "DEPOT_SECTION":
                    data['DEPOT'] = 1
                    break
                elif len(parts) == 3:
                    data['NODE_COORD_SECTION'].append(parts)
                elif len(parts) == 2:
                    data['DEMAND_SECTION'].append(parts)
                elif len(parts) == 1:
                    data['STATIONS_COORD_SECTION'].append(parts[0])
    return data

def find_next_id(instance, solution, demand, energy, consumption, check=True):
    prev_node = instance.nodes[solution[-1]]
    distances = {}
    for node in instance.demands:
        if node.id in solution:
            continue
        distance = node.distance_to(prev_node)
        if 0 < distance*consumption <= energy and node.demand <= demand:
            if check:
                next_keys = find_next_id(instance, solution + [node.id], demand-node.demand, energy-distance*consumption, consumption, False)
            if not check or len(next_keys) > 0:
                distances[node.id] = distance
    keys = list(distances.keys())
    if len(keys) == 0 and prev_node.is_demand:
        for node in instance.depots + instance.stations:
            distance = node.distance_to(prev_node)
            if 0 < distance*consumption <= energy:
                distances[node.id] = distance
    keys = list(distances.keys())
    if len(keys) > 0:
        keys.sort(key=lambda x: distances[x])
    return keys

@memory.cache(ignore=["instance"])
def generate_init_tours(instance, name, init_mode='clockhand', round_int=False):
    from .InitSolution import InitClockHand
    print(f"Running initial solution: {name}")
    if init_mode == 'clockhand':
        init = InitClockHand.from_instance(instance, round_int)
        solution, score = init.init_solution()
    elif init_mode == 'dbca':
        solution = instance.make_env('VNS').init_solution()
        score = instance.evaluation(solution)
    elif init_mode == 'default':
        solution = instance.make_env().init_solution()
        if instance.mode == "EVRP" and instance.args.algo != "VNS":
            vrp_repairer = instance.make_env("VNS")
            vrp_repairer.step(solution)
            solution = vrp_repairer.get_best_solution()
        score = instance.evaluation(solution)
    print(f"Init completed! Instance {name}: {score:.3f}")
    return solution

def angle_comparator(nodes):
    node_points = [[node.x, node.y] for node in nodes][:-1]
    depot = node_points[0]
    center = np.mean(node_points, 0)
    angle = angle_between(depot[0], depot[1], center[0], center[1])
    return angle

def sort_tours_by_center(tours):
    tours = sorted(tours, key=lambda nodes: angle_comparator(nodes))
    return tours

def convert_solution_to_tours(nodes, solution):
    tours = []
    tour = []
    for node_id in solution:
        node = nodes[node_id]
        tour.append(node)
        if node.is_depot:
            if len(tour) > 1:
                tours.append(tour)
            tour = [node]
    tours = sort_tours_by_center(tours)
    return tours

def plot_solution(nodes, tours, name=None, score=None):
    import plotly.graph_objects as go
    import plotly.io as pio
    try:
        pio.kaleido.scope.mathjax = None
    except:
        pass

    fig = go.Figure()
    title = f"{name}"
    if score is not None:
        title = f"{name} - {score:.3f}"
    fig.update_layout(title_text=title, title_x=0.5)
    station_x, station_y = [], []
    for node in nodes:
        if node.is_depot:
            depot = node
        elif node.is_station:
            station_x.append(node.x)
            station_y.append(node.y)
    if len(station_x) > 1:
        fig.add_trace(go.Scatter(x=station_x, y=station_y, mode='markers', name="station", marker_color="black", marker_size=6, marker_symbol="square"))
    color_ids = np.linspace(0, 1, max(len(tours), 8))
    colors = cm.gist_rainbow(color_ids)
    for k, tour in enumerate(tours):
        pos_x, pos_y = [], []
        demand_x, demand_y = [], []
        for node in tour:
            pos_x.append(node.x)
            pos_y.append(node.y)
            if node.is_demand:
                demand_x.append(node.x)
                demand_y.append(node.y)
        color = colors[k]
        color_1 = "rgb(" + ",".join(f"{int(x*240)}" for x in color) + ")"
        color[1] = 1 - 0.7*(1-color[1])
        color_2 = "rgb(" + ",".join(f"{int(x*240)}" for x in color) + ")"
        fig.add_trace(go.Scatter(x=pos_x, y=pos_y, mode='lines', name=f"EVRP{k+1}", line_color=color_2, line_width=2))
        fig.add_trace(go.Scatter(x=demand_x, y=demand_y, mode='markers', name=f"EVRP{k+1}", marker_color=color_1, marker_size=3))
    fig.add_trace(go.Scatter(x=[depot.x], y=[depot.y], mode='markers', name="depot", marker_color="red", marker_size=10, marker_symbol="hexagram"))
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(showlegend=False)
    return fig

def lighten_color(color, amount=0.5):
    color = colorsys.rgb_to_hls(*mc.to_rgb(color))
    return colorsys.hls_to_rgb(color[0], 1 - amount * (1 - color[1]), color[2])

def set_seed(seed):
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

def swap_and_flatten(arr):
    shape = arr.shape
    return arr.swapaxes(0, 1).reshape(shape[0] * shape[1], *shape[2:])

def load_scores(path="logs"):
    os.makedirs(path, exist_ok=True)
    if os.path.isfile(f'{path}/best_scores.pkl'):
        with open(f'{path}/best_scores.pkl', 'rb') as f:
            return pickle.load(f)
    return {}

def save_scores(best_scores, path="logs"):
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/best_scores.pkl', 'wb') as f:
        pickle.dump(best_scores, f)

def compare(key):
    items = re.split(r'(\d+)', key)
    items = tuple(read_number(x) for x in items)
    return items
    
def sort_instances(names):
    return sorted(names, key=compare)