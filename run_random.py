from multiprocessing import Pool
import os
from random import randint
from time import sleep

def run(cmd):
    print(cmd)
    os.system(cmd)

if __name__ == "__main__":
    all_cmd = [
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_evrp_wcci --algo=HGS --max-count=1",
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_evrp_wcci --algo=VNS --max-count=1",
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_cvrp --algo=HGS --round-int --max-count=1",
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_cvrp --algo=VNS --round-int --max-count=1",
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_dimacs --algo=HGS --max-count=1",
        # "python -u evaluate.py --seed=1 --data-folder=dataset/train/data_dimacs --algo=VNS --max-count=1",

        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N500 --algo=HGS --max-count=1",
        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N1000 --algo=HGS --max-count=1",
        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N2000 --algo=HGS --max-count=1",

        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N500 --algo=VNS --max-count=1",
        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N1000 --algo=VNS --max-count=1",
        "python -u evaluate.py --seed=1 --data-folder=dataset/test/uniform_N2000 --algo=VNS --max-count=1",

        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Antwerp --algo=HGS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Leuven --algo=HGS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Ghent --algo=HGS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Brussels --algo=HGS --max-count=1 --min-extend-nodes=1024",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Flanders --algo=HGS --max-count=1 --min-extend-nodes=1024",

        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Antwerp --algo=VNS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Leuven --algo=VNS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Ghent --algo=VNS --max-count=1 --min-extend-nodes=512",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Brussels --algo=VNS --max-count=1 --min-extend-nodes=1024",
        "python -u evaluate.py --seed=1 --data-folder=dataset/train/realworld/Flanders --algo=VNS --max-count=1 --min-extend-nodes=1024",
    ]

    folders = set([cmd.split("--data-folder=")[1].split(" --max-count")[0] for cmd in all_cmd])

    # for folder in folders:
    #     run(f"python -u init_solution.py --data-folder={folder}")

    # with Pool(3) as p:
    #     p.map(run, all_cmd)
    for cmd in all_cmd:
        run(cmd + " --n-envs=16")