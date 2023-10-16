from tkinter import *
from tkinter import messagebox as msgbox
from random import randint as rnd

vertical = 20     #基盤の縦のマス数
side = 10     #基盤の横のマス数
size = 30     #1マスの大きさ
mino_size = 4    #ミノの(縦横最大の)ブロック数
NEXTCOUNT = 4   #保持するミノの数
form = 0    #ミノの種類
next_form = [form for i in range(NEXTCOUNT)]
mode = 0    #ミノの向き
y = -1     #ミノのy座標
x = 4     #ミノのx座標
speed = 0     #落下速度
index = 0   #ゲーム進行
score = 0   #スコア
lv = 1  #レベル
mouse_x = 0
mouse_y = 0
mouse_c = 0
#色の定義
colors = ["#00ffff", #I:0
          "#0000ff", #J:1
          "#ffa500", #L:2
          "#ffff00", #O:3
          "#008000", #S:4
          "#800080", #T:5
          "#ff0000", #Z:6
          "#404040"] #foundation:7
y_data = [0, 0, 0, 0]
x_data = [0, 0, 0, 0]
foundation_data = [7, 7, 7, 7]
foundation = [[0 for i in range(side + 2)] for j in range(vertical + 2)] 

mino_data = [[[[2, 0], [2, 1], [2, 2], [2, 3]],     #I:0,0度
              [[0, 1], [1, 1], [2, 1], [3, 1]],     #右に90度回転後
              [[1, 0], [1, 1], [1, 2], [1, 3]],     #右に180度回転後
              [[0, 2], [1, 2], [2, 2], [3, 2]]],    #右に270度回転後
             [[[1, 0], [2, 0], [2, 1], [2, 2]],     #J:1
              [[1, 1], [1, 2], [2, 1], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 2]],
              [[1, 1], [2, 1], [3, 0], [3, 1]]],
             [[[1, 2], [2, 0], [2, 1], [2, 2]],     #L:2
              [[1, 1], [2, 1], [3, 1], [3, 2]],
              [[2, 0], [2, 1], [2, 2], [3, 0]],
              [[1, 0], [1, 1], [2, 1], [3, 1]]],
             [[[1, 1], [1, 2], [2, 1], [2, 2]],     #O:3
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]]],
             [[[1, 1], [1, 2], [2, 0], [2, 1]],     #S:4
              [[1, 1], [2, 1], [2, 2], [3, 2]],
              [[2, 1], [2, 2], [3, 0], [3, 1]],
              [[1, 0], [2, 0], [2, 1], [3, 1]]],
             [[[1, 1], [2, 0], [2, 1], [2, 2]],     #T:5
              [[1, 1], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 1]],
              [[1, 1], [2, 0], [2, 1], [3, 1]]],
             [[[1, 0], [1, 1], [2, 1], [2, 2]],     #Z:6
              [[1, 2], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [3, 1], [3, 2]],
              [[1, 1], [2, 0], [2, 1], [3, 0]]]]
