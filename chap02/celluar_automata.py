import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import ArrayVisualizer

visualizer = ArrayVisualizer() #Visualizerの初期化

SPACE_SIZE = 600
RULE = 30 #CAのバイナリコーディングされたルール
#CAの状態空間
state = np.zeros(SPACE_SIZE, dtype=np.int8)
next_state = np.zeros(SPACE_SIZE, dtype=np.int8)

#最初の状態を初期化
###ランダム###
# state[:] = np.random(2, size=len(state))
### 中央の1ピクセルのみ1, あとは0 ###
state[len(state)//2] = 1
