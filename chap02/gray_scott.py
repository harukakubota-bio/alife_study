import sys, os
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

visualizer = MatrixVisualizer() #visualizerの初期化

SPACE_GRID_SIZE =256 #シミュレーション空間の縦・横のグリッド数
dx = 0.01 #空間のグリッド1メモリ当たりのモデルの長さ
dt = 1 #シミュレーション1ステップごとのモデル内の時間の変化量
VISUALIZATION_STEP = 8 #アニメーションを何ステップごとに描画するのか

#Gray-scottモデルのパラメータの設定
Du = 2e-5
Dv = 1e-5
f, k = 0.022, 0.051 #stripe
#f, k = 0.04, 0.06 # amorphous
#f, k = 0.035, 0.065 # spots
#f, K = 0.012, 0.05 # wandering bubbles
#f, k = 0.025, 0.05 # waves

#初期化
u = np.ones((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
v = np.zeros((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
#中央に初期パターンとしてu=0.5,v=0.25のSQUARE_SIZE四方の正方形の領域を作る
SQUARE_SIZE = 20 
u[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE] = 0.5
v[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE] = 0.25

#対象性を崩すために、少しノイズを入れる(ただし振れ幅が0~1だと大きすぎるので0.1をかける)
u += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE)*0.1
v += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE)*0.1

while visualizer:
      visualizer.update(u) #行列uだけを使用し絵を描く

      for i in range(VISUALIZATION_STEP):
            #ラプラシアンの計算
            laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                           np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4*u) / (dx*dx)
            laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) +
                           np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4*v) / (dx*dx)
            #Gray_scottモデル方程式
            dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
            dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
            u += dt*dudt
            v += dt*dvdt
            #表示をアップデート
      visualizer.update(u)