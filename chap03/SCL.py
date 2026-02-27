import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from alifebook_lib.visualizers import SCLVisualizer
from scl_interaction_functions import *

#visualizernの初期化
visualizers = SCLVisualizer()

SPACE_SIZE = 16

# 初期化設定に関するパラメタ
INITIAL_SUBSTRATE_DENSITY = 0.8
INITIAL_CATALYST_POSITIONS = [(8,8)]
INITIAL_BONDED_LINK_POSITIONS = [
    (5,6,6,5),    (6,5,7,5),   (7,5,8,5),  (8,5,9,5),  (9,5,10,5),
    (10,5,11,6),  (11,6,11,7), (11,7,11,8),(11,8,11,9),(11,9,11,10),
    (11,10,10,11),(10,11,9,11),(9,11,8,11),(8,11,7,11),(7,11,6,11),
    (6,11,5,10),  (5,10,5,9),  (5,9,5,8),  (5,8,5,7),  (5,7,5,6)]

#モデルのパラメーター
MOBILITy_FACTOR = {
    "HOLE":           0.1,
    "SUBSTRATE":      0.1,
    "CATALYST":       0.0001,
    "LINK":           0.05,
    "LINK_SUBSTANCE": 0.05,
}
PRODUCTION_PROBABILITY             = 0.95
DISINTEGRATION_PROBABILITY         = 0.0005
BONDING_CHAIN_INITIATE_PROBABILITY = 0.1
BONDING_CHAIN_EXTEND_PROBABILITY   = 0.6
BONDING_CHAIN_SPLICE_PROBABILITY   = 0.9
BOND_DECAY_PROBABILITY             = 0.0005
ABSORPTION_PROBABILITY             = 0.5
EMISSION_PROBABILITY               = 0.5


#初期化
particles = np.empty((SPACE_SIZE, SPACE_SIZE), dtype=object) #dtype=objectはオブジェクトの型全般を格納できる
#INITIAL_SUBSTANCE_DENSITYに従い、SUBSTANCEとHOLEを配置する
#80%の確率でSUBSTRATE(基質)を配置し、その他はHOLE(何もなし)を配置する
for x in range(SPACE_SIZE):
    for y in range(SPACE_SIZE):
        if evaluate_probability(INITIAL_SUBSTRATE_DENSITY):
            p = {"type":"SUBSTRATE", "disintegrating_flag": False, "bonds": []}
        else:
            p = {"type":"HOLE", "disintegrating_flag":False, "bonds": []}
        particles[x,y] = p

#INITIAL_CATALYST_POSITIONS(今回はど真ん中(8,8))にCATALYSTを配置する
for x, y in INITIAL_CATALYST_POSITIONS:
      particles[x, y]["type"] = "CATALYST"


#膜がない状態からのスタート
#for x0, y0, x1, y1 in INITIAL_BONDED_LINK_POSITIONS:
    #particles[x0, y0]["type"] = "LINK"
    #particles[x0, y0]["bonds"].append((x1, y1))
    #particles[x1, y1]["bonds"].append((x0, y0))