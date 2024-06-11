import tkinter as tk
from tkinter import ttk
from chess import Chess
from config import *
from copy import deepcopy
from os import path
#from PIL import Image, ImageTk
#from threading import Timer

class ChessMain:
    def __init__(self):
        self.chessboard = {}
        self.castle = {}
        self.turn = None
        self.my_turn = None
        self.opp_turn = None
        self.depth = None
        self.previous_position = None
        
        self.undo_list=[]
        self.dead_list=[]
        self.move_data=[]
        self.moved_mark=[]
        self.r_possible_moves=[]
        self.board = None

        self.root = tk.Tk()
        self.root.geometry('660x680')
        self.root.resizable(False, False)
        self.root.title("Chess")
        self.base_dir = path.dirname(path.abspath(__file__))
        self.root.iconphoto(False, tk.PhotoImage(file=path.join(self.base_dir, "static", icon_img)))
        
        #set background image
        self.bgimg = tk.PhotoImage(file=path.join(self.base_dir, "static", background_img))

        self.canvas = tk.Canvas(self.root, width=660 , height=680)
        self.canvas.pack(fill="both", expand=True)
        self.background_image_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.bgimg, tags="background")
        self.root.bind("<Configure>", self.on_configure)
        #canvas1.create_text( 200, 250, text = "Welcome text here") 

        #self.bgimg = ImageTk.PhotoImage(Image.open(background_img))
        #tk.Label(self.mainframe, image=self.bgimg).place(x=0, y=0, relwidth=1, relheight=1)
        self.mainframe = tk.Frame(self.canvas, bg="")
        self.mainframe.pack(side="top", fill="both", expand=True)

        self.gameframe = tk.Frame(self.canvas, bg="")#background_color)
        
        
    def on_configure(self, event):
        # Reapply the background image to the frame
        self.canvas.delete("background")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bgimg, tags="background")


    def dashboardPage(self):
        self.level = tk.IntVar()
        self.level.set(2)
        self.color = tk.StringVar()
        self.color.set('B')
        scaleval = {1:'Normal', 2:'Hard'}
        #scaleval = {1:'Easy', 2:'Medium', 3:'Hard'}
                
        self.formframe = tk.Frame(self.mainframe, border=2, relief="solid")
        self.formframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.formframe, text="\nSelect Color:", fg="Black").pack(fill=tk.BOTH, expand=True)
        ttk.Radiobutton(self.formframe, text="Black", variable=self.color, value='B').pack(anchor=tk.S)
        ttk.Radiobutton(self.formframe, text="White", variable=self.color, value='W').pack(anchor=tk.S)

        tk.Label(self.formframe, text="\nSelect Level:", fg="Black").pack(fill=tk.BOTH, expand=True)
        #game lavel selector
        tk.Scale(self.formframe, orient="horizontal", showvalue=0, variable=self.level, from_=1, to_=2, command=\
                 lambda val:leveltext.config(text=scaleval[int(val)])).pack(fill=tk.BOTH, expand=True)
        
        leveltext = tk.Label(self.formframe, text=scaleval[self.level.get()])
        leveltext.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.formframe, text="",).pack(fill=tk.BOTH, expand=True)
        ttk.Button(self.formframe, text="Start Game", command=self.gamePage).pack(fill=tk.BOTH, expand=True)
    
        
    def gamePage(self):
        self.head_frame = tk.Frame(self.gameframe, bg=background_color)
        self.head_frame.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.win_txt = tk.Label(self.head_frame, text=human_turn_msg, font=("Arial",14), width=46, height=1, fg="black")
        self.win_txt.pack()

        self.left_frame = tk.Frame(self.gameframe, bg=background_color, border=2, relief="solid")
        self.left_txt = tk.Label(self.left_frame, text='', font=dead_chess_font, fg="black", width=2, height=18)
        self.left_txt.pack()
        self.left_frame.pack(side=tk.LEFT)
        
        self.board_frame = tk.Frame(self.gameframe, height='660', border=2, relief="solid")
        self.board_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER,)
        
        self.right_frame = tk.Frame(self.gameframe, bg=background_color, border=2, relief="solid")
        self.right_txt = tk.Label(self.right_frame, text='', font=dead_chess_font, fg="black", width=2, height=18)
        self.right_txt.pack()
        self.right_frame.pack(side=tk.RIGHT)

        self.fun_frame = tk.Frame(self.gameframe, bg=background_color)
        self.fun_frame.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        self.undo_btn = tk.Button(self.fun_frame, text='Undo Step', bg='white', relief="groove", font=("Arial",15),command=self.undo_step)
        self.undo_btn.pack(side=tk.LEFT)
        self.reset_btn = tk.Button(self.fun_frame,text='Reset Game', bg='white', relief="groove", font=("Arial",15), command=self.reset_board)
        self.reset_btn.pack(side=tk.LEFT)
        self.home_btn = tk.Button(self.fun_frame, text='Home Page', bg='white', relief="groove", font=("Arial",15), command=self.home_page)
        self.home_btn.pack(side=tk.LEFT)
        
        self.chessboard = Chess.BOARD.copy()
        self.castle = deepcopy(Chess.CASTLE)
        self.board = [[0 for i in range(8)] for j in range(8)]

        self.depth = game_level[self.level.get()]
        self.turn = self.my_turn = self.color.get()
        self.opp_turn = 'W' if self.my_turn == 'B' else 'B'

        arr = [str(i)+str(j) for i in range(0,8,1) for j in range(0,8,1)]
        arr.reverse() if self.my_turn=='W' else arr
        index = 0
        for row in range(8):  
            for col in range(8):
                color = even_color if (row+col)%2==0 else odd_color#d3d3d3
                txt = '' if self.chessboard[arr[index]] == '' else Chess.gui_man[self.chessboard[arr[index]][:2]]     
                self.board[int(arr[index][0])][int(arr[index][1])] = tk.Button(self.board_frame, text=txt, bg=color, borderwidth=0, relief="groove",\
                                font=("Arial",25), width=3, height=1, command=lambda row=int(arr[index][0]),col=int(arr[index][1]):self.make_move(row,col))
                self.board[int(arr[index][0])][int(arr[index][1])].grid(row=row, column= col)
                index += 1

        self.mainframe.pack_forget()
        self.gameframe.pack(side="top", expand=True, fill="both")

    def stop_command(self, txt):
        for i in range(8):    
            for j in range(8):
                self.board[i][j].config(command='')
        self.undo_btn.config(command='')
        self.win_txt.config(text=txt)

    def undo_step(self):
        if len(self.undo_list)>0:
            self.move_data = []
            temp = self.undo_list.pop()
            # self.castle = {}
            # self.dead_list = []
            self.castle = deepcopy(temp[1])
            self.dead_list = temp[2].copy()

            for box,man in temp[0].items():
                i=int(box[0]); j=int(box[1])
                color = even_color if (i+j)%2==0 else odd_color
                txt = Chess.gui_man[man[0:2]] if man!='' else ''
                self.board[i][j].config(text=txt, bg=color)
                self.chessboard[box] = man
            
            self.right_txt.config(text='')
            self.left_txt.config(text='')

            if len(self.dead_list)>0:
                right=""
                left=""
                for dead in self.dead_list:
                    if dead[0] == self.my_turn:
                        right = right + Chess.gui_man[dead[0:2]]
                    else:
                        left = left + Chess.gui_man[dead[0:2]]

                if len(right)>1: right = "\n".join(right)
                if len(left)>1: left = "\n".join(left)
                self.right_txt.config(text=right)
                self.left_txt.config(text=left)

    def reset_board(self):
        self.win_txt.config(text=human_turn_msg)
        self.turn = self.my_turn
        self.previous_position = None
        self.undo_list=[]
        self.dead_list=[]
        self.move_data=[]
        self.moved_mark=[]
        self.r_possible_moves=[]
        self.chessboard = {}
        self.castle = {}
        self.chessboard = Chess.BOARD.copy()
        self.castle = deepcopy(Chess.CASTLE)

        self.left_txt.config(text="")
        self.right_txt.config(text="")        

        for i in range(8):
            for j in range(8):
                color = even_color if (i+j)%2==0 else odd_color
                txt = Chess.gui_man[self.chessboard[str(i)+str(j)][0:2]] if self.chessboard[str(i)+str(j)]!='' else ''
                self.board[i][j].config(text=txt,bg=color,command=lambda row=i,col=j: self.make_move(row,col))


    def home_page(self):
        self.depth = None
        self.turn=None
        self.my_turn=None
        self.opp_turn=None
        self.castle=None
        self.chessboard=None
        self.my_promote_row=None
        self.opp_promote_row=None
        self.previous_position=None
        self.dead_list=[]
        self.undo_list=[]
        self.r_possible_moves=[]
        self.moved_mark=[]
        self.move_data=[]

        self.left_txt.config(text='')
        self.right_txt.config(text='')

        if len(self.gameframe.winfo_children())>0:
            for widget in self.gameframe.winfo_children():
                widget.destroy()

        self.gameframe.pack_forget()
        self.mainframe.pack(side="top", expand=True, fill="both")


    def add_label(self, frame, text):
        if frame.cget("text")=="":
            frame.config(text=text)
        else:
            frame.config(text = frame.cget("text")+ "\n" + text)


    def make_move(self, row, col):
        if self.my_turn==self.turn:
            box_id = str(row)+str(col)
            dead_chessman_id = None
            
            #return previous background color (remove possible move marks)
            if len(self.r_possible_moves)>0:
                for box in self.r_possible_moves:
                    mark_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                    self.board[int(box[0])][int(box[1])].config(bg=mark_color)

            #step 1: if curent box id in possile moves    
            if box_id in self.r_possible_moves:
                self.undo_list.append((self.chessboard.copy(), deepcopy(self.castle), self.dead_list.copy()))
                dead_chessman_id = self.chessboard[box_id] if self.chessboard[box_id] != '' else ''
                chessman_id = self.chessboard[self.previous_position]
                chessman_color = chessman_id[0]
                chessman_short_id = chessman_id[1]
                chessman_name = Chess.gui_man[chessman_id[0:2]]
                
                if row == promote_row[self.my_turn] and chessman_short_id =='S':
                    chessman_id = chessman_id[0]+'Q'+chessman_id[2:]
                    chessman_name = Chess.gui_man[chessman_id[0:2]]
                    chessman_short_id = chessman_id[1]
                    #if we want then we can also add promotiong pawn to dead list 

                #make and remove moved mark
                if len(self.moved_mark)>0:
                    for box in self.moved_mark:
                        mark_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                        self.board[int(box[0])][int(box[1])].config(bg=mark_color)
                    self.moved_mark = []

                self.board[int(self.previous_position[0])][int(self.previous_position[1])].config(text='')
                self.board[row][col].config(text=chessman_name)
                self.board[int(self.previous_position[0])][int(self.previous_position[1])].config(bg=move_color)
                self.board[row][col].config(bg=move_color)
                #self.widget_ids[box_id].color = man_color[cls.my_turn]

                self.moved_mark.append(box_id)
                self.moved_mark.append(self.previous_position)

                if chessman_short_id=='K' and abs(int(self.previous_position[1])-col)==2:
                #castle case
                    if int(self.previous_position[1])-col==2:#left castle
                        self.board[int(self.castle[self.turn]['lep'][0])][int(self.castle[self.turn]['lep'][1])].config(text='')
                        self.board[int(self.castle[self.turn]['lboxes'][0][0])][int(self.castle[self.turn]['lboxes'][0][1])].config(text=Chess.gui_man[self.castle[self.turn]['leid'][0:2]])
                        self.board[int(self.castle[self.turn]['lep'][0])][int(self.castle[self.turn]['lep'][1])].config(bg=move_color)
                        self.board[int(self.castle[self.turn]['lboxes'][0][0])][int(self.castle[self.turn]['lboxes'][0][1])].config(bg=move_color)
                        self.moved_mark.append(self.castle[self.turn]['lep'])
                        self.moved_mark.append(self.castle[self.turn]['lboxes'][0])
                        
                    else:#right castle
                        self.board[int(self.castle[self.turn]['rep'][0])][int(self.castle[self.turn]['rep'][1])].config(text='')
                        self.board[int(self.castle[self.turn]['rboxes'][0][0])][int(self.castle[self.turn]['rboxes'][0][1])].config(text=Chess.gui_man[self.castle[self.turn]['reid'][0:2]])
                        self.board[int(self.castle[self.turn]['rep'][0])][int(self.castle[self.turn]['rep'][1])].config(bg=move_color)
                        self.board[int(self.castle[self.turn]['rboxes'][0][0])][int(self.castle[self.turn]['rboxes'][0][1])].config(bg=move_color)
                        self.moved_mark.append(self.castle[self.turn]['rep'])
                        self.moved_mark.append(self.castle[self.turn]['rboxes'][0])


                if self.chessboard[box_id] != '':    #if killing chessman
                    self.dead_list.append(dead_chessman_id)
                    #append dead piece in left frame (my kill) side
                    self.add_label(self.left_txt, Chess.gui_man[dead_chessman_id[0:2]])

                if len(self.undo_list)>max_undo_step:
                    self.undo_list.pop(0)
                    
                Chess.push(self.turn, self.chessboard, self.castle, self.previous_position, box_id, self.chessboard[self.previous_position])

                temp = Chess.get_both_data(self.turn, self.chessboard, self.castle)
                if temp[1]['kp'] in temp[0]['all_moves']:
                    self.moved_mark.append(temp[1]['kp'])
                    self.board[int(temp[1]['kp'][0])][int(temp[1]['kp'][1])].config(bg=check_color)

                if len(temp[1]['legal_moves'])==0:
                    if Chess.checkmate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                        self.stop_command(human_win_msg)
                        return None

                    elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                        self.stop_command(human_win_msg)
                        return None
                
                if Chess.insufficient_piece(self.chessboard):
                    self.stop_command(draw_msg)
                    return None
                    
                self.previous_position = None
                self.r_possible_moves.clear()
                self.move_data = []
                
                self.turn = self.opp_turn
                self.win_txt.config(text=computer_turn_msg)
                self.undo_btn.config(command='')
                self.reset_btn.config(command='')
                self.home_btn.config(command='')
                self.root.after(100, self.computer_move)
                #tt = Timer(.001, self.computer_move)
                #tt.start()

            #step 2: if box id not in possibble moves
            else:
                if len(self.r_possible_moves)>0:
                    self.r_possible_moves.clear()

                if self.chessboard[box_id] != '' and self.chessboard[box_id][0] == self.my_turn:
                    moving_man = self.chessboard[box_id]
                    self.previous_position = box_id
                    possible_moves = []

                    if len(self.move_data) == 0:
                        self.move_data = Chess.get_both_data(self.my_turn, self.chessboard, self.castle)
                    possible_moves = self.move_data[0]['legal_moves'].get(moving_man,[])
                    self.r_possible_moves = possible_moves.copy()    #storing bg color of possible moves
                    for box in possible_moves:  #changing color for possible moves
                        self.board[int(box[0])][int(box[1])].config(bg=pm_color)
                else:
                    self.previous_position = None

    #-------------- computer move ------------------------
    def computer_move(self):

        data,points = Chess.play(self.chessboard.copy(), deepcopy(self.castle), self.opp_turn, self.depth)        
        self.reset_btn.config(command=self.reset_board)
        self.home_btn.config(command=self.home_page)
        if data!=None:
            chessman_name,from_,to_= data
            
            if len(self.moved_mark)>0:
                for box in self.moved_mark:
                    mark_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                    self.board[int(box[0])][int(box[1])].config(bg=mark_color)
                self.moved_mark = []

            if chessman_name[1]=='S' and int(to_[0])==promote_row[self.opp_turn]:
                chessman_name = chessman_name[0]+'Q'+chessman_name[2:]

            self.board[int(from_[0])][int(from_[1])].config(text='')
            self.board[int(to_[0])][int(to_[1])].config(text=Chess.gui_man[chessman_name[0:2]])
            self.board[int(from_[0])][int(from_[1])].config(bg=move_color)
            self.board[int(to_[0])][int(to_[1])].config(bg=move_color)

            self.moved_mark.append(from_)
            self.moved_mark.append(to_)

            if self.chessboard[to_]!='':
                self.dead_list.append(self.chessboard[to_])
                self.add_label(self.right_txt, Chess.gui_man[self.chessboard[to_][0:2]])
                #self.right_txt.config(text = self.right_txt.cget("text")+Chess.gui_man[self.chessboard[to_][0:2]])
            
            if chessman_name[1]=='K' and abs(int(from_[1])-int(to_[1]))==2:
                #castle case
                if int(from_[1])-int(to_[1])==2:
                    #left castle
                    self.board[int(self.castle[self.opp_turn]['lep'][0])][int(self.castle[self.opp_turn]['lep'][1])].config(text='')
                    self.board[int(self.castle[self.opp_turn]['lboxes'][0][0])][int(self.castle[self.opp_turn]['lboxes'][0][1])].config(text=Chess.gui_man[self.castle[self.opp_turn]['leid'][0:2]])
                    self.board[int(self.castle[self.opp_turn]['lep'][0])][int(self.castle[self.opp_turn]['lep'][1])].config(bg=move_color)
                    self.board[int(self.castle[self.opp_turn]['lboxes'][0][0])][int(self.castle[self.opp_turn]['lboxes'][0][1])].config(bg=move_color)
                    self.moved_mark.append(self.castle[self.opp_turn]['lep'])
                    self.moved_mark.append(self.castle[self.opp_turn]['lboxes'][0])
                else:
                    #right castle
                    self.board[int(self.castle[self.opp_turn]['rep'][0])][int(self.castle[self.opp_turn]['rep'][1])].config(text='')
                    self.board[int(self.castle[self.opp_turn]['rboxes'][0][0])][int(self.castle[self.opp_turn]['rboxes'][0][1])].config(text=Chess.gui_man[self.castle[self.opp_turn]['reid'][0:2]])
                    self.board[int(self.castle[self.opp_turn]['rep'][0])][int(self.castle[self.opp_turn]['rep'][1])].config(bg=move_color)
                    self.board[int(self.castle[self.opp_turn]['rboxes'][0][0])][int(self.castle[self.opp_turn]['rboxes'][0][1])].config(bg=move_color)
                    self.moved_mark.append(self.castle[self.opp_turn]['rep'])
                    self.moved_mark.append(self.castle[self.opp_turn]['rboxes'][0])
            
            Chess.push(self.opp_turn, self.chessboard, self.castle, from_, to_, chessman_name)
            temp = Chess.get_both_data(self.opp_turn, self.chessboard, self.castle)

            if temp[1]['kp'] in temp[0]['all_moves']:
                self.moved_mark.append(temp[1]['kp'])
                self.board[int(temp[1]['kp'][0])][int(temp[1]['kp'][1])].config(bg=check_color)

            if len(temp[1]['legal_moves'])==0:
                if Chess.checkmate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                    self.stop_command(computer_win_msg)
                    return None

                elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                    self.stop_command(computer_win_msg)
                    return None
                
            if Chess.insufficient_piece(self.chessboard):
                self.stop_command(draw_msg)
                return None

            self.turn = self.my_turn
            self.win_txt.config(text=human_turn_msg)
            self.undo_btn.config(command=self.undo_step)
            

if __name__ == '__main__':
    obj = ChessMain()
    obj.dashboardPage()
    obj.root.mainloop()