mino = [[7 for i in range(mino_size)] for j in range(mino_size)]
next_mino = [mino for i in range(NEXTCOUNT)]
class Move_mino:
    def __init__(self, next_y, next_x, next_mode):
        self.next_y = next_y
        self.next_x = next_x
        self.next_mode = next_mode

    def reference(self): #動作後の基盤データを抽出する
        global x_data, y_data, foundation_data
        for i in range(len(mino_data[next_form[0]][mode % 4])):
            y_data[i] = mino_data[next_form[0]][(mode + self.next_mode) % 4][i][0] + y
            x_data[i] = mino_data[next_form[0]][(mode + self.next_mode) % 4][i][1] + x
            foundation_data[i] = foundation[y_data[i] + self.next_y][x_data[i] + self.next_x]

    def move_mino(self, e): #抽出した基盤データを基に次のマスにブロックがなければ移動する
        global x, y, foundation, mode
        self.reference()
        if foundation_data == [7, 7, 7, 7]:
            y += 1 * self.next_y
            x += 1 * self.next_x
        if self.next_y == 1 and foundation_data != [7, 7, 7, 7]:
            for i in range(len(y_data)):
                foundation[y_data[i]][x_data[i]] = next_form[0]
            sc = delete()
            calculate_score(sc)
            game_over()
            mode = 0
            y = -1
            x = 4
            next_mino[0] = [[7 for i in range(mino_size)] for j in range(mino_size)]
            create_mino()
            next_minoset()
        cv.delete("all")     #キャンバス描画の消去
        draw_foundation()
        draw_mino()
        draw_info()

    def drop_mino(self):
        global speed,lv
        speed += 1
        if speed == 11-lv:
            self.move_mino(Event)
            speed = 0

    def spin_mino(self, e):
        self.reference()
        global mode
        if foundation_data == [7, 7, 7, 7]:
            mode += 1 * self.next_mode
            next_mino[0] = [[7 for i in range(mino_size)] for j in range(mino_size)]
            for i in range(len(mino_data[next_form[0]][mode % 4])):
                y = mino_data[next_form[0]][mode % 4][i][0]
                x = mino_data[next_form[0]][mode % 4][i][1]
                next_mino[0][y][x] = next_form[0]
            cv.delete("all")
            draw_foundation()
            draw_mino()
            draw_info()

def draw_foundation():      #基盤の描画
    for v in range(vertical):
        v1 = v * size       #1マス当たりの上辺の位置
        v2 = v1 + size      #１マス当たりの下辺の位置
        for s in range(side):
            s1 = s * size       #１マス当たりの左辺の位置
            s2 = s1 + size      #１マス当たりの右辺の位置
            for c in range(len(colors)):
                if foundation[v + 1][s + 1] == c:
                    color = colors[c]
                    cv.create_rectangle(s1, v1, s2, v2, fill=color)     #四角形を描画

def create_mino():      #ミノの作成
    global form, mino
    form = rnd(0, 6)
    for i in range(len(mino_data[form][mode % 4])):
        y = mino_data[form][mode % 4][i][0]     #4x4マスにおけるy軸座標
        x = mino_data[form][mode % 4][i][1]     #4x4マスにおけるx軸座標
        mino[y][x] = form

def draw_mino():    #ミノのマスがformと一致していれば描画する
    for v in range(mino_size):
        v1 = (v + y - 1) * size
        v2 = v1 + size
        for s in range(mino_size):
            s1 = (s + x - 1) * size
            s2 = s1 + size
            if next_mino[0][v][s] == next_form[0]:
                cv.create_rectangle(s1, v1, s2, v2, fill = colors[next_form[0]])

def next_minoset():    #次以降のミノの保持
    global mino, form
    for i in range(NEXTCOUNT-1):
        next_mino[i] = next_mino[i+1]
        next_form[i] = next_form[i+1]
    next_mino[NEXTCOUNT-1] = mino
    next_form[NEXTCOUNT-1] = form
    mino = [[7 for i in range(mino_size)] for j in range(mino_size)]

def draw_info():   #プレイ画面外の描画
    draw_txt("SCORE", 450, 430, 25, "black", "INFO")
    draw_txt(score, 450, 460, 25, "black", "INFO")
    draw_txt("LEVEL", 450,490, 25, "black", "INFO")
    draw_txt(lv, 450, 520, 25, "black", "INFO")
    for i in range(1,NEXTCOUNT):
        cv.create_rectangle(310, -50 + 120*i, 470, 50 + 120*i, outline="black", width=4)
        draw_txt("NEXT", 350, 30, 20, "black", "INFO")
        draw_txt(i, 320, -38 + 120*i, 20, "black", "INFO")        
        for v in range(1,mino_size-1):
            v1 = (v - 2 + i * 4) * size
            v2 = v1 + size
            for s in range(mino_size):
                s1 = (s + 11) * size
                s2 = s1 + size
                if next_mino[i][v][s] == next_form[i]:
                    cv.create_rectangle(s1, v1, s2, v2, fill = colors[next_form[i]])
                    
def delete():
    sc = 0
    for v in range(len(foundation)):
        if (7 in foundation[v]) == False and foundation[v] != [8 for i in range(side + 2)]:
            del foundation[v]
            add_foundation = [7 for i in range(side + 2)]
            add_foundation[0], add_foundation[side + 1] = 8, 8
            foundation.insert(0, add_foundation)
            sc += 1
    return sc

def calculate_score(sc):
    global score, lv
    score += sc*sc*lv*100
    if score > 100000:
        lv = 10
    elif score > 80000:
        lv = 9
    elif score > 65000:
        lv = 8
    elif score > 50000:
        lv = 7
    elif score > 35000:
        lv = 6
    elif score > 20000:
        lv = 5
    elif score > 10000:
        lv = 4
    elif score > 5000:
        lv = 3
    elif score > 2000:
        lv = 2

def game_over():
    global index
    top_foundation = [7 for i in range(side + 2)]
    top_foundation[0], top_foundation[side + 1] = 8, 8
    if foundation[1] != top_foundation:
        msgbox.showinfo(message = "Game Over")     #メッセージの表示
        index = 0
    

def draw_txt(txt,x,y,siz,col,tg):   #影付き文字列を表示する関数
    fnt = ("Times New Roman", siz, "bold")
    cv.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

def mouse_press(e):
    global mouse_c
    mouse_c = 1

def main():
    global win, cv, foundation, index, score, lv, mouse_x, mouse_y, mouse_c
    if index == 0: #タイトルロゴ
        cv.delete("all")
        cv.create_image(300,300, image=img)
        draw_txt("T○TR○S", 300, 200, 50, "red", "TITLE")
        draw_txt("Click to start.", 300, 350, 25, "green", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1:    #タイトル画面　スタート待ち
        if mouse_c == 1:
            foundation = [[7 for i in range(side + 2)] for j in range(vertical + 2)]    #基盤の作成，何もないマスは7
            for i in range(vertical + 2):
                foundation[i][0], foundation[i][side + 1] = 8, 8    #外側の壁は8
            foundation[vertical + 1] = [8 for i in range(side + 2)]     #底の壁は8
            mouse_c = 0
            score = 0
            lv = 1
            cv.delete("TITLE")
            index = 2
    elif index == 2:
        cv.delete("all")
        for i in range(NEXTCOUNT):
            create_mino()
            next_minoset()
        draw_foundation()
        draw_mino()
        index = 3
    elif index == 3:
        left = Move_mino(0, -1, 0)
        right = Move_mino(0, 1, 0)
        under = Move_mino(1, 0, 0)
        left_spin = Move_mino(0, 0, -1)
        right_spin = Move_mino(0, 0, 1)

        win.bind("<Left>", left.move_mino)     #左キーが押されたら左に移動
        win.bind("<Right>", right.move_mino)     #右キーが押されたら右に移動
        win.bind("<Return>", under.move_mino)     #エンターキーが押されたら下に移動
        win.bind("<Up>", right_spin.spin_mino)     #上キーが押されたら右回転
        win.bind("<Down>", left_spin.spin_mino)     #下キーが押されたら左回転
        under.drop_mino()
    win.after(100,main)
win = Tk()     #ウィンドウの作成
win.title("T○TR○S")
win.resizable(False, False)
win.bind("<Motion>", mouse_move)
win.bind("<ButtonPress>", mouse_press)
cv = Canvas(win, width=600, height=vertical * size)     #キャンバスの作成
img = PhotoImage(file="title_bg_img.png")
cv.pack()    #オブジェクト配置のオプション
main()
win.mainloop()
