import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from alifebook_lib.visualizers import SCLVisualizer
from scl_interaction_functions import *

#visualizernの初期化
visualizer = SCLVisualizer()

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
MOBILITY_FACTOR = {
    "HOLE":           0.1,
    "SUBSTRATE":      0.1,
    "CATALYST":       0.0001,
    "LINK":           0.05,
    "LINK_SUBSTRATE": 0.05,
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

while visualizer:
    #分子の移動
    #前提:SCLモデルでは分子が単独でワープするのではなく、隣のマスと中身をスワップする
    #False: リストの初期値であり全員が動いていない(False)の状態にする, dtype=bool:このリストにはTrueかFalseしか入れない
    moved = np.full(particles.shape, False, dtype=bool)

    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x,y]
            
            #自分の座標(x,y)と空間の大きさをもとにノイマン近傍(上下左右)からランダムに1つ選び出す
            n_x, n_y = get_random_neumann_neighborhood(x, y, SPACE_SIZE) 
            n_p = particles[n_x, n_y]
            #2つの分子が入れ替わる確率を計算
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p["type"]] * MOBILITY_FACTOR[n_p["type"]])
            #分子が移動できるかどうかの4つの条件をチェック
                #1.自分がこのターンでまだ動いていないこと
                #2.入れ替わり相手もこのターンでまだウドいていないこと
                #3.自分も相手も誰とも結合(bond)していないこと
                #4.先ほどの計算した確率でTrueが出たこと
            if not moved[x, y] and not moved[n_x, n_y] and \
               len(p["bonds"]) == 0 and len(n_p["bonds"]) == 0 and \
               evaluate_probability(mobility_factor):
                   #上の4つの条件をクリアしたものは中身が入れ替わる、そして自分と相手の座標をTrueとしこのターンは動かないようにする
                   particles[x, y], particles[n_x, n_y] = n_p, p
                   moved[x, y] = moved[n_x, n_y] = True

    
    #分子の反応
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
             production(particles, x, y, PRODUCTION_PROBABILITY)
             disintegration(particles, x, y, DISINTEGRATION_PROBABILITY)
             #bondingだけは、分子の状態に応じて確率を変えるために3つの確率を与える
             bonding(particles, x, y, BONDING_CHAIN_INITIATE_PROBABILITY,
                                      BONDING_CHAIN_SPLICE_PROBABILITY,
                                      BONDING_CHAIN_EXTEND_PROBABILITY)
             bond_decay(particles, x, y, BOND_DECAY_PROBABILITY)
             absorption(particles, x, y, ABSORPTION_PROBABILITY)
             emission(particles, x, y, EMISSION_PROBABILITY)
    visualizer.update(particles)
