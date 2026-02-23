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
next_state = np.zeros(SPACE_SIZE, dtype=np.int8) #stateの次の世代がnext_state

#最初の状態を初期化
###ランダム###
state[:] = np.random.randint(2, size=len(state))
### 中央の1ピクセルのみ1, あとは0(最初の1マス) ###
state[len(state)//2] = 1  
while visualizer:  #ウィンドウが開いている限りずっと続く
#stateから計算した次の結果をnext_stateの保存
    for i in range(SPACE_SIZE): #左端(0)から右端(599)まで
    #left, center, right cellの状態を取得(隣のセルを確認)
        l = state[i-1]
        c = state[i]
        r = state[(i+1)%SPACE_SIZE] #右端の次は左端へつながるように設定
        neighbor_cell_code = 2**2 *l + 2**1 * c + 2**0 * r #マスの数字を2進数とみなしそれを1つの数字(0~7)へと変換
        if (RULE >> neighbor_cell_code) &1: #ルールの番号から次の数字が0か1を判断
            next_state[i] = 1
        else:
            next_state[i] = 0   

#最後に入れ替え
    state, next_state = next_state, state
    visualizer.update(1-state)
