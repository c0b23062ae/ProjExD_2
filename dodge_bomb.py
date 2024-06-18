import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }
KK_IMG = {  # 移動量合計値辞書
    (-5, 0): (0, 0),        # 左
    (-5, -5): (-45, 0),     # 左上
    (-5, +5): (45, 0),      # 左下

    (0, -5): (90, 1),       # 上
    (+5, -5): (45, 1),      # 右上
    (+5, 0): (0, 1),        # 右
    (+5, +5): (-45, 1),     # 右下
    (0, +5): (-90, 1),      # 下
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数： こうかとんRectかばくだんRect
    戻り値： タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTure, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:   # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


#def rotozoom(sum):
#    """
#    引数： こうかとんの移動量の合計値sum_mv[]
#    戻り値： タプル（回転角度）
#    引数と一致するキーの値を返す
#    """
#    for k, v in KK_IMG.items():
#        if list(KK_IMG[k]) == sum:  # KK_IMGとsumが一致していたら
#            return KK_IMG.get(k)  # KK_IMGのvalueを返す


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))   # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)   # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    angle = 0
    black = pg.Surface((WIDTH, HEIGHT))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            # 全画面黒
            pg.draw.rect(black, (0, 0, 0), (WIDTH, HEIGHT))
            # 半透明にする
            screen.blit(black)
            return # ゲームオーバー
        screen.blit(bg_img, [0, 0])             # 背景画像を貼り付ける

        key_lst = pg.key.get_pressed()          # 押されてるキーを取得
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_rct.move_ip(sum_mv)          
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        # angle = rotozoom(sum_mv)[0]
        #if rotozoom(sum_mv)[1] == 1:
        #    kk_img = pg.transform.flip(kk_img, True, False)
        if sum_mv == [-5, 0]:
            angle = 0        # 左
        if sum_mv == [-5, -5]:
            angle = -45    # 左上
        if sum_mv == [-5, +5]:
            angle = 45      # 左下

        if sum_mv == [0, -5]:
            angle = -90     # 上
        if sum_mv == [+5, -5]:
            angle = -135    # 右上
        if sum_mv == [+5, 0]:
            angle = 180      # 右
        if sum_mv == [+5, +5]:
            angle = 135     # 右下
        if sum_mv == [0, +5]:
            angle = 90       # 下
        img = pg.transform.rotozoom(kk_img, angle, 1)
        #kk_img = pg.transform.flip(kk_img, True, False)
        screen.blit(img, kk_rct)

        bb_rct.move_ip(vx, vy)   
        yoko, tate = check_bound(bb_rct)
        if not yoko:    # 横方向にはみ出たら
            vx *= -1
        if not tate:    # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        #kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
