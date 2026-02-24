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