import sys, os
sys.path.append(os.pardir)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from alifebook_lib.visualizers import ArrayVisualizer

visualizer = ArrayVisualizer() #Visualizerの初期化

SPACE_SIZE = 600
RULE = 30 #CAのバイナリコーディングされたルール
#CAの状態空間
state = np.zeros(SPACE_SIZE, dtype=np.int8) #最小サイズの箱を用意し、メモリの節約
next_state = np.zeros(SPACE_SIZE, dtype=np.int8)

#最初の状態を初期化
###ランダム###
# state[:] = np.random(2, size=len(state))
### 中央の1ピクセルのみ1, あとは0 ###
state[len(state)//2] = 1
while visualizer: 
#stateから計算した次の結果をnext_stateの保存
    for i in range(SPACE_SIZE):
    #left, center, right cellの状態を取得
        l = state[i-1]
        c = state[i]
        r = state[(i+1)%SPACE_SIZE]
        neighbor_cell_code = 2**2 *l + 2**1 * c + 2**0 * r 
        if (RULE >> neighbor_cell_code) &1:
            next_state[i] = 1
        else:
            next_state[i] = 0   

#最後に入れ替え
    state, next_state = next_state, state
    visualizer.update(1-state)
