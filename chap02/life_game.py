import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer
import game_of_life_patterns

# visualizerの初期化 (Appendix参照)
visualizer = MatrixVisualizer()

WIDTH = 50
HEIGHT = 50

state = np.zeros((HEIGHT,WIDTH), dtype=np.int8)
next_state = np.empty((HEIGHT,WIDTH), dtype=np.int8)

#初期化
###ランダム###
#state = np.random.randint(2, size=(HEIGHT,WIDTH), dtype=np.int8)
pattern = game_of_life_patterns.GLIDER_GUN
state[2:2+pattern.shape[0], 2:2+pattern.shape[1]] = pattern

while visualizer:
   for i in range(HEIGHT):
       for j in range(WIDTH):
           #自分と近傍のセルの状態を取得
           # c : center (自分自身)
           # nw: north west, ne: north east ...
           #iは行、jは列
           #端になった時、もう反対の端を参照できるように幅や高さで割ったあまりを考える必要のあるマスもある
           #[]の中は座標
           nw = state[i-1,j-1]
           n  = state[i-1,j]
           ne = state[i-1,(j+1)%WIDTH]
           w  = state[i,j-1]
           c  = state[i,j]
           e  = state[i,(j+1)%WIDTH]
           sw = state[(i+1)%HEIGHT,j-1]
           s  = state[(i+1)%HEIGHT,j]
           se = state[(i+1)%HEIGHT,(j+1)%WIDTH]
           neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
           
           #自分が死んでいて、周りに3匹生きているものがいるとき→次の世代でcは生
           if c == 0 and neighbor_cell_sum == 3:
               next_state[i,j] = 1
           #自分が生きていて、周りに2または3の生き残りがいるとき→次の世代でもcは生
           elif c == 1 and neighbor_cell_sum in (2,3): #cが1かつ、neighbor_cell_sumが2または3のとき
               next_state[i,j] = 1
           #周りが1つ以下（過疎で死滅）、または4つ以上（過密で死滅）→次の世代でcは死
           else:
               next_state[i,j] = 0
   state,next_state = next_state,state

   visualizer.update(1-state)