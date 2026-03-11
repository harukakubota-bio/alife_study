from scl_utils import *

def production(particles, x, y, probability):
    p = particles[x,y]
    # 対象の近傍粒子２つをランダムに選ぶ
    n0_x, n0_y, n1_x, n1_y = get_random_2_moore_neighborhood(x, y, particles.shape[0])
    n0_p = particles[n0_x, n0_y]
    n1_p = particles[n1_x, n1_y]
    #この直下のif節では書かれている3つの条件のうち一つでも当てはまってしまったら、関数を返すガード節と呼ばれるもの
    #結局このif節を通り抜けられるのは「自分が触媒かつ、選んだ二人の隣人が基質であるもの」のみ
    if p['type'] != 'CATALYST' or n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        n0_p['type'] = 'HOLE'
        n1_p['type'] = 'LINK'


def disintegration(particles, x, y, probability):
    p = particles[x,y]
    # disintegrationはすぐに起こらない場合もあるので、一旦フラグを立てる
    #元の材料である2つのsubstanceに戻るためには自分がいるマスに加えてもう一つ空きます(HOLE)が必要
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        p['disintegrating_flag'] = True

    if not p['disintegrating_flag']:
        return
    # LINKがSUBSTRATEを含む場合には、強制的に放出するためにemissionを確率１で実行
    emission(particles, x, y, 1.0)
    # 対象の近傍粒子をランダムに選ぶ
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        # LINKの相互結合をすべて消すため、bond_decayを確率１で実行する
        bond_decay(particles, x, y, 1.0)
        # disintegration
        p['type']   = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating_flag'] = False


def bonding(particles, x, y,
            chain_initiate_probability, chain_splice_probability, chain_extend_probability,
            chain_inhibit_bond_flag=True, catalyst_inhibit_bond_flag=True):
    p = particles[x,y]
    # 対象の近傍粒子をランダムに選ぶ
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    # ２つの分子のタイプ・結合の数・角度・交差をチェック
    n_p = particles[n_x, n_y]
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if not n_p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if (n_x, n_y) in p['bonds']:
        return
    if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2: #どちらかがすでに2つの結合をもっている場合
        return
    #線が交差したり、鋭角になったりしないかのチェック
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y, particles.shape[0])
    if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in particles[an1_x,an1_y]['bonds']:
        return
    # Bondingは以下の２つの場合には起こらない
    # 1) moore近傍に膜のチェーンが存在する場合 (chain_inhibit_bond_flag)(膜同士がくっつき塊になってしまうのを防ぐ)
    # 2) moore近傍に触媒分子が存在する場合 (catalyst_inhibit_bond_flag)(触媒に膜がぴったりついてしまうと身動きが取れず死んでしまう)
    mn_list = get_moore_neighborhood(x, y, particles.shape[0]) + get_moore_neighborhood(n_x, n_y, particles.shape[0])
    if catalyst_inhibit_bond_flag:
        for mn_x, mn_y in mn_list: #mn_listには2つ上で取り出した(7,8)(8,9)のような座標が入っており、ここではその座標を取り出している(x座標がmn_xに、y座標がmn_yに)
            if particles[mn_x,mn_y]['type'] is 'CATALYST':
                return
    if chain_inhibit_bond_flag:
        for mn_x, mn_y in mn_list:
            if len(particles[mn_x,mn_y]['bonds']) >= 2:
                if not (x, y) in particles[mn_x,mn_y]['bonds'] and not (n_x, n_y) in particles[mn_x,mn_y]['bonds']:
                    return
    # Bonding
    if len(p['bonds'])==0 and len(n_p['bonds'])==0:
        prob = chain_initiate_probability #両方フリーなら新規作成
    elif len(p['bonds'])==1 and len(n_p['bonds'])==1:
        prob = chain_splice_probability #両方片手空きなら結合(またはループの完成)
    else:
        prob = chain_extend_probability #そうでないなら延長
    if evaluate_probability(prob): #それぞれの確率であたりが出れば、つないでいる相手の座標リストにお互いの座標を加える
        p['bonds'].append((n_x, n_y))
        n_p['bonds'].append((x, y))


def bond_decay(particles, x, y, probability):
    p = particles[x,y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability): #p[〇]という表記はpにある〇というものへのアクセスをする
        for b in p['bonds']: #bは座標として取り出される。(例：(7,8)であればb[0]は7,b[1]は8となる)
            particles[b[0], b[1]]['bonds'].remove((x, y))  #取り出した座標にアクセスし、そこの座標のbondsという引き出しを開ける
        p['bonds'] = []


def absorption(particles, x, y, probability):
    p = particles[x,y]
    # 対象の近傍粒子をランダムに選ぶ
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    #以下の条件を通り抜けられるのはpがLINKであり、かつn_pがSUBSTRATEの場合のみ
    #ここを==とandで記述するとif文の中にif文が入る形となり、何度もインテンドを繰り返さねばならず読みにくくなってしまう
    if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        p['type']   = 'LINK_SUBSTRATE'
        n_p['type'] = 'HOLE'


def emission(particles, x, y, probability):
    p = particles[x,y]
    # 対象の近傍粒子をランダムに選ぶ
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
        return
    if evaluate_probability(probability):
        p['type']   = 'LINK'
        n_p['type'] = 'SUBSTRATE'
