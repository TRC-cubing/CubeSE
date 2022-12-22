import subprocess
import threading as th
import time as tm
import tkinter as tk
import heapq
from PIL import Image, ImageTk
from tkinter import Event, Place, StringVar, font, ttk
from tkinter.constants import DISABLED, NORMAL, E, X

root = tk.Tk()
#region GUI_prepare
SCHEIGHT = root.winfo_screenheight()
SCWIDTH = root.winfo_screenwidth()
HEIGHT = round(SCHEIGHT * 0.9)
WIDTH = round(SCWIDTH * 0.95)
CVWIDTH=round(WIDTH * 0.36923)
CVHEIGHT=round(HEIGHT * 0.45)
BCVWIDTH=round(WIDTH * 0.553846)
BCVHEIGHT=round(HEIGHT * 0.675)
OCVWIDTH=round(WIDTH * 0.46153846)
OCVHEIGHT=round(HEIGHT * 0.75)
Solver_frame = ttk.Frame(root)
Solver_for_Beginners_frame = ttk.Frame(root)
PLL_Explorer_frame = ttk.Frame(root)
OLL_Explorer_frame = ttk.Frame(root)
F2L_Explorer_frame = ttk.Frame(root)
sub_step_Explorer_frame = ttk.Frame(root)
show_rotation_path = "Hide"
show_PLL_path = "Aa"
ID = None
#endregion GUI_prepare

class State:
    #class for rubix cube
    def __init__(self, cp, co, ep, eo):
        self.cp = cp
        self.co = co
        self.ep = ep
        self.eo = eo

    def apply_move(self, move):
        #apply moves and return new state
        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]
        new_ep = [self.ep[p] for p in move.ep]
        new_eo = [(self.eo[p] + move.eo[i]) % 2 for i, p in enumerate(move.ep)]
        return State(new_cp, new_co, new_ep, new_eo)

#solved
solved_state = State(
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
)

#moves
moves = {
    'U': State([3, 0, 1, 2, 4, 5, 6, 7],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'D': State([0, 1, 2, 3, 5, 6, 7, 4],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'L': State([4, 1, 2, 0, 7, 5, 6, 3],
                [2, 0, 0, 1, 1, 0, 0, 2],
                [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'R': State([0, 2, 6, 3, 4, 1, 5, 7],
                [0, 1, 2, 0, 0, 2, 1, 0],
                [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'F': State([0, 1, 3, 7, 4, 5, 2, 6],
                [0, 0, 1, 2, 0, 0, 2, 1],
                [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
                [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]),
    'B': State([1, 5, 2, 3, 0, 4, 6, 7],
                [1, 2, 0, 0, 2, 1, 0, 0],
                [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11],
                [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
                )}
#move_names = []
faces = list(moves.keys())
for face_name in faces:
    #move_names += [face_name, face_name + '2', face_name + '\'']
    moves[face_name + '2'] = moves[face_name].apply_move(moves[face_name])
    moves[face_name + '\''] = moves[face_name].apply_move(moves[face_name]).apply_move(moves[face_name])

del faces

RL_dict = {"U":"L", "U2":"L2", "U'":"L'", "D":"R", "D2":"R2", "D'":"R'", "R":"U", "R2":"U2", "R'":"U'", "L":"D", "L2":"D2", "L'":"D'", "F":"F", "F2":"F2", "F'":"F'", "B":"B", "B2":"B2", "B'":"B'"}
FB_dict = {"U":"B", "U2":"B2", "U'":"B'", "D":"F", "D2":"F2", "D'":"F'", "F":"U", "F2":"U2", "F'":"U'", "B":"D", "B2":"D2", "B'":"D'", "R":"R", "R2":"R2", "R'":"R'", "L":"L", "L2":"L2", "L'":"L'"}

def scramble2state():
    scrambled_state = solved_state
    for move_name in exe.scramblecheck:
        move_state = moves[move_name]
        scrambled_state = scrambled_state.apply_move(move_state)
    return scrambled_state

def scramble2state_RL():
    scrambled_state = solved_state
    for move_name in exe.scramblecheck:
        move_state = moves[RL_dict[move_name]]
        scrambled_state = scrambled_state.apply_move(move_state)
    return scrambled_state

def scramble2state_FB():
    scrambled_state = solved_state
    for move_name in exe.scramblecheck:
        move_state = moves[FB_dict[move_name]]
        scrambled_state = scrambled_state.apply_move(move_state)
    return scrambled_state

class Roots:
#region functions 
    def solving_thread(self):
        thread1 = th.Thread(target=exe.Solving_Start)
        thread1.setDaemon(True)
        thread1.start()

    def Exit(self):
        if not exe.search.poll():
            exe.search.kill()
            """cmd = "stopsearch.vbs"
            subprocess.Popen(cmd, shell=True)"""
            global ID
            root.after_cancel(ID)

    def Exit_thread(self):
        thread2 = th.Thread(target=Rt.Exit)
        thread2.start()

    def Explorer_thread(self):
        thread3 = th.Thread(target=pllex.PLLarg_dicision)
        thread3.setDaemon(True)
        thread3.start()

    def Explorer_Exit(self):
        if not pllex.search.poll():
            pllex.search.kill()
            """cmd = "stopsearch.vbs"
            subprocess.Popen(cmd, shell=True)
            global ID
            root.after_cancel(ID)"""

    def Explorer_Exit_thread(self):
        thread4 = th.Thread(target=Rt.Explorer_Exit)
        thread4.start()

    def Explorer2_thread(self):
        thread5 = th.Thread(target=ollex.OLLarg_dicision)
        thread5.setDaemon(True)
        thread5.start()

    def Explorer2_Exit(self):
        if not ollex.search.poll():
            ollex.search.kill()

    def Explorer2_Exit_thread(self):
        thread6 = th.Thread(target=Rt.Explorer2_Exit)
        thread6.start()

    def Explorer3_thread(self):
        thread7 = th.Thread(target=f2lex.F2Larg_dicision)
        thread7.setDaemon(True)
        thread7.start()

    def Explorer3_Exit(self):
        if not f2lex.search.poll():
            f2lex.search.kill()

    def Explorer3_Exit_thread(self):
        thread8 = th.Thread(target=Rt.Explorer3_Exit)
        thread8.start()

    def Explorer4_thread(self):
        thread9 = th.Thread(target=sub_stepex.sub_steps_arg_dicision)
        thread9.setDaemon(True)
        thread9.start()

    def Explorer4_Exit(self):
        if not sub_stepex.search.poll():
            sub_stepex.search.kill()

    def Explorer4_Exit_thread(self):
        thread10 = th.Thread(target=Rt.Explorer4_Exit)
        thread10.start()

    def change_to_Solver_frame(self):
        Solver_frame.tkraise()

    def change_to_Solver_for_Beginners_frame(self):
        Solver_for_Beginners_frame.tkraise()

    def change_to_PLL_Explorer_frame(self):
        PLL_Explorer_frame.tkraise()

    def change_to_OLL_Explorer_frame(self):
        OLL_Explorer_frame.tkraise()

    def change_to_F2L_Explorer_frame(self):
        F2L_Explorer_frame.tkraise()

    def change_to_sub_step_Explorer_frame(self):
        sub_step_Explorer_frame.tkraise()

#endregion functions
    def Prepare_Start(self):
#region Solver_for_cubers_frame
        root.title("Cube SE")
        #root.state("zoomed")
        root.geometry("{0}x{1}+{2}+{3}".format(round(SCWIDTH * 0.95), round(SCHEIGHT * 0.9), round(SCWIDTH * 0.025), round(SCHEIGHT * 0.05)))
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        Solver_frame.grid(row=0, column=0, sticky="nsew")

    #menu
        menu_list = tk.Menu(root)
        menu_list.add_cascade(label="Solver for cubers", command=Rt.change_to_Solver_frame)
        menu_list.add_cascade(label="Solver for beginners", command=Rt.change_to_Solver_for_Beginners_frame)
        menu_list.add_cascade(label="PLL Explorer", command=Rt.change_to_PLL_Explorer_frame)
        menu_list.add_cascade(label="OLL Explorer", command=Rt.change_to_OLL_Explorer_frame)
        menu_list.add_cascade(label="F2L Explorer", command=Rt.change_to_F2L_Explorer_frame)
        menu_list.add_cascade(label="sub steps Explorer", command=Rt.change_to_sub_step_Explorer_frame)
        root.config(menu=menu_list)

    #label
        lbl_1 = ttk.Label(Solver_frame, text="Input scramble")
        lbl_1.place(relx=0.0077, rely=0)
        lbl_2 = ttk.Label(Solver_frame, text="Designate the first searching depth (default:7)")
        lbl_2.place(relx=0.0077, rely=0.075)
        lbl_3 = ttk.Label(Solver_frame, text="Designate max searching depth (default:23)")
        lbl_3.place(relx=0.0077, rely=0.15)
        lbl_4 = ttk.Label(Solver_frame, text="Designate searching time in second (default:10)")
        lbl_4.place(relx=0.0077, rely=0.225)
        lbl_5 = ttk.Label(Solver_frame, text="Select searching mode (default:Use only UD Domino Reduction)")
        lbl_5.place(relx=0.307, rely=0)
        lbl_caution = ttk.Label(Solver_frame, text="It may take some time \nto start searching for solutions \nfor the first execution", font=("MenLo", "16", "bold"), background="Yellow", padding=[round(WIDTH * 0.0077), round(HEIGHT * 0.0125)])
        lbl_caution.place(relx=0.308, rely=0.175)

    #textbox
        self.txt_scramble = ttk.Entry(Solver_frame, width=round(WIDTH * 0.04615))
        self.txt_scramble.place(relx=0.0077, rely=0.0375)
        self.txt_min_length = ttk.Entry(Solver_frame, width=round(WIDTH * 0.003847))
        self.txt_min_length.place(relx=0.0077, rely=0.1125)
        self.txt_min_length.insert(0, "7")
        self.txt_max_length = ttk.Entry(Solver_frame, width=round(WIDTH * 0.003847))
        self.txt_max_length.place(relx=0.0077, rely=0.1875)
        self.txt_max_length.insert(0, "23")
        self.txt_timeout = ttk.Entry(Solver_frame, width=round(WIDTH * 0.003847))
        self.txt_timeout.place(relx=0.0077, rely=0.2625)
        self.txt_timeout.insert(0, "10")

    #scrollbar
        self.Solution_Box = tk.Text(Solver_frame)
        self.Solution_Box.place(width=int(WIDTH * 0.48462), height=round(HEIGHT * 0.6125), relx=0.0077, rely=0.375)
        bar_y = ttk.Scrollbar(self.Solution_Box, orient=tk.VERTICAL)
        bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        bar_y.config(command=self.Solution_Box.yview)
        self.Solution_Box.config(yscrollcommand=bar_y.set)

    #checkbox
        self.var1 = tk.BooleanVar(Solver_frame)
        delete_or_not = ttk.Checkbutton(Solver_frame, text="Check to delete recent solutions", variable=self.var1)
        delete_or_not.place(relx=0.13077, rely=0.3375)
        self.var2 = tk.BooleanVar(Solver_frame)
        insert_or_not = ttk.Checkbutton(Solver_frame, text="Check to insert Rotation letters", variable=self.var2)
        insert_or_not.place(relx=0.56538, rely=0.475)

    #radiobutton
        self.select_axis_var = tk.IntVar(Solver_frame)
        self.select_axis_var.set(1)
        all_axis_button = ttk.Radiobutton(Solver_frame, text="Use all", value=0, var=self.select_axis_var)
        all_axis_button.place(relx=0.3077, rely=0.025)
        UD_axis_button = ttk.Radiobutton(Solver_frame, text="Use only UD Domino Reduction", value=1, var=self.select_axis_var)
        UD_axis_button.place(relx=0.3077, rely=0.0625)
        RL_axis_button = ttk.Radiobutton(Solver_frame, text="Use only RL Domino Reduction", value=2, var=self.select_axis_var)
        RL_axis_button.place(relx=0.3077, rely=0.1)
        FB_axis_button = ttk.Radiobutton(Solver_frame, text="Use only FB Domino Reduction", value=3, var=self.select_axis_var)
        FB_axis_button.place(relx=0.3077, rely=0.1375)

    #button
        self.ButtonStart = ttk.Button(Solver_frame,text="Start", command=Rt.solving_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.01875)])
        self.ButtonStart.place(relx=0.0077, rely=0.3)
        self.ButtonExit = ttk.Button(Solver_frame,text="Stop", command=Rt.Exit_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.01875)])
        self.ButtonExit.place(relx=0.06923077, rely=0.3)
        self.ButtonExit["state"] = tk.DISABLED

    #canvas
        self.scramble_canvas = tk.Canvas(Solver_frame, width=round(WIDTH * 0.36923), height=round(HEIGHT * 0.45), bg="Black")
        self.scramble_canvas.place(relx=0.5846154, rely=0)
        # 735 -> 760

    #list
        self.ColorList = ["White","White","White","White","White","White","White","White","White",
                    "Green","Green","Green","Green","Green","Green","Green","Green","Green",
                    "Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow",
                    "Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange",
                    "Red","Red","Red","Red","Red","Red","Red","Red","Red",
                    "Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue"]
        
        exe.Paint()

        class MoveButtonFunction():
            def U(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[2],Rt.ColorList[5],Rt.ColorList[8],Rt.ColorList[1],Rt.ColorList[4], \
                    Rt.ColorList[7],Rt.ColorList[0],Rt.ColorList[3],Rt.ColorList[6],Rt.ColorList[27], \
                    Rt.ColorList[28],Rt.ColorList[29],Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47], \
                    Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38],Rt.ColorList[9],Rt.ColorList[10],Rt.ColorList[11] \
                    =Rt.ColorList[0],Rt.ColorList[1],Rt.ColorList[2],Rt.ColorList[3],Rt.ColorList[4], \
                    Rt.ColorList[5],Rt.ColorList[6],Rt.ColorList[7],Rt.ColorList[8],Rt.ColorList[9], \
                    Rt.ColorList[10],Rt.ColorList[11],Rt.ColorList[27],Rt.ColorList[28],Rt.ColorList[29], \
                    Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47],Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38]

                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "U ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "U2 ")
                    else:
                        Rt.txt_scramble.insert("end", "U' ")

            def F(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[9],Rt.ColorList[10],Rt.ColorList[11],Rt.ColorList[12],Rt.ColorList[13], \
                    Rt.ColorList[14],Rt.ColorList[15],Rt.ColorList[16],Rt.ColorList[17],Rt.ColorList[6], \
                    Rt.ColorList[7],Rt.ColorList[8],Rt.ColorList[36],Rt.ColorList[39],Rt.ColorList[42], \
                    Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20],Rt.ColorList[29],Rt.ColorList[32],Rt.ColorList[35] \
                    =Rt.ColorList[15],Rt.ColorList[12],Rt.ColorList[9],Rt.ColorList[16],Rt.ColorList[13], \
                    Rt.ColorList[10],Rt.ColorList[17],Rt.ColorList[14],Rt.ColorList[11],Rt.ColorList[35], \
                    Rt.ColorList[32],Rt.ColorList[29],Rt.ColorList[6],Rt.ColorList[7],Rt.ColorList[8], \
                    Rt.ColorList[42],Rt.ColorList[39],Rt.ColorList[36],Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20]
                
                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "F ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "F2 ")
                    else:
                        Rt.txt_scramble.insert("end", "F' ")

            def D(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20],Rt.ColorList[21],Rt.ColorList[22], \
                    Rt.ColorList[23],Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26],Rt.ColorList[15], \
                    Rt.ColorList[16],Rt.ColorList[17],Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44], \
                    Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53],Rt.ColorList[33],Rt.ColorList[34],Rt.ColorList[35] \
                    =Rt.ColorList[24],Rt.ColorList[21],Rt.ColorList[18],Rt.ColorList[25],Rt.ColorList[22], \
                    Rt.ColorList[19],Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20],Rt.ColorList[33], \
                    Rt.ColorList[34],Rt.ColorList[35],Rt.ColorList[15],Rt.ColorList[16],Rt.ColorList[17], \
                    Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44],Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53]

                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "D ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "D2 ")
                    else:
                        Rt.txt_scramble.insert("end", "D' ")
                        
            def L(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[27],Rt.ColorList[28],Rt.ColorList[29],Rt.ColorList[30],Rt.ColorList[31], \
                    Rt.ColorList[32],Rt.ColorList[33],Rt.ColorList[34],Rt.ColorList[35],Rt.ColorList[0], \
                    Rt.ColorList[3],Rt.ColorList[6],Rt.ColorList[9],Rt.ColorList[12],Rt.ColorList[15], \
                    Rt.ColorList[18],Rt.ColorList[21],Rt.ColorList[24],Rt.ColorList[47],Rt.ColorList[50],Rt.ColorList[53] \
                    =Rt.ColorList[33],Rt.ColorList[30],Rt.ColorList[27],Rt.ColorList[34],Rt.ColorList[31], \
                    Rt.ColorList[28],Rt.ColorList[35],Rt.ColorList[32],Rt.ColorList[29],Rt.ColorList[53], \
                    Rt.ColorList[50],Rt.ColorList[47],Rt.ColorList[0],Rt.ColorList[3],Rt.ColorList[6], \
                    Rt.ColorList[9],Rt.ColorList[12],Rt.ColorList[15],Rt.ColorList[24],Rt.ColorList[21],Rt.ColorList[18]

                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "L ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "L2 ")
                    else:
                        Rt.txt_scramble.insert("end", "L' ")
            
            def R(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38],Rt.ColorList[39],Rt.ColorList[40], \
                    Rt.ColorList[41],Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44],Rt.ColorList[8], \
                    Rt.ColorList[5],Rt.ColorList[2],Rt.ColorList[45],Rt.ColorList[48],Rt.ColorList[51], \
                    Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20],Rt.ColorList[17],Rt.ColorList[14],Rt.ColorList[11] \
                    =Rt.ColorList[42],Rt.ColorList[39],Rt.ColorList[36],Rt.ColorList[43],Rt.ColorList[40], \
                    Rt.ColorList[37],Rt.ColorList[44],Rt.ColorList[41],Rt.ColorList[38],Rt.ColorList[17], \
                    Rt.ColorList[14],Rt.ColorList[11],Rt.ColorList[8],Rt.ColorList[5],Rt.ColorList[2], \
                    Rt.ColorList[45],Rt.ColorList[48],Rt.ColorList[51],Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20]
                
                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "R ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "R2 ")
                    else:
                        Rt.txt_scramble.insert("end", "R' ")
            
            def B(self, rotation):
                for i in range(rotation):
                    Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47],Rt.ColorList[48],Rt.ColorList[49], \
                    Rt.ColorList[50],Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53],Rt.ColorList[2], \
                    Rt.ColorList[1],Rt.ColorList[0],Rt.ColorList[27],Rt.ColorList[30],Rt.ColorList[33], \
                    Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26],Rt.ColorList[44],Rt.ColorList[41],Rt.ColorList[38] \
                    =Rt.ColorList[51],Rt.ColorList[48],Rt.ColorList[45],Rt.ColorList[52],Rt.ColorList[49], \
                    Rt.ColorList[46],Rt.ColorList[53],Rt.ColorList[50],Rt.ColorList[47],Rt.ColorList[44], \
                    Rt.ColorList[41],Rt.ColorList[38],Rt.ColorList[2],Rt.ColorList[1],Rt.ColorList[0], \
                    Rt.ColorList[27],Rt.ColorList[30],Rt.ColorList[33],Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26]
            
                if Rt.var2.get():
                    if rotation == 1:
                        Rt.txt_scramble.insert("end", "B ")
                    elif rotation == 2:
                        Rt.txt_scramble.insert("end", "B2 ")
                    else:
                        Rt.txt_scramble.insert("end", "B' ")

            def x(self):
                Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38],Rt.ColorList[39],Rt.ColorList[40], \
                Rt.ColorList[41],Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44],Rt.ColorList[8], \
                Rt.ColorList[5],Rt.ColorList[2],Rt.ColorList[45],Rt.ColorList[48],Rt.ColorList[51], \
                Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20],Rt.ColorList[17],Rt.ColorList[14],Rt.ColorList[11] \
                =Rt.ColorList[42],Rt.ColorList[39],Rt.ColorList[36],Rt.ColorList[43],Rt.ColorList[40], \
                Rt.ColorList[37],Rt.ColorList[44],Rt.ColorList[41],Rt.ColorList[38],Rt.ColorList[17], \
                Rt.ColorList[14],Rt.ColorList[11],Rt.ColorList[8],Rt.ColorList[5],Rt.ColorList[2], \
                Rt.ColorList[45],Rt.ColorList[48],Rt.ColorList[51],Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20]

                for i in range(3):
                    Rt.ColorList[27],Rt.ColorList[28],Rt.ColorList[29],Rt.ColorList[30],Rt.ColorList[31], \
                    Rt.ColorList[32],Rt.ColorList[33],Rt.ColorList[34],Rt.ColorList[35],Rt.ColorList[0], \
                    Rt.ColorList[3],Rt.ColorList[6],Rt.ColorList[9],Rt.ColorList[12],Rt.ColorList[15], \
                    Rt.ColorList[18],Rt.ColorList[21],Rt.ColorList[24],Rt.ColorList[47],Rt.ColorList[50],Rt.ColorList[53] \
                    =Rt.ColorList[33],Rt.ColorList[30],Rt.ColorList[27],Rt.ColorList[34],Rt.ColorList[31], \
                    Rt.ColorList[28],Rt.ColorList[35],Rt.ColorList[32],Rt.ColorList[29],Rt.ColorList[53], \
                    Rt.ColorList[50],Rt.ColorList[47],Rt.ColorList[0],Rt.ColorList[3],Rt.ColorList[6], \
                    Rt.ColorList[9],Rt.ColorList[12],Rt.ColorList[15],Rt.ColorList[24],Rt.ColorList[21],Rt.ColorList[18]

                Rt.ColorList[1],Rt.ColorList[4],Rt.ColorList[7],Rt.ColorList[10],Rt.ColorList[13],Rt.ColorList[16], \
                Rt.ColorList[19],Rt.ColorList[22],Rt.ColorList[25],Rt.ColorList[46],Rt.ColorList[49],Rt.ColorList[52] \
                =Rt.ColorList[10],Rt.ColorList[13],Rt.ColorList[16],Rt.ColorList[19],Rt.ColorList[22],Rt.ColorList[25], \
                Rt.ColorList[52],Rt.ColorList[49],Rt.ColorList[46],Rt.ColorList[7],Rt.ColorList[4],Rt.ColorList[1]
                return exe.Paint()
            
            def y(self):
                Rt.ColorList[2],Rt.ColorList[5],Rt.ColorList[8],Rt.ColorList[1],Rt.ColorList[4], \
                Rt.ColorList[7],Rt.ColorList[0],Rt.ColorList[3],Rt.ColorList[6],Rt.ColorList[27], \
                Rt.ColorList[28],Rt.ColorList[29],Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47], \
                Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38],Rt.ColorList[9],Rt.ColorList[10],Rt.ColorList[11] \
                =Rt.ColorList[0],Rt.ColorList[1],Rt.ColorList[2],Rt.ColorList[3],Rt.ColorList[4], \
                Rt.ColorList[5],Rt.ColorList[6],Rt.ColorList[7],Rt.ColorList[8],Rt.ColorList[9], \
                Rt.ColorList[10],Rt.ColorList[11],Rt.ColorList[27],Rt.ColorList[28],Rt.ColorList[29], \
                Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47],Rt.ColorList[36],Rt.ColorList[37],Rt.ColorList[38]
            
                for i in range(3):
                    Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20],Rt.ColorList[21],Rt.ColorList[22], \
                    Rt.ColorList[23],Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26],Rt.ColorList[15], \
                    Rt.ColorList[16],Rt.ColorList[17],Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44], \
                    Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53],Rt.ColorList[33],Rt.ColorList[34],Rt.ColorList[35] \
                    =Rt.ColorList[24],Rt.ColorList[21],Rt.ColorList[18],Rt.ColorList[25],Rt.ColorList[22], \
                    Rt.ColorList[19],Rt.ColorList[26],Rt.ColorList[23],Rt.ColorList[20],Rt.ColorList[33], \
                    Rt.ColorList[34],Rt.ColorList[35],Rt.ColorList[15],Rt.ColorList[16],Rt.ColorList[17], \
                    Rt.ColorList[42],Rt.ColorList[43],Rt.ColorList[44],Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53]
                
                Rt.ColorList[12],Rt.ColorList[13],Rt.ColorList[14],Rt.ColorList[39],Rt.ColorList[40],Rt.ColorList[41], \
                Rt.ColorList[48],Rt.ColorList[49],Rt.ColorList[50],Rt.ColorList[30],Rt.ColorList[31],Rt.ColorList[32] \
                =Rt.ColorList[39],Rt.ColorList[40],Rt.ColorList[41],Rt.ColorList[48],Rt.ColorList[49],Rt.ColorList[50], \
                Rt.ColorList[30],Rt.ColorList[31],Rt.ColorList[32],Rt.ColorList[12],Rt.ColorList[13],Rt.ColorList[14]
                return exe.Paint()

            def z(self):
                Rt.ColorList[9],Rt.ColorList[10],Rt.ColorList[11],Rt.ColorList[12],Rt.ColorList[13], \
                Rt.ColorList[14],Rt.ColorList[15],Rt.ColorList[16],Rt.ColorList[17],Rt.ColorList[6], \
                Rt.ColorList[7],Rt.ColorList[8],Rt.ColorList[36],Rt.ColorList[39],Rt.ColorList[42], \
                Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20],Rt.ColorList[29],Rt.ColorList[32],Rt.ColorList[35] \
                =Rt.ColorList[15],Rt.ColorList[12],Rt.ColorList[9],Rt.ColorList[16],Rt.ColorList[13], \
                Rt.ColorList[10],Rt.ColorList[17],Rt.ColorList[14],Rt.ColorList[11],Rt.ColorList[35], \
                Rt.ColorList[32],Rt.ColorList[29],Rt.ColorList[6],Rt.ColorList[7],Rt.ColorList[8], \
                Rt.ColorList[42],Rt.ColorList[39],Rt.ColorList[36],Rt.ColorList[18],Rt.ColorList[19],Rt.ColorList[20]

                for i in range(3):
                    Rt.ColorList[45],Rt.ColorList[46],Rt.ColorList[47],Rt.ColorList[48],Rt.ColorList[49], \
                    Rt.ColorList[50],Rt.ColorList[51],Rt.ColorList[52],Rt.ColorList[53],Rt.ColorList[2], \
                    Rt.ColorList[1],Rt.ColorList[0],Rt.ColorList[27],Rt.ColorList[30],Rt.ColorList[33], \
                    Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26],Rt.ColorList[44],Rt.ColorList[41],Rt.ColorList[38] \
                    =Rt.ColorList[51],Rt.ColorList[48],Rt.ColorList[45],Rt.ColorList[52],Rt.ColorList[49], \
                    Rt.ColorList[46],Rt.ColorList[53],Rt.ColorList[50],Rt.ColorList[47],Rt.ColorList[44], \
                    Rt.ColorList[41],Rt.ColorList[38],Rt.ColorList[2],Rt.ColorList[1],Rt.ColorList[0], \
                    Rt.ColorList[27],Rt.ColorList[30],Rt.ColorList[33],Rt.ColorList[24],Rt.ColorList[25],Rt.ColorList[26]

                Rt.ColorList[3],Rt.ColorList[4],Rt.ColorList[5],Rt.ColorList[37],Rt.ColorList[40],Rt.ColorList[43], \
                Rt.ColorList[23],Rt.ColorList[22],Rt.ColorList[21],Rt.ColorList[34],Rt.ColorList[31],Rt.ColorList[28] \
                =Rt.ColorList[34],Rt.ColorList[31],Rt.ColorList[28],Rt.ColorList[3],Rt.ColorList[4],Rt.ColorList[5], \
                Rt.ColorList[37],Rt.ColorList[40],Rt.ColorList[43],Rt.ColorList[23],Rt.ColorList[22],Rt.ColorList[21]
                return exe.Paint()

        Mbf = MoveButtonFunction()

        self.Scramble_Print_Dictionary = {
            "U" : Mbf.U,
            "U2" : Mbf.U,
            "U'" : Mbf.U,
            "F" : Mbf.F,
            "F2" : Mbf.F,
            "F'" : Mbf.F,
            "D" : Mbf.D,
            "D2" : Mbf.D,
            "D'" : Mbf.D,
            "L" : Mbf.L,
            "L2" : Mbf.L,
            "L'" : Mbf.L,
            "R" : Mbf.R,
            "R2" : Mbf.R,
            "R'" : Mbf.R,
            "B" : Mbf.B,
            "B2" : Mbf.B,
            "B'" : Mbf.B
        }

        def Print_Reset():
            Rt.ColorList = ["White","White","White","White","White","White","White","White","White", \
                        "Green","Green","Green","Green","Green","Green","Green","Green","Green", \
                        "Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow", \
                        "Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange", \
                        "Red","Red","Red","Red","Red","Red","Red","Red","Red", \
                        "Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue"]

            if Rt.var2.get():
                Rt.txt_scramble.delete(0, "end")

            return exe.Paint()
    #buttoncommand
        ButtonU = ttk.Button(Solver_frame,text="U", command=lambda:[Mbf.U(rotation = 1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonU.place(relx=0.56538, rely=0.525)
        # 735 420
        ButtonU2 = ttk.Button(Solver_frame,text="U2", command=lambda:[Mbf.U(rotation = 2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonU2.place(relx=0.6346154, rely=0.525)
        # 815 380 -> 825 420
        ButtonUprime = ttk.Button(Solver_frame,text="U'", command=lambda:[Mbf.U(rotation = 3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonUprime.place(relx=0.703846, rely=0.525)
        # 895 380 -> 915 420
        
        ButtonD = ttk.Button(Solver_frame,text="D", command=lambda:[Mbf.D(rotation=1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonD.place(relx=0.78077, rely=0.525)
        # 975 380 -> 1015 420
        ButtonD2 = ttk.Button(Solver_frame,text="D2", command=lambda:[Mbf.D(rotation=2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonD2.place(relx=0.85, rely=0.525)
        # 1055 380 -> 1105 420
        ButtonDprime = ttk.Button(Solver_frame,text="D'", command=lambda:[Mbf.D(rotation=3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonDprime.place(relx=0.919231, rely=0.525)
        # 1135 380 -> 1195 420

        ButtonR = ttk.Button(Solver_frame,text="R", command=lambda:[Mbf.R(rotation=1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonR.place(relx=0.56538, rely=0.625)
        ButtonR2 = ttk.Button(Solver_frame,text="R2", command=lambda:[Mbf.R(rotation=2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonR2.place(relx=0.6346154, rely=0.625)
        ButtonRprime = ttk.Button(Solver_frame,text="R'", command=lambda:[Mbf.R(rotation=3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonRprime.place(relx=0.703846, rely=0.625)

        ButtonL = ttk.Button(Solver_frame,text="L", command=lambda:[Mbf.L(rotation=1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonL.place(relx=0.78077, rely=0.625)
        ButtonL2 = ttk.Button(Solver_frame,text="L2", command=lambda:[Mbf.L(rotation=2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonL2.place(relx=0.85, rely=0.625)
        ButtonLprime = ttk.Button(Solver_frame,text="L'", command=lambda:[Mbf.L(rotation=3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonLprime.place(relx=0.919231, rely=0.625)

        ButtonF = ttk.Button(Solver_frame,text="F", command=lambda:[Mbf.F(rotation=1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonF.place(relx=0.56538, rely=0.725)
        ButtonF2 = ttk.Button(Solver_frame,text="F2", command=lambda:[Mbf.F(rotation=2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonF2.place(relx=0.6346154, rely=0.725)
        ButtonFprime = ttk.Button(Solver_frame,text="F'", command=lambda:[Mbf.F(rotation=3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonFprime.place(relx=0.703846, rely=0.725)

        ButtonB = ttk.Button(Solver_frame,text="B", command=lambda:[Mbf.B(rotation=1), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonB.place(relx=0.78077, rely=0.725)
        ButtonB2 = ttk.Button(Solver_frame,text="B2", command=lambda:[Mbf.B(rotation=2), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonB2.place(relx=0.85, rely=0.725)
        ButtonBprime = ttk.Button(Solver_frame,text="B'", command=lambda:[Mbf.B(rotation=3), exe.Paint()], width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        ButtonBprime.place(relx=0.919231, rely=0.725)
        
        Buttonx = ttk.Button(Solver_frame,text="x", command=Mbf.x, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        Buttonx.place(relx=0.56538, rely=0.825)
        Buttony = ttk.Button(Solver_frame,text="y", command=Mbf.y, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        Buttony.place(relx=0.6346154, rely=0.825)
        Buttonz = ttk.Button(Solver_frame,text="z", command=Mbf.z, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01385), round(HEIGHT * 0.0225)])
        Buttonz.place(relx=0.703846, rely=0.825)

        ButtonReset = ttk.Button(Solver_frame,text="Reset", command=Print_Reset, width=round(WIDTH * 0.03077), padding=[0, round(HEIGHT * 0.0225)])
        ButtonReset.place(relx=0.78077, rely=0.825)

#endregion Solver_for_cubers_frame

#region Solver_for_Beginners_frame
        Solver_for_Beginners_frame.grid(row=0, column=0, sticky="nsew")
    
    #picture
        self.rotation_image = Image.open("RP\\" + show_rotation_path + ".png")
        self.resize_image = self.rotation_image.resize((round(WIDTH * 0.36923077), round(HEIGHT * 0.3375)))
        self.show_rotation_img = ImageTk.PhotoImage(self.resize_image)
        # self.show_rotation_img = tk.PhotoImage(file=(show_rotation_path+".png"))
        self.show_img = tk.Label(Solver_for_Beginners_frame, image=self.show_rotation_img)
        self.show_img.place(relx=0.5923077, rely=0.3)
        # 240 + 270 = 510, 570
        # 480, 270

    #squares
        self.B_selected_color = "White"
        self.B_paint_canvas = tk.Canvas(Solver_for_Beginners_frame, width=round(WIDTH * 0.553846), height=round(HEIGHT * 0.675), bg="Black")
        self.B_paint_canvas.place(relx=0, rely=0)
        # 720, 540
        bexe.B_Paint()
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.041666), round(BCVHEIGHT * 0.74074), round(BCVWIDTH * 0.20833), round(BCVHEIGHT * 0.962963), fill=self.B_selected_color, tags="show")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.50277), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.58055), round(BCVHEIGHT * 0.88518), fill="White", tags="SelectWhite")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.58611), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.66388), round(BCVHEIGHT * 0.88518), fill="Yellow", tags="SelectYellow")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.66944), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.74722), round(BCVHEIGHT * 0.88518), fill="Red", tags="SelectRed")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.75277), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.83055), round(BCVHEIGHT * 0.88518), fill="Dark Orange", tags="SelectOrange")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.83611), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.91388), round(BCVHEIGHT * 0.88518), fill="Blue", tags="SelectBlue")
        self.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.91944), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.99722), round(BCVHEIGHT * 0.88518), fill="Green", tags="SelectGreen")
        self.B_paint_canvas.tag_bind("SelectWhite", "<ButtonPress>", bexe.B_select_color_white)
        self.B_paint_canvas.tag_bind("SelectYellow", "<ButtonPress>", bexe.B_select_color_yellow)
        self.B_paint_canvas.tag_bind("SelectOrange", "<ButtonPress>", bexe.B_select_color_orange)
        self.B_paint_canvas.tag_bind("SelectRed", "<ButtonPress>", bexe.B_select_color_red)
        self.B_paint_canvas.tag_bind("SelectBlue", "<ButtonPress>", bexe.B_select_color_blue)
        self.B_paint_canvas.tag_bind("SelectGreen", "<ButtonPress>", bexe.B_select_color_green)

    #label
        B_lbl1 = ttk.Label(Solver_for_Beginners_frame, text="Selected color", font=("MenLo", "13", "bold"))
        B_lbl1.place(relx=0.0246154, rely=0.46)
        B_lbl2 = ttk.Label(Solver_for_Beginners_frame, text="Select color", font=("MenLo", "13", "bold"))
        B_lbl2.place(relx=0.376923, rely=0.46)
        B_lbl3 = ttk.Label(Solver_for_Beginners_frame, text="Solution", font=("MenLo", "18", "bold"))
        B_lbl3.place(relx=0.73077, rely=0.0125)
        B_lbl_sol = ttk.Label(Solver_for_Beginners_frame, textvariable=bexe.lbltext, font=("MenLo", "25", "bold"), wraplength=round(WIDTH * 0.3846154))
        B_lbl_sol.place(relx=0.592377, rely=0.0625)
        B_lbl_so5 = ttk.Label(Solver_for_Beginners_frame, text="Hold the white center on the top, the green center in front, and the red center to the right.", font=("MenLo", "16", "bold"), background="Yellow", wraplength=round(WIDTH * 0.3846154))
        B_lbl_so5.place(relx=0.592377,rely=0.225)
        B_lbl_4 = ttk.Label(Solver_for_Beginners_frame, text="Press buttons below to show how to rotate Rubik's cube")
        B_lbl_4.place(relx=0.6, rely=0.6625)

    #button
        B_Reset_Button = ttk.Button(Solver_for_Beginners_frame, text="Reset", width=round(WIDTH * 0.00384615), padding=[round(WIDTH * 0.061538), round(HEIGHT * 0.1)], command=bexe.B_Paint_reset)
        B_Reset_Button.place(relx=0.0153846, rely=0.7125)
        # 20, 570, 5, 80, 80
        B_Solved_Button = ttk.Button(Solver_for_Beginners_frame, text="Solved", width=round(WIDTH * 0.0046154), padding=[round(WIDTH * 0.061538), round(HEIGHT * 0.1)], command=bexe.B_Paint_solved)
        B_Solved_Button.place(relx=0.2, rely=0.7125)
        self.B_Start_Button = ttk.Button(Solver_for_Beginners_frame, text="Start", width=round(WIDTH * 0.00384615), padding=[round(WIDTH * 0.061538), round(HEIGHT * 0.1)], command=bexe.dicision)
        self.B_Start_Button.place(relx=0.3846154, rely=0.7125)
        B_Hide_Button = ttk.Button(Solver_for_Beginners_frame, text="Hide", width=round(WIDTH * 0.016923077), padding=[round(WIDTH * 0.0015384615), round(HEIGHT * 0.0025)], command=lambda : bexe.Show_Rotation_pic(18))
        B_Hide_Button.place(relx=0.846154, rely=0.6625)

        U_show_button = ttk.Button(Solver_for_Beginners_frame, text="U", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(0))
        U_show_button.place(relx=0.6, rely=0.7125)
        U2_show_button = ttk.Button(Solver_for_Beginners_frame, text="U2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(1))
        U2_show_button.place(relx=0.66154, rely=0.7125)
        Uprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="U'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(2))
        Uprime_show_button.place(relx=0.723077, rely=0.7125)
        D_show_button = ttk.Button(Solver_for_Beginners_frame, text="D", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(3))
        D_show_button.place(relx=0.784615, rely=0.7125)
        D2_show_button = ttk.Button(Solver_for_Beginners_frame, text="D2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(4))
        D2_show_button.place(relx=0.846154, rely=0.7125)
        Dprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="D'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(5))
        Dprime_show_button.place(relx=0.9077, rely=0.7125)

        R_show_button = ttk.Button(Solver_for_Beginners_frame, text="R", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(6))
        R_show_button.place(relx=0.6, rely=0.8)
        R2_show_button = ttk.Button(Solver_for_Beginners_frame, text="R2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(7))
        R2_show_button.place(relx=0.66154, rely=0.8)
        Rprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="R'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(8))
        Rprime_show_button.place(relx=0.723077, rely=0.8)
        L_show_button = ttk.Button(Solver_for_Beginners_frame, text="L", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(9))
        L_show_button.place(relx=0.784615, rely=0.8)
        L2_show_button = ttk.Button(Solver_for_Beginners_frame, text="L2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(10))
        L2_show_button.place(relx=0.846154, rely=0.8)
        Lprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="L'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(11))
        Lprime_show_button.place(relx=0.9077, rely=0.8)

        F_show_button = ttk.Button(Solver_for_Beginners_frame, text="F", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(12))
        F_show_button.place(relx=0.6, rely=0.8875)
        F2_show_button = ttk.Button(Solver_for_Beginners_frame, text="F2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(13))
        F2_show_button.place(relx=0.66154, rely=0.8875)
        Fprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="F'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(14))
        Fprime_show_button.place(relx=0.723077, rely=0.8875)
        B_show_button = ttk.Button(Solver_for_Beginners_frame, text="B", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(15))
        B_show_button.place(relx=0.784615, rely=0.8875)
        B2_show_button = ttk.Button(Solver_for_Beginners_frame, text="B2", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(16))
        B2_show_button.place(relx=0.846154, rely=0.8875)
        Bprime_show_button = ttk.Button(Solver_for_Beginners_frame, text="B'", width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT  * 0.0225)], command=lambda : bexe.Show_Rotation_pic(17))
        Bprime_show_button.place(relx=0.9077, rely=0.8875)

    #bind  
        self.B_paint_canvas.tag_bind("N0", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N0")])
        self.B_paint_canvas.tag_bind("N1", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N1")])
        self.B_paint_canvas.tag_bind("N2", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N2")])
        self.B_paint_canvas.tag_bind("N3", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N3")])
        self.B_paint_canvas.tag_bind("N5", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N5")])
        self.B_paint_canvas.tag_bind("N6", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N6")])
        self.B_paint_canvas.tag_bind("N7", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N7")])
        self.B_paint_canvas.tag_bind("N8", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N8")])
        self.B_paint_canvas.tag_bind("N9", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N9")])
        self.B_paint_canvas.tag_bind("N10", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N10")])
        self.B_paint_canvas.tag_bind("N11", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N11")])
        self.B_paint_canvas.tag_bind("N12", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N12")])
        self.B_paint_canvas.tag_bind("N14", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N14")])
        self.B_paint_canvas.tag_bind("N15", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N15")])
        self.B_paint_canvas.tag_bind("N16", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N16")])
        self.B_paint_canvas.tag_bind("N17", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N17")])
        self.B_paint_canvas.tag_bind("N18", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N18")])
        self.B_paint_canvas.tag_bind("N19", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N19")])
        self.B_paint_canvas.tag_bind("N20", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N20")])
        self.B_paint_canvas.tag_bind("N21", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N21")])
        self.B_paint_canvas.tag_bind("N23", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N23")])
        self.B_paint_canvas.tag_bind("N24", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N24")])
        self.B_paint_canvas.tag_bind("N25", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N25")])
        self.B_paint_canvas.tag_bind("N26", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N26")])
        self.B_paint_canvas.tag_bind("N27", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N27")])
        self.B_paint_canvas.tag_bind("N28", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N28")])
        self.B_paint_canvas.tag_bind("N29", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N29")])
        self.B_paint_canvas.tag_bind("N30", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N30")])
        self.B_paint_canvas.tag_bind("N32", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N32")])
        self.B_paint_canvas.tag_bind("N33", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N33")])
        self.B_paint_canvas.tag_bind("N34", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N34")])
        self.B_paint_canvas.tag_bind("N35", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N35")])
        self.B_paint_canvas.tag_bind("N36", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N36")])
        self.B_paint_canvas.tag_bind("N37", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N37")])
        self.B_paint_canvas.tag_bind("N38", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N38")])
        self.B_paint_canvas.tag_bind("N39", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N39")])
        self.B_paint_canvas.tag_bind("N41", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N41")])
        self.B_paint_canvas.tag_bind("N42", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N42")])
        self.B_paint_canvas.tag_bind("N43", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N43")])
        self.B_paint_canvas.tag_bind("N44", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N44")])
        self.B_paint_canvas.tag_bind("N45", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N45")])
        self.B_paint_canvas.tag_bind("N46", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N46")])
        self.B_paint_canvas.tag_bind("N47", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N47")])
        self.B_paint_canvas.tag_bind("N48", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N48")])
        self.B_paint_canvas.tag_bind("N50", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N50")])
        self.B_paint_canvas.tag_bind("N51", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N51")])
        self.B_paint_canvas.tag_bind("N52", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N52")])
        self.B_paint_canvas.tag_bind("N53", "<ButtonPress>", func=lambda event : [bexe.B_change_color(event, "N53")])

#endregion Solver_for_Beginners_frame

#region PLL_Explorer
        PLL_Explorer_frame.grid(row=0, column=0, sticky="nsew")
        self.selected_PLL = tk.StringVar()
        self.selected_PLL.set("Selected PLL : Aa")

    #textbox and pulldown
        PLL_list = ["Aa","Ab","E","F","Ga","Gb","Gc","Gd","H","Ja","Jb","Na","Nb","Ra","Rb","T","Ua","Ub","V","Y","Z"]
        self.PLL_var = tk.StringVar()
        self.Ex_commbobox_PLL = ttk.Combobox(PLL_Explorer_frame, values=PLL_list, textvariable=self.PLL_var, state="readonly")
        self.Ex_commbobox_PLL.place(relx=0.0077,rely=0.0375)
        self.Ex_commbobox_PLL.current(0)
        self.Ex_commbobox_PLL.bind("<<ComboboxSelected>>", pllex.showPLLpic)
        startfrom1 = ["None", "y", "y2", "y'"]
        startfrom2 = ["None", "x", "x'"]
        self.Ex_startfrom1_PLL_comb = ttk.Combobox(PLL_Explorer_frame, values=startfrom1, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex_startfrom1_PLL_comb.place(relx=0.2461538, rely=0.21875)
        # 170
        self.Ex_startfrom1_PLL_comb.current(0)
        self.Ex_startfrom2_PLL_comb = ttk.Combobox(PLL_Explorer_frame, values=startfrom2, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex_startfrom2_PLL_comb.place(relx=0.2461538, rely=0.26875)
        # 215
        self.Ex_startfrom2_PLL_comb.current(0)

        self.Ex_txt_min_length = ttk.Entry(PLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex_txt_min_length.place(relx=0.0077, rely=0.1125)
        self.Ex_txt_min_length.insert(0, "6")
        self.Ex_txt_max_length = ttk.Entry(PLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex_txt_max_length.place(relx=0.0077, rely=0.1875)
        self.Ex_txt_max_length.insert(0, "30")
        self.Ex_txt_timeout = ttk.Entry(PLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex_txt_timeout.place(relx=0.0077, rely=0.2625)
        self.Ex_txt_timeout.insert(0, "50")
    
    #label
        Ex_lbl_1 = ttk.Label(PLL_Explorer_frame, text="Select PLL")
        Ex_lbl_1.place(relx=0.0077, rely=0)
        Ex_lbl_2 = ttk.Label(PLL_Explorer_frame, text="Designate the first searching depth (default:6)")
        Ex_lbl_2.place(relx=0.0077, rely=0.075)
        Ex_lbl_3 = ttk.Label(PLL_Explorer_frame, text="Designate max searching depth (default:30)")
        Ex_lbl_3.place(relx=0.0077, rely=0.15)
        Ex_lbl_4 = ttk.Label(PLL_Explorer_frame, text="Designate how many solutions to explore (default:50)")
        Ex_lbl_4.place(relx=0.0077, rely=0.225)
        Ex_lbl_5 = ttk.Label(PLL_Explorer_frame, text="Check faces you want to use")
        Ex_lbl_5.place(relx=0.2461538, rely=0)
        Ex_lbl_6 = ttk.Label(PLL_Explorer_frame, text="Use half turns")
        Ex_lbl_6.place(relx=0.2461538, rely=0.1125)
        Ex_lbl_7 = ttk.Label(PLL_Explorer_frame, text="Select the orientation")
        Ex_lbl_7.place(relx=0.2461538, rely=0.1875)
        Ex_lbl_8 = ttk.Label(PLL_Explorer_frame, textvariable=self.selected_PLL, font=("MenLo", "25", "bold"))
        Ex_lbl_8.place(relx=0.61538, rely=0)
        # 780
        Ex_lbl_10 = ttk.Label(PLL_Explorer_frame, text="and")
        Ex_lbl_10.place(relx=0.3176923, rely=0.24375)
        Ex_lbl_11 = ttk.Label(PLL_Explorer_frame, text="Put AUF and ADF into brackets")
        Ex_lbl_11.place(relx=0.353846, rely=0.1125)

    #checkbox
        self.Ex_var0 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_slice_fat = ttk.Checkbutton(PLL_Explorer_frame,variable=self.Ex_var0,text="allow fat and slice moves",command=pllex.allow_to_check)
        self.Ex_slice_fat.place(relx=0.4, rely=0)

        self.Ex_var1 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen1 = ttk.Checkbutton(PLL_Explorer_frame,text="U",variable=self.Ex_var1)
        self.Ex_available_gen1.place(relx=0.2461538, rely=0.0375)
        self.Ex_var1.set(1)
        # 320
        self.Ex_var2 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen2 = ttk.Checkbutton(PLL_Explorer_frame,text="D",variable=self.Ex_var2)
        self.Ex_available_gen2.place(relx=0.276923, rely=0.0375)
        self.Ex_var2.set(1)
        # 350 -> 360
        self.Ex_var3 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen3 = ttk.Checkbutton(PLL_Explorer_frame,text="L",variable=self.Ex_var3)
        self.Ex_available_gen3.place(relx=0.3076923, rely=0.0375)
        self.Ex_var3.set(1)
        # 380 -> 400
        self.Ex_var4 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen4 = ttk.Checkbutton(PLL_Explorer_frame,text="R",variable=self.Ex_var4)
        self.Ex_available_gen4.place(relx=0.3384615, rely=0.0375)
        self.Ex_var4.set(1)
        # 410 -> 440
        self.Ex_var5 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen5 = ttk.Checkbutton(PLL_Explorer_frame,text="F",variable=self.Ex_var5)
        self.Ex_available_gen5.place(relx=0.36923077, rely=0.0375)
        self.Ex_var5.set(1)
        # 440 -> 480
        self.Ex_var6 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen6 = ttk.Checkbutton(PLL_Explorer_frame,text="B",variable=self.Ex_var6)
        self.Ex_available_gen6.place(relx=0.4, rely=0.0375)
        self.Ex_var6.set(1)
        # 470 -> 520
        self.Ex_var7 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen7 = ttk.Checkbutton(PLL_Explorer_frame,text="Uw",variable=self.Ex_var7,state=tk.DISABLED)
        self.Ex_available_gen7.place(relx=0.2461538, rely=0.075)
        self.Ex_var7.set(0)
        # 320
        self.Ex_var8 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen8 = ttk.Checkbutton(PLL_Explorer_frame,text="Dw",variable=self.Ex_var8,state=tk.DISABLED)
        self.Ex_available_gen8.place(relx=0.276923, rely=0.075)
        self.Ex_var8.set(0)
        # 360
        self.Ex_var9 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen9 = ttk.Checkbutton(PLL_Explorer_frame,text="Lw",variable=self.Ex_var9,state=tk.DISABLED)
        self.Ex_available_gen9.place(relx=0.3076923, rely=0.075)
        self.Ex_var9.set(0)
        # 400
        self.Ex_var10 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen10 = ttk.Checkbutton(PLL_Explorer_frame,text="Rw",variable=self.Ex_var10,state=tk.DISABLED)
        self.Ex_available_gen10.place(relx=0.3384615, rely=0.075)
        self.Ex_var10.set(0)
        # 440
        self.Ex_var11 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen11 = ttk.Checkbutton(PLL_Explorer_frame,text="Fw",variable=self.Ex_var11,state=tk.DISABLED)
        self.Ex_available_gen11.place(relx=0.36923077, rely=0.075)
        self.Ex_var11.set(0)
        # 480
        self.Ex_var12 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen12 = ttk.Checkbutton(PLL_Explorer_frame,text="Bw",variable=self.Ex_var12,state=tk.DISABLED)
        self.Ex_available_gen12.place(relx=0.4, rely=0.075)
        self.Ex_var12.set(0)
        # 520
        self.Ex_var13 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen13 = ttk.Checkbutton(PLL_Explorer_frame,text="M",variable=self.Ex_var13,state=tk.DISABLED)
        self.Ex_available_gen13.place(relx=0.43076923, rely=0.075)
        self.Ex_var13.set(0)
        # 560
        self.Ex_var14 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen14 = ttk.Checkbutton(PLL_Explorer_frame,text="E",variable=self.Ex_var14,state=tk.DISABLED)
        self.Ex_available_gen14.place(relx=0.46153846, rely=0.075)
        self.Ex_var14.set(0)
        # 590 -> 600
        self.Ex_var15 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_available_gen15 = ttk.Checkbutton(PLL_Explorer_frame,text="S",variable=self.Ex_var15,state=tk.DISABLED)
        self.Ex_available_gen15.place(relx=0.4923077, rely=0.075)
        self.Ex_var15.set(0)
        # 620 -> 640
        self.Ex_var16 = tk.BooleanVar(PLL_Explorer_frame)
        self.Ex_solution_delete = ttk.Checkbutton(PLL_Explorer_frame,text="Check to delete recent algs",variable=self.Ex_var16)
        self.Ex_solution_delete.place(relx=0.35384615, rely=0.1875)
        self.Ex_var16.set(0)
        # 460

    #radiobutton
        self.htm_var = tk.IntVar(PLL_Explorer_frame)
        self.htm_var.set(0)
        usehtm_button = ttk.Radiobutton(PLL_Explorer_frame, text="Yes", value=0, var=self.htm_var)
        usehtm_button.place(relx=0.246153846, rely=0.15)
        unusehtm_button = ttk.Radiobutton(PLL_Explorer_frame, text="No", value=1, var=self.htm_var)
        unusehtm_button.place(relx=0.2923077, rely=0.15)
        self.auf_var = tk.IntVar(PLL_Explorer_frame)
        self.auf_var.set(1)
        usebracket_button = ttk.Radiobutton(PLL_Explorer_frame, text="Yes", value=0, var=self.auf_var)
        usebracket_button.place(relx=0.35384615, rely=0.15)
        unusebracket_button = ttk.Radiobutton(PLL_Explorer_frame, text="No", value=1, var=self.auf_var)
        unusebracket_button.place(relx=0.4, rely=0.15)

    #button
        self.Button_explor_PLL_start = ttk.Button(PLL_Explorer_frame,text="Start", command=Rt.Explorer_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_PLL_start.place(relx=0.35384615, rely=0.225)
        self.Button_explor_PLL_exit = ttk.Button(PLL_Explorer_frame,text="Stop", command=Rt.Explorer_Exit_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_PLL_exit.place(relx=0.4153846, rely=0.225)
        self.Button_explor_PLL_exit["state"] = tk.DISABLED

    #scrollbar
        self.explor_PLL_Box = tk.Text(PLL_Explorer_frame)
        self.explor_PLL_Box.place(relwidth=0.461538, relheight=0.675, relx=0.0077, rely=0.3125)
        exploe_PLL_bar_y = ttk.Scrollbar(self.explor_PLL_Box, orient=tk.VERTICAL)
        exploe_PLL_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        exploe_PLL_bar_y.config(command=self.explor_PLL_Box.yview)
        self.explor_PLL_Box.config(yscrollcommand=exploe_PLL_bar_y.set)

    #pic
        self.PLL_image = Image.open("RP\\" + show_PLL_path + "perm.png")
        self.resize_image_PLL = self.PLL_image.resize((round(WIDTH * 0.473077), round(HEIGHT * 0.76875)))
        self.show_PLL_img = ImageTk.PhotoImage(self.resize_image_PLL)
        self.show_img2 = tk.Label(PLL_Explorer_frame, image=self.show_PLL_img)
        self.show_img2.place(relx=0.5076923, rely=0.125)

#endregion PLL_Explorer

#region OLL_Explorer
        OLL_Explorer_frame.grid(row=0, column=0, sticky="nsew")

    #label
        Ex2_lbl_1 = ttk.Label(OLL_Explorer_frame, text="Designate the first searching depth (default:6)")
        Ex2_lbl_1.place(relx=0.0077, rely=0)
        Ex2_lbl_2 = ttk.Label(OLL_Explorer_frame, text="Designate max searching depth (default:30)")
        Ex2_lbl_2.place(relx=0.0077, rely=0.075)
        Ex2_lbl_3 = ttk.Label(OLL_Explorer_frame, text="Designate how many solutions to explore (default:50)")
        Ex2_lbl_3.place(relx=0.0077, rely=0.15)
        Ex2_lbl_4 = ttk.Label(OLL_Explorer_frame, text="Check faces you want to use")
        Ex2_lbl_4.place(relx=0.2461538, rely=0)
        Ex2_lbl_5 = ttk.Label(OLL_Explorer_frame, text="Use half turns")
        Ex2_lbl_5.place(relx=0.2461538, rely=0.1125)
        Ex2_lbl_6 = ttk.Label(OLL_Explorer_frame, text="Select the orientation")
        Ex2_lbl_6.place(relx=0.2461538, rely=0.1875)
        Ex2_lbl_7 = ttk.Label(OLL_Explorer_frame, text="and")
        Ex2_lbl_7.place(relx=0.3176923, rely=0.24375)
        Ex2_lbl_8 = ttk.Label(OLL_Explorer_frame, text="Click to paint", font=("MenLo", "25", "bold"))
        Ex2_lbl_8.place(relx=0.65384, rely=0)
        Ex2_lbl_9 = ttk.Label(OLL_Explorer_frame, text="Put ADF into brackets")
        Ex2_lbl_9.place(relx=0.353846, rely=0.1125)

    #textbox
        self.Ex2_txt_min_length = ttk.Entry(OLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex2_txt_min_length.place(relx=0.0077, rely=0.0375)
        self.Ex2_txt_min_length.insert(0, "6")
        self.Ex2_txt_max_length = ttk.Entry(OLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex2_txt_max_length.place(relx=0.0077, rely=0.1125)
        self.Ex2_txt_max_length.insert(0, "30")
        self.Ex2_txt_timeout = ttk.Entry(OLL_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex2_txt_timeout.place(relx=0.0077, rely=0.1875)
        self.Ex2_txt_timeout.insert(0, "50")

    #checkbox
        self.Ex2_var0 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_slice_fat = ttk.Checkbutton(OLL_Explorer_frame,variable=self.Ex2_var0,text="allow fat and slice moves",command=ollex.allow_to_check)
        self.Ex2_slice_fat.place(relx=0.4, rely=0)

        self.Ex2_var1 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen1 = ttk.Checkbutton(OLL_Explorer_frame,text="U",variable=self.Ex2_var1)
        self.Ex2_available_gen1.place(relx=0.2461538, rely=0.0375)
        self.Ex2_var1.set(1)
        # 320
        self.Ex2_var2 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen2 = ttk.Checkbutton(OLL_Explorer_frame,text="D",variable=self.Ex2_var2)
        self.Ex2_available_gen2.place(relx=0.276923, rely=0.0375)
        self.Ex2_var2.set(1)
        # 350 -> 360
        self.Ex2_var3 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen3 = ttk.Checkbutton(OLL_Explorer_frame,text="L",variable=self.Ex2_var3)
        self.Ex2_available_gen3.place(relx=0.3076923, rely=0.0375)
        self.Ex2_var3.set(1)
        # 380 -> 400
        self.Ex2_var4 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen4 = ttk.Checkbutton(OLL_Explorer_frame,text="R",variable=self.Ex2_var4)
        self.Ex2_available_gen4.place(relx=0.3384615, rely=0.0375)
        self.Ex2_var4.set(1)
        # 410 -> 440
        self.Ex2_var5 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen5 = ttk.Checkbutton(OLL_Explorer_frame,text="F",variable=self.Ex2_var5)
        self.Ex2_available_gen5.place(relx=0.36923077, rely=0.0375)
        self.Ex2_var5.set(1)
        # 440 -> 480
        self.Ex2_var6 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen6 = ttk.Checkbutton(OLL_Explorer_frame,text="B",variable=self.Ex2_var6)
        self.Ex2_available_gen6.place(relx=0.4, rely=0.0375)
        self.Ex2_var6.set(1)
        # 470 -> 520
        self.Ex2_var7 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen7 = ttk.Checkbutton(OLL_Explorer_frame,text="Uw",variable=self.Ex2_var7,state=tk.DISABLED)
        self.Ex2_available_gen7.place(relx=0.2461538, rely=0.075)
        self.Ex2_var7.set(0)
        # 320
        self.Ex2_var8 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen8 = ttk.Checkbutton(OLL_Explorer_frame,text="Dw",variable=self.Ex2_var8,state=tk.DISABLED)
        self.Ex2_available_gen8.place(relx=0.276923, rely=0.075)
        self.Ex2_var8.set(0)
        # 360
        self.Ex2_var9 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen9 = ttk.Checkbutton(OLL_Explorer_frame,text="Lw",variable=self.Ex2_var9,state=tk.DISABLED)
        self.Ex2_available_gen9.place(relx=0.3076923, rely=0.075)
        self.Ex2_var9.set(0)
        # 400
        self.Ex2_var10 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen10 = ttk.Checkbutton(OLL_Explorer_frame,text="Rw",variable=self.Ex2_var10,state=tk.DISABLED)
        self.Ex2_available_gen10.place(relx=0.3384615, rely=0.075)
        self.Ex2_var10.set(0)
        # 440
        self.Ex2_var11 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen11 = ttk.Checkbutton(OLL_Explorer_frame,text="Fw",variable=self.Ex2_var11,state=tk.DISABLED)
        self.Ex2_available_gen11.place(relx=0.36923077, rely=0.075)
        self.Ex2_var11.set(0)
        # 480
        self.Ex2_var12 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen12 = ttk.Checkbutton(OLL_Explorer_frame,text="Bw",variable=self.Ex2_var12,state=tk.DISABLED)
        self.Ex2_available_gen12.place(relx=0.4, rely=0.075)
        self.Ex2_var12.set(0)
        # 520
        self.Ex2_var13 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen13 = ttk.Checkbutton(OLL_Explorer_frame,text="M",variable=self.Ex2_var13,state=tk.DISABLED)
        self.Ex2_available_gen13.place(relx=0.43076923, rely=0.075)
        self.Ex2_var13.set(0)
        # 560
        self.Ex2_var14 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen14 = ttk.Checkbutton(OLL_Explorer_frame,text="E",variable=self.Ex2_var14,state=tk.DISABLED)
        self.Ex2_available_gen14.place(relx=0.46153846, rely=0.075)
        self.Ex2_var14.set(0)
        # 590 -> 600
        self.Ex2_var15 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_available_gen15 = ttk.Checkbutton(OLL_Explorer_frame,text="S",variable=self.Ex2_var15,state=tk.DISABLED)
        self.Ex2_available_gen15.place(relx=0.4923077, rely=0.075)
        self.Ex2_var15.set(0)

        self.Ex2_var16 = tk.BooleanVar(OLL_Explorer_frame)
        self.Ex2_solution_delete = ttk.Checkbutton(OLL_Explorer_frame,text="Check to delete recent algs",variable=self.Ex2_var16)
        self.Ex2_solution_delete.place(relx=0.35384615, rely=0.1875)
        self.Ex2_var16.set(0)

    #radiobutton
        self.htm_var2 = tk.IntVar(OLL_Explorer_frame)
        self.htm_var2.set(0)
        usehtm_button2 = ttk.Radiobutton(OLL_Explorer_frame, text="Yes", value=0, var=self.htm_var2)
        usehtm_button2.place(relx=0.246153846, rely=0.15)
        unusehtm_button2 = ttk.Radiobutton(OLL_Explorer_frame, text="No", value=1, var=self.htm_var2)
        unusehtm_button2.place(relx=0.2923077, rely=0.15)
        self.auf_var2 = tk.IntVar(OLL_Explorer_frame)
        self.auf_var2.set(1)
        usebracket_button2 = ttk.Radiobutton(OLL_Explorer_frame, text="Yes", value=0, var=self.auf_var2)
        usebracket_button2.place(relx=0.35384615, rely=0.15)
        unusebracket_button2 = ttk.Radiobutton(OLL_Explorer_frame, text="No", value=1, var=self.auf_var2)
        unusebracket_button2.place(relx=0.4, rely=0.15)
    
    #pulldown
        self.Ex2_startfrom1_OLL_comb = ttk.Combobox(OLL_Explorer_frame, values=startfrom1, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex2_startfrom1_OLL_comb.place(relx=0.2461538, rely=0.21875)
        # 170
        self.Ex2_startfrom1_OLL_comb.current(0)
        self.Ex2_startfrom2_OLL_comb = ttk.Combobox(OLL_Explorer_frame, values=startfrom2, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex2_startfrom2_OLL_comb.place(relx=0.2461538, rely=0.26875)
        # 215
        self.Ex2_startfrom2_OLL_comb.current(0)

    #button
        self.Button_explor_OLL_start = ttk.Button(OLL_Explorer_frame, text="Start", command=Rt.Explorer2_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_OLL_start.place(relx=0.35384615, rely=0.225)
        self.Button_explor_OLL_exit = ttk.Button(OLL_Explorer_frame, text="Stop", command=Rt.Explorer2_Exit_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_OLL_exit.place(relx=0.4153846, rely=0.225)
        self.Button_explor_OLL_exit["state"] = tk.DISABLED
        self.Button_explor_OLL_reset = ttk.Button(OLL_Explorer_frame, text="Reset", command=ollex.Paint_reset, width=round(WIDTH * 0.02), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_OLL_reset.place(relx=0.653846, rely=0.89)

    #scrollbar
        self.explor_OLL_Box = tk.Text(OLL_Explorer_frame)
        self.explor_OLL_Box.place(relwidth=0.461538, relheight=0.675, relx=0.0077, rely=0.3125)
        exploe_OLL_bar_y = ttk.Scrollbar(self.explor_OLL_Box, orient=tk.VERTICAL)
        exploe_OLL_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        exploe_OLL_bar_y.config(command=self.explor_OLL_Box.yview)
        self.explor_OLL_Box.config(yscrollcommand=exploe_OLL_bar_y.set)

    #canvas
        self.OLL_paint_canvas = tk.Canvas(OLL_Explorer_frame, width=round(WIDTH * 0.46153846), height=round(HEIGHT * 0.75), bg="Black")
        self.OLL_paint_canvas.place(relx=0.5, rely=0.125)
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.03333), round(OCVHEIGHT * 0.125), round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.375), fill="Gray", tags="M0")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.03333), round(OCVHEIGHT * 0.375), round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.625), fill="Gray", tags="M1")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.03333), round(OCVHEIGHT * 0.625), round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.875), fill="Gray", tags="M2")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.125), round(OCVWIDTH * 0.96666), round(OCVHEIGHT * 0.375), fill="Gray", tags="M3")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.375), round(OCVWIDTH * 0.96666), round(OCVHEIGHT * 0.625), fill="Gray", tags="M4")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.625), round(OCVWIDTH * 0.96666), round(OCVHEIGHT * 0.875), fill="Gray", tags="M5")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.03333), round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.125), fill="Gray", tags="M6")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.03333), round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.125), fill="Gray", tags="M7")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.03333), round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.125), fill="Gray", tags="M8")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.875), round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.96666), fill="Gray", tags="M9")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.875), round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.96666), fill="Gray", tags="M10")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.875), round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.96666), fill="Gray", tags="M11")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.125), round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.375), fill="Gray", tags="M12")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.125), round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.375), fill="Gray", tags="M13")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.125), round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.375), fill="Gray", tags="M14")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.375), round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.625), fill="Gray", tags="M15")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.375), round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.625), fill="Yellow", tags="M16")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.375), round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.625), fill="Gray", tags="M17")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.125), round(OCVHEIGHT * 0.625), round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.875), fill="Gray", tags="M18")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.375), round(OCVHEIGHT * 0.625), round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.875), fill="Gray", tags="M19")
        self.OLL_paint_canvas.create_rectangle(round(OCVWIDTH * 0.625), round(OCVHEIGHT * 0.625), round(OCVWIDTH * 0.875), round(OCVHEIGHT * 0.875), fill="Gray", tags="M20")

    #bind
        self.OLL_paint_canvas.tag_bind("M0", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M0")])
        self.OLL_paint_canvas.tag_bind("M1", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M1")])
        self.OLL_paint_canvas.tag_bind("M2", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M2")])
        self.OLL_paint_canvas.tag_bind("M3", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M3")])
        self.OLL_paint_canvas.tag_bind("M4", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M4")])
        self.OLL_paint_canvas.tag_bind("M5", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M5")])
        self.OLL_paint_canvas.tag_bind("M6", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M6")])
        self.OLL_paint_canvas.tag_bind("M7", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M7")])
        self.OLL_paint_canvas.tag_bind("M8", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M8")])
        self.OLL_paint_canvas.tag_bind("M9", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M9")])
        self.OLL_paint_canvas.tag_bind("M10", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M10")])
        self.OLL_paint_canvas.tag_bind("M11", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M11")])
        self.OLL_paint_canvas.tag_bind("M12", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M12")])
        self.OLL_paint_canvas.tag_bind("M13", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M13")])
        self.OLL_paint_canvas.tag_bind("M14", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M14")])
        self.OLL_paint_canvas.tag_bind("M15", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M15")])
        self.OLL_paint_canvas.tag_bind("M17", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M17")])
        self.OLL_paint_canvas.tag_bind("M18", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M18")])
        self.OLL_paint_canvas.tag_bind("M19", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M19")])
        self.OLL_paint_canvas.tag_bind("M20", "<ButtonPress>", func=lambda event : [ollex.OLL_change_color(event, "M20")])

#endregion OLL_Explorer

#region F2L_Explorer
        F2L_Explorer_frame.grid(row=0, column=0, sticky="nsew")
        
    #label
        Ex3_lbl_1 = ttk.Label(F2L_Explorer_frame, text="Designate the first searching depth (default:3)")
        Ex3_lbl_1.place(relx=0.0077, rely=0)
        Ex3_lbl_2 = ttk.Label(F2L_Explorer_frame, text="Designate max searching depth (default:30)")
        Ex3_lbl_2.place(relx=0.0077, rely=0.075)
        Ex3_lbl_3 = ttk.Label(F2L_Explorer_frame, text="Designate how many solutions to explore (default:50)")
        Ex3_lbl_3.place(relx=0.0077, rely=0.15)
        Ex3_lbl_4 = ttk.Label(F2L_Explorer_frame, text="Check faces you want to use")
        Ex3_lbl_4.place(relx=0.2461538, rely=0)
        Ex3_lbl_5 = ttk.Label(F2L_Explorer_frame, text="Use half turns")
        Ex3_lbl_5.place(relx=0.2461538, rely=0.1125)
        Ex3_lbl_6 = ttk.Label(F2L_Explorer_frame, text="Select the orientation")
        Ex3_lbl_6.place(relx=0.2461538, rely=0.1875)
        Ex3_lbl_8 = ttk.Label(F2L_Explorer_frame, text="Click to paint", font=("MenLo", "25", "bold"))
        Ex3_lbl_8.place(relx=0.687, rely=0)
        Ex3_lbl_12 = ttk.Label(F2L_Explorer_frame, text="Solve :")
        Ex3_lbl_12.place(relx=0.593846, rely=0.5225)
        Ex3_lbl_13 = ttk.Label(F2L_Explorer_frame, text="Solved slot :")
        Ex3_lbl_13.place(relx=0.593846, rely=0.5525)
        Ex3_lbl_14 = ttk.Label(F2L_Explorer_frame, text="Paint only one corner and one edge", font=("Menlo", "18", "bold"))
        Ex3_lbl_14.place(relx=0.583846, rely=0.6025)

    #textbox
        self.Ex3_txt_min_length = ttk.Entry(F2L_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex3_txt_min_length.place(relx=0.0077, rely=0.0375)
        self.Ex3_txt_min_length.insert(0, "3")
        self.Ex3_txt_max_length = ttk.Entry(F2L_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex3_txt_max_length.place(relx=0.0077, rely=0.1125)
        self.Ex3_txt_max_length.insert(0, "30")
        self.Ex3_txt_timeout = ttk.Entry(F2L_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex3_txt_timeout.place(relx=0.0077, rely=0.1875)
        self.Ex3_txt_timeout.insert(0, "50")

    #checkbox
        self.Ex3_var0 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_slice_fat = ttk.Checkbutton(F2L_Explorer_frame,variable=self.Ex3_var0,text="allow fat and slice moves",command=f2lex.allow_to_check)
        self.Ex3_slice_fat.place(relx=0.4, rely=0)

        self.Ex3_var1 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen1 = ttk.Checkbutton(F2L_Explorer_frame,text="U",variable=self.Ex3_var1)
        self.Ex3_available_gen1.place(relx=0.2461538, rely=0.0375)
        self.Ex3_var1.set(1)
        # 320
        self.Ex3_var2 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen2 = ttk.Checkbutton(F2L_Explorer_frame,text="D",variable=self.Ex3_var2)
        self.Ex3_available_gen2.place(relx=0.276923, rely=0.0375)
        self.Ex3_var2.set(1)
        # 350 -> 360
        self.Ex3_var3 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen3 = ttk.Checkbutton(F2L_Explorer_frame,text="L",variable=self.Ex3_var3)
        self.Ex3_available_gen3.place(relx=0.3076923, rely=0.0375)
        self.Ex3_var3.set(1)
        # 380 -> 400
        self.Ex3_var4 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen4 = ttk.Checkbutton(F2L_Explorer_frame,text="R",variable=self.Ex3_var4)
        self.Ex3_available_gen4.place(relx=0.3384615, rely=0.0375)
        self.Ex3_var4.set(1)
        # 410 -> 440
        self.Ex3_var5 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen5 = ttk.Checkbutton(F2L_Explorer_frame,text="F",variable=self.Ex3_var5)
        self.Ex3_available_gen5.place(relx=0.36923077, rely=0.0375)
        self.Ex3_var5.set(1)
        # 440 -> 480
        self.Ex3_var6 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen6 = ttk.Checkbutton(F2L_Explorer_frame,text="B",variable=self.Ex3_var6)
        self.Ex3_available_gen6.place(relx=0.4, rely=0.0375)
        self.Ex3_var6.set(1)
        # 470 -> 520
        self.Ex3_var7 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen7 = ttk.Checkbutton(F2L_Explorer_frame,text="Uw",variable=self.Ex3_var7,state=tk.DISABLED)
        self.Ex3_available_gen7.place(relx=0.2461538, rely=0.075)
        self.Ex3_var7.set(0)
        # 320
        self.Ex3_var8 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen8 = ttk.Checkbutton(F2L_Explorer_frame,text="Dw",variable=self.Ex3_var8,state=tk.DISABLED)
        self.Ex3_available_gen8.place(relx=0.276923, rely=0.075)
        self.Ex3_var8.set(0)
        # 360
        self.Ex3_var9 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen9 = ttk.Checkbutton(F2L_Explorer_frame,text="Lw",variable=self.Ex3_var9,state=tk.DISABLED)
        self.Ex3_available_gen9.place(relx=0.3076923, rely=0.075)
        self.Ex3_var9.set(0)
        # 400
        self.Ex3_var10 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen10 = ttk.Checkbutton(F2L_Explorer_frame,text="Rw",variable=self.Ex3_var10,state=tk.DISABLED)
        self.Ex3_available_gen10.place(relx=0.3384615, rely=0.075)
        self.Ex3_var10.set(0)
        # 440
        self.Ex3_var11 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen11 = ttk.Checkbutton(F2L_Explorer_frame,text="Fw",variable=self.Ex3_var11,state=tk.DISABLED)
        self.Ex3_available_gen11.place(relx=0.36923077, rely=0.075)
        self.Ex3_var11.set(0)
        # 480
        self.Ex3_var12 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen12 = ttk.Checkbutton(F2L_Explorer_frame,text="Bw",variable=self.Ex3_var12,state=tk.DISABLED)
        self.Ex3_available_gen12.place(relx=0.4, rely=0.075)
        self.Ex3_var12.set(0)
        # 520
        self.Ex3_var13 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen13 = ttk.Checkbutton(F2L_Explorer_frame,text="M",variable=self.Ex3_var13,state=tk.DISABLED)
        self.Ex3_available_gen13.place(relx=0.43076923, rely=0.075)
        self.Ex3_var13.set(0)
        # 560
        self.Ex3_var14 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen14 = ttk.Checkbutton(F2L_Explorer_frame,text="E",variable=self.Ex3_var14,state=tk.DISABLED)
        self.Ex3_available_gen14.place(relx=0.46153846, rely=0.075)
        self.Ex3_var14.set(0)
        # 590 -> 600
        self.Ex3_var15 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_available_gen15 = ttk.Checkbutton(F2L_Explorer_frame,text="S",variable=self.Ex3_var15,state=tk.DISABLED)
        self.Ex3_available_gen15.place(relx=0.4923077, rely=0.075)
        self.Ex3_var15.set(0)

        self.Ex3_var16 = tk.BooleanVar(F2L_Explorer_frame)
        self.Ex3_solution_delete = ttk.Checkbutton(F2L_Explorer_frame,text="Check to delete recent algs",variable=self.Ex3_var16)
        self.Ex3_solution_delete.place(relx=0.35384615, rely=0.1875)
        self.Ex3_var16.set(0)

        self.solved_slot_var0 = tk.BooleanVar(F2L_Explorer_frame)
        self.solved_slot0 = ttk.Checkbutton(F2L_Explorer_frame,text="FR slot",variable=self.solved_slot_var0,state=tk.DISABLED,command=lambda: f2lex.paint_slots(0))
        self.solved_slot0.place(relx=0.648846, rely=0.5525)
        self.solved_slot_var0.set(0)

        self.solved_slot_var1 = tk.BooleanVar(F2L_Explorer_frame)
        self.solved_slot1 = ttk.Checkbutton(F2L_Explorer_frame,text="FL slot",variable=self.solved_slot_var1,command=lambda: f2lex.paint_slots(1))
        self.solved_slot1.place(relx=0.698846, rely=0.5525)
        self.solved_slot_var1.set(0)

        self.solved_slot_var2 = tk.BooleanVar(F2L_Explorer_frame)
        self.solved_slot2 = ttk.Checkbutton(F2L_Explorer_frame,text="BR slot",variable=self.solved_slot_var2,command=lambda: f2lex.paint_slots(2))
        self.solved_slot2.place(relx=0.748846, rely=0.5525)
        self.solved_slot_var2.set(0)

        self.solved_slot_var3 = tk.BooleanVar(F2L_Explorer_frame)
        self.solved_slot3 = ttk.Checkbutton(F2L_Explorer_frame,text="BL slot",variable=self.solved_slot_var3,command=lambda: f2lex.paint_slots(3))
        self.solved_slot3.place(relx=0.798846, rely=0.5525)
        self.solved_slot_var3.set(0)

    #radiobutton
        self.htm_var3 = tk.IntVar(F2L_Explorer_frame)
        self.htm_var3.set(0)
        usehtm_button3 = ttk.Radiobutton(F2L_Explorer_frame, text="Yes", value=0, var=self.htm_var3)
        usehtm_button3.place(relx=0.246153846, rely=0.15)
        unusehtm_button3 = ttk.Radiobutton(F2L_Explorer_frame, text="No", value=1, var=self.htm_var3)
        unusehtm_button3.place(relx=0.2923077, rely=0.15)
        self.auf_var3 = tk.IntVar(F2L_Explorer_frame)
    
    #pulldown
        self.Ex3_startfrom1_F2L_comb = ttk.Combobox(F2L_Explorer_frame, values=startfrom1, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex3_startfrom1_F2L_comb.place(relx=0.2461538, rely=0.21875)
        self.Ex3_startfrom1_F2L_comb.current(0)
        self.F2L_list = ["FR slot", "FL slot", "BR slot", "BL slot"]
        self.F2L_var = tk.StringVar()
        self.Ex3_commbobox_F2L = ttk.Combobox(F2L_Explorer_frame, values=self.F2L_list, textvariable=self.F2L_var, state="readonly")
        self.Ex3_commbobox_F2L.place(relx=0.633846, rely=0.5225)
        self.Ex3_commbobox_F2L.current(0)
        self.Ex3_commbobox_F2L.bind("<<ComboboxSelected>>", f2lex.select_slot)

    #button
        self.Button_explor_F2L_start = ttk.Button(F2L_Explorer_frame, text="Start", command=Rt.Explorer3_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_F2L_start.place(relx=0.35384615, rely=0.225)
        self.Button_explor_F2L_exit = ttk.Button(F2L_Explorer_frame, text="Stop", command=Rt.Explorer3_Exit_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_F2L_exit.place(relx=0.4153846, rely=0.225)
        self.Button_explor_F2L_exit["state"] = tk.DISABLED
        self.Button_explor_F2L_Reset = ttk.Button(F2L_Explorer_frame, text="Reset", command=f2lex.Paint_reset, width=round(WIDTH * 0.004077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_F2L_Reset.place(relx=0.8953846, rely=0.52)

    #scrollbar
        self.explor_F2L_Box = tk.Text(F2L_Explorer_frame)
        self.explor_F2L_Box.place(relwidth=0.461538, relheight=0.675, relx=0.0077, rely=0.3125)
        exploe_F2L_bar_y = ttk.Scrollbar(self.explor_F2L_Box, orient=tk.VERTICAL)
        exploe_F2L_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        exploe_F2L_bar_y.config(command=self.explor_F2L_Box.yview)
        self.explor_F2L_Box.config(yscrollcommand=exploe_F2L_bar_y.set)

    #canvas
        self.Ex3_selected_color = "White"
        self.Ex3_slot_color_set = ["White", "Blue", "Red"]
        self.F2L_paint_canvas = tk.Canvas(F2L_Explorer_frame, width=round(WIDTH * 0.36923), height=round(HEIGHT * 0.45), bg="Black")
        self.F2L_paint_canvas.place(relx=0.5846154, rely=0.065)
        f2lex.Paint()
        self.F2L_paint_canvas.tag_bind("Select0", "<ButtonPress>", f2lex.Ex3_select_color0)
        self.F2L_paint_canvas.tag_bind("Select1", "<ButtonPress>", f2lex.Ex3_select_color1)
        self.F2L_paint_canvas.tag_bind("Select2", "<ButtonPress>", f2lex.Ex3_select_color2)
        Ex3_lbl10 = ttk.Label(F2L_Explorer_frame, text="Selected color", font=("MenLo", "11", "bold"))
        Ex3_lbl10.place(relx=0.5882154, rely=0.365)
        Ex3_lbl11 = ttk.Label(F2L_Explorer_frame, text="Select color", font=("MenLo", "11", "bold"))
        Ex3_lbl11.place(relx=0.825923, rely=0.365)

    #bind        
        self.F2L_paint_canvas.tag_bind("O0", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O0")])
        self.F2L_paint_canvas.tag_bind("O1", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O1")])
        self.F2L_paint_canvas.tag_bind("O2", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O2")])
        self.F2L_paint_canvas.tag_bind("O3", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O3")])
        self.F2L_paint_canvas.tag_bind("O5", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O5")])
        self.F2L_paint_canvas.tag_bind("O6", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O6")])
        self.F2L_paint_canvas.tag_bind("O7", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O7")])
        self.F2L_paint_canvas.tag_bind("O8", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O8")])
        self.F2L_paint_canvas.tag_bind("O9", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O9")])
        self.F2L_paint_canvas.tag_bind("O10", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O10")])
        self.F2L_paint_canvas.tag_bind("O11", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O11")])
        self.F2L_paint_canvas.tag_bind("O12", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O12")])
        self.F2L_paint_canvas.tag_bind("O14", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O14")])
        self.F2L_paint_canvas.tag_bind("O15", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O15")])
        self.F2L_paint_canvas.tag_bind("O17", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O17")])
        self.F2L_paint_canvas.tag_bind("O18", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O18")])
        self.F2L_paint_canvas.tag_bind("O20", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O20")])
        self.F2L_paint_canvas.tag_bind("O24", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O24")])
        self.F2L_paint_canvas.tag_bind("O26", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O26")])
        self.F2L_paint_canvas.tag_bind("O27", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O27")])
        self.F2L_paint_canvas.tag_bind("O28", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O28")])
        self.F2L_paint_canvas.tag_bind("O29", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O29")])
        self.F2L_paint_canvas.tag_bind("O30", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O30")])
        self.F2L_paint_canvas.tag_bind("O32", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O32")])
        self.F2L_paint_canvas.tag_bind("O33", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O33")])
        self.F2L_paint_canvas.tag_bind("O35", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O35")])
        self.F2L_paint_canvas.tag_bind("O36", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O36")])
        self.F2L_paint_canvas.tag_bind("O37", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O37")])
        self.F2L_paint_canvas.tag_bind("O38", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O38")])
        self.F2L_paint_canvas.tag_bind("O39", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O39")])
        self.F2L_paint_canvas.tag_bind("O41", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O41")])
        self.F2L_paint_canvas.tag_bind("O42", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O42")])
        self.F2L_paint_canvas.tag_bind("O44", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O44")])
        self.F2L_paint_canvas.tag_bind("O45", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O45")])
        self.F2L_paint_canvas.tag_bind("O46", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O46")])
        self.F2L_paint_canvas.tag_bind("O47", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O47")])
        self.F2L_paint_canvas.tag_bind("O48", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O48")])
        self.F2L_paint_canvas.tag_bind("O50", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O50")])
        self.F2L_paint_canvas.tag_bind("O51", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O51")])
        self.F2L_paint_canvas.tag_bind("O53", "<ButtonPress>", func=lambda event : [f2lex.Ex3_change_color(event, "O53")])

#endregion F2L_Explorer

#region sub_step_Explorer
        sub_step_Explorer_frame.grid(row=0, column=0, sticky="nsew")
    #label
        Ex4_lbl_1 = ttk.Label(sub_step_Explorer_frame, text="Designate the first searching depth (default:6)")
        Ex4_lbl_1.place(relx=0.0077, rely=0)
        Ex4_lbl_2 = ttk.Label(sub_step_Explorer_frame, text="Designate max searching depth (default:30)")
        Ex4_lbl_2.place(relx=0.0077, rely=0.075)
        Ex4_lbl_3 = ttk.Label(sub_step_Explorer_frame, text="Designate how many solutions to explore (default:50)")
        Ex4_lbl_3.place(relx=0.0077, rely=0.15)
        Ex4_lbl_4 = ttk.Label(sub_step_Explorer_frame, text="Check faces you want to use")
        Ex4_lbl_4.place(relx=0.2461538, rely=0)
        Ex4_lbl_5 = ttk.Label(sub_step_Explorer_frame, text="Use half turns")
        Ex4_lbl_5.place(relx=0.2461538, rely=0.1125)
        Ex4_lbl_6 = ttk.Label(sub_step_Explorer_frame, text="Select the orientation")
        Ex4_lbl_6.place(relx=0.2461538, rely=0.1875)
        Ex4_lbl_7 = ttk.Label(sub_step_Explorer_frame, text="and")
        Ex4_lbl_7.place(relx=0.3176923, rely=0.24375)
        Ex4_lbl_8 = ttk.Label(sub_step_Explorer_frame, text="Click to paint", font=("MenLo", "25", "bold"))
        Ex4_lbl_8.place(relx=0.687, rely=0)
        Ex4_lbl_9 = ttk.Label(sub_step_Explorer_frame, text="Put AUF and ADF into brackets")
        Ex4_lbl_9.place(relx=0.353846, rely=0.1125)
        Ex4_lbl_12 = ttk.Label(sub_step_Explorer_frame, text="Select :")
        Ex4_lbl_12.place(relx=0.593846, rely=0.5225)

    #textbox
        self.Ex4_txt_min_length = ttk.Entry(sub_step_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex4_txt_min_length.place(relx=0.0077, rely=0.0375)
        self.Ex4_txt_min_length.insert(0, "6")
        self.Ex4_txt_max_length = ttk.Entry(sub_step_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex4_txt_max_length.place(relx=0.0077, rely=0.1125)
        self.Ex4_txt_max_length.insert(0, "30")
        self.Ex4_txt_timeout = ttk.Entry(sub_step_Explorer_frame, width=round(WIDTH * 0.003846154))
        self.Ex4_txt_timeout.place(relx=0.0077, rely=0.1875)
        self.Ex4_txt_timeout.insert(0, "50")

    #checkbox
        self.Ex4_var0 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_slice_fat = ttk.Checkbutton(sub_step_Explorer_frame,variable=self.Ex4_var0,text="allow fat and slice moves",command=sub_stepex.allow_to_check)
        self.Ex4_slice_fat.place(relx=0.4, rely=0)

        self.Ex4_var1 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen1 = ttk.Checkbutton(sub_step_Explorer_frame,text="U",variable=self.Ex4_var1)
        self.Ex4_available_gen1.place(relx=0.2461538, rely=0.0375)
        self.Ex4_var1.set(1)
        # 320
        self.Ex4_var2 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen2 = ttk.Checkbutton(sub_step_Explorer_frame,text="D",variable=self.Ex4_var2)
        self.Ex4_available_gen2.place(relx=0.276923, rely=0.0375)
        self.Ex4_var2.set(1)
        # 350 -> 360
        self.Ex4_var3 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen3 = ttk.Checkbutton(sub_step_Explorer_frame,text="L",variable=self.Ex4_var3)
        self.Ex4_available_gen3.place(relx=0.3076923, rely=0.0375)
        self.Ex4_var3.set(1)
        # 380 -> 400
        self.Ex4_var4 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen4 = ttk.Checkbutton(sub_step_Explorer_frame,text="R",variable=self.Ex4_var4)
        self.Ex4_available_gen4.place(relx=0.3384615, rely=0.0375)
        self.Ex4_var4.set(1)
        # 410 -> 440
        self.Ex4_var5 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen5 = ttk.Checkbutton(sub_step_Explorer_frame,text="F",variable=self.Ex4_var5)
        self.Ex4_available_gen5.place(relx=0.36923077, rely=0.0375)
        self.Ex4_var5.set(1)
        # 440 -> 480
        self.Ex4_var6 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen6 = ttk.Checkbutton(sub_step_Explorer_frame,text="B",variable=self.Ex4_var6)
        self.Ex4_available_gen6.place(relx=0.4, rely=0.0375)
        self.Ex4_var6.set(1)
        # 470 -> 520
        self.Ex4_var7 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen7 = ttk.Checkbutton(sub_step_Explorer_frame,text="Uw",variable=self.Ex4_var7,state=tk.DISABLED)
        self.Ex4_available_gen7.place(relx=0.2461538, rely=0.075)
        self.Ex4_var7.set(0)
        # 320
        self.Ex4_var8 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen8 = ttk.Checkbutton(sub_step_Explorer_frame,text="Dw",variable=self.Ex4_var8,state=tk.DISABLED)
        self.Ex4_available_gen8.place(relx=0.276923, rely=0.075)
        self.Ex4_var8.set(0)
        # 360
        self.Ex4_var9 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen9 = ttk.Checkbutton(sub_step_Explorer_frame,text="Lw",variable=self.Ex4_var9,state=tk.DISABLED)
        self.Ex4_available_gen9.place(relx=0.3076923, rely=0.075)
        self.Ex4_var9.set(0)
        # 400
        self.Ex4_var10 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen10 = ttk.Checkbutton(sub_step_Explorer_frame,text="Rw",variable=self.Ex4_var10,state=tk.DISABLED)
        self.Ex4_available_gen10.place(relx=0.3384615, rely=0.075)
        self.Ex4_var10.set(0)
        # 440
        self.Ex4_var11 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen11 = ttk.Checkbutton(sub_step_Explorer_frame,text="Fw",variable=self.Ex4_var11,state=tk.DISABLED)
        self.Ex4_available_gen11.place(relx=0.36923077, rely=0.075)
        self.Ex4_var11.set(0)
        # 480
        self.Ex4_var12 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen12 = ttk.Checkbutton(sub_step_Explorer_frame,text="Bw",variable=self.Ex4_var12,state=tk.DISABLED)
        self.Ex4_available_gen12.place(relx=0.4, rely=0.075)
        self.Ex4_var12.set(0)
        # 520
        self.Ex4_var13 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen13 = ttk.Checkbutton(sub_step_Explorer_frame,text="M",variable=self.Ex4_var13,state=tk.DISABLED)
        self.Ex4_available_gen13.place(relx=0.43076923, rely=0.075)
        self.Ex4_var13.set(0)
        # 560
        self.Ex4_var14 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen14 = ttk.Checkbutton(sub_step_Explorer_frame,text="E",variable=self.Ex4_var14,state=tk.DISABLED)
        self.Ex4_available_gen14.place(relx=0.46153846, rely=0.075)
        self.Ex4_var14.set(0)
        # 590 -> 600
        self.Ex4_var15 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_available_gen15 = ttk.Checkbutton(sub_step_Explorer_frame,text="S",variable=self.Ex4_var15,state=tk.DISABLED)
        self.Ex4_available_gen15.place(relx=0.4923077, rely=0.075)
        self.Ex4_var15.set(0)

        self.Ex4_var16 = tk.BooleanVar(sub_step_Explorer_frame)
        self.Ex4_solution_delete = ttk.Checkbutton(sub_step_Explorer_frame,text="Check to delete recent algs",variable=self.Ex4_var16)
        self.Ex4_solution_delete.place(relx=0.35384615, rely=0.1875)
        self.Ex4_var16.set(0)

    #radiobutton
        self.htm_var4 = tk.IntVar(sub_step_Explorer_frame)
        self.htm_var4.set(0)
        usehtm_button4 = ttk.Radiobutton(sub_step_Explorer_frame, text="Yes", value=0, var=self.htm_var4, state=tk.NORMAL)
        usehtm_button4.place(relx=0.246153846, rely=0.15)
        unusehtm_button4 = ttk.Radiobutton(sub_step_Explorer_frame, text="No", value=1, var=self.htm_var4, state=tk.NORMAL)
        unusehtm_button4.place(relx=0.2923077, rely=0.15)
        self.auf_var4 = tk.IntVar(sub_step_Explorer_frame)
        self.auf_var4 = tk.IntVar(sub_step_Explorer_frame)
        self.auf_var4.set(1)
        self.usebracket_button4 = ttk.Radiobutton(sub_step_Explorer_frame, text="Yes", value=0, var=self.auf_var4)
        self.usebracket_button4.place(relx=0.35384615, rely=0.15)
        self.unusebracket_button4 = ttk.Radiobutton(sub_step_Explorer_frame, text="No", value=1, var=self.auf_var4)
        self.unusebracket_button4.place(relx=0.4, rely=0.15)
    
    #pulldown
        self.Ex4_startfrom1_sub_step_comb = ttk.Combobox(sub_step_Explorer_frame, values=startfrom1, state="readonly", width=round(WIDTH * 0.0077))
        self.Ex4_startfrom1_sub_step_comb.place(relx=0.2461538, rely=0.21875)
        self.Ex4_startfrom1_sub_step_comb.current(0)
        self.Ex4_startfrom2_sub_step_comb = ttk.Combobox(sub_step_Explorer_frame, values=startfrom2, state="readonly", width=round(WIDTH * 0.0077), )
        self.Ex4_startfrom2_sub_step_comb.place(relx=0.2461538, rely=0.26875)
        self.Ex4_startfrom2_sub_step_comb.current(0)
        self.sub_step_list = ["OLL + PLL", "OLL + CPLL", "LS + EOLL", "LS + OLL", "Advanced F2L (Adj)", "Advanced F2L (Opp)"]
        self.sub_step_var = tk.StringVar()
        self.Ex4_commbobox_sub_step = ttk.Combobox(sub_step_Explorer_frame, values=self.sub_step_list, textvariable=self.sub_step_var, state="readonly")
        self.Ex4_commbobox_sub_step.place(relx=0.633846, rely=0.5225)
        self.Ex4_commbobox_sub_step.current(0)
        self.Ex4_commbobox_sub_step.bind("<<ComboboxSelected>>", sub_stepex.select_sub_step)

    #button
        self.Button_explor_sub_step_start = ttk.Button(sub_step_Explorer_frame, text="Start", command=Rt.Explorer4_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_sub_step_start.place(relx=0.35384615, rely=0.225)
        self.Button_explor_sub_step_exit = ttk.Button(sub_step_Explorer_frame, text="Stop", command=Rt.Explorer4_Exit_thread, width=round(WIDTH * 0.003077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_sub_step_exit.place(relx=0.4153846, rely=0.225)
        self.Button_explor_sub_step_exit["state"] = tk.DISABLED
        self.Button_explor_sub_step_Reset = ttk.Button(sub_step_Explorer_frame, text="Reset", width=round(WIDTH * 0.004077), padding=[round(WIDTH * 0.01384615), round(HEIGHT * 0.0225)])
        self.Button_explor_sub_step_Reset.bind("<ButtonPress>", sub_stepex.select_sub_step)
        self.Button_explor_sub_step_Reset.place(relx=0.8953846, rely=0.52)

    #scrollbar
        self.explor_sub_step_Box = tk.Text(sub_step_Explorer_frame)
        self.explor_sub_step_Box.place(relwidth=0.461538, relheight=0.675, relx=0.0077, rely=0.3125)
        exploe_sub_step_bar_y = ttk.Scrollbar(self.explor_sub_step_Box, orient=tk.VERTICAL)
        exploe_sub_step_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        exploe_sub_step_bar_y.config(command=self.explor_sub_step_Box.yview)
        self.explor_sub_step_Box.config(yscrollcommand=exploe_sub_step_bar_y.set)

    #canvas
        self.Ex4_selected_color = "Yellow"
        self.sub_step_paint_canvas = tk.Canvas(sub_step_Explorer_frame, width=round(WIDTH * 0.36923), height=round(HEIGHT * 0.45), bg="Black")
        self.sub_step_paint_canvas.place(relx=0.5846154, rely=0.065)
        sub_stepex.Paint()
        self.sub_step_paint_canvas.tag_bind("Select_white", "<ButtonPress>", sub_stepex.Ex4_select_color_white)
        self.sub_step_paint_canvas.tag_bind("Select_yellow", "<ButtonPress>", sub_stepex.Ex4_select_color_yellow)
        self.sub_step_paint_canvas.tag_bind("Select_red", "<ButtonPress>", sub_stepex.Ex4_select_color_red)
        self.sub_step_paint_canvas.tag_bind("Select_orange", "<ButtonPress>", sub_stepex.Ex4_select_color_orange)
        self.sub_step_paint_canvas.tag_bind("Select_blue", "<ButtonPress>", sub_stepex.Ex4_select_color_blue)
        self.sub_step_paint_canvas.tag_bind("Select_green", "<ButtonPress>", sub_stepex.Ex4_select_color_green)
        Ex4_lbl10 = ttk.Label(sub_step_Explorer_frame, text="Selected color", font=("MenLo", "11", "bold"))
        Ex4_lbl10.place(relx=0.5882154, rely=0.365)
        Ex4_lbl11 = ttk.Label(sub_step_Explorer_frame, text="Select color", font=("MenLo", "11", "bold"))
        Ex4_lbl11.place(relx=0.825923, rely=0.365)

    #bind        
        self.sub_step_paint_canvas.tag_bind("P0", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P0")])
        self.sub_step_paint_canvas.tag_bind("P1", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P1")])
        self.sub_step_paint_canvas.tag_bind("P2", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P2")])
        self.sub_step_paint_canvas.tag_bind("P3", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P3")])
        self.sub_step_paint_canvas.tag_bind("P5", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P5")])
        self.sub_step_paint_canvas.tag_bind("P6", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P6")])
        self.sub_step_paint_canvas.tag_bind("P7", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P7")])
        self.sub_step_paint_canvas.tag_bind("P8", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P8")])
        self.sub_step_paint_canvas.tag_bind("P9", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P9")])
        self.sub_step_paint_canvas.tag_bind("P10", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P10")])
        self.sub_step_paint_canvas.tag_bind("P11", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P11")])
        self.sub_step_paint_canvas.tag_bind("P14", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P14")])
        self.sub_step_paint_canvas.tag_bind("P17", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P17")])
        self.sub_step_paint_canvas.tag_bind("P20", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P20")])
        self.sub_step_paint_canvas.tag_bind("P24", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P24")])
        self.sub_step_paint_canvas.tag_bind("P26", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P26")])
        self.sub_step_paint_canvas.tag_bind("P27", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P27")])
        self.sub_step_paint_canvas.tag_bind("P28", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P28")])
        self.sub_step_paint_canvas.tag_bind("P29", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P29")])
        self.sub_step_paint_canvas.tag_bind("P30", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P30")])
        self.sub_step_paint_canvas.tag_bind("P33", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P33")])
        self.sub_step_paint_canvas.tag_bind("P36", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P36")])
        self.sub_step_paint_canvas.tag_bind("P37", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P37")])
        self.sub_step_paint_canvas.tag_bind("P38", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P38")])
        self.sub_step_paint_canvas.tag_bind("P39", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P39")])
        self.sub_step_paint_canvas.tag_bind("P41", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P41")])
        self.sub_step_paint_canvas.tag_bind("P42", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P42")])
        self.sub_step_paint_canvas.tag_bind("P44", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P44")])
        self.sub_step_paint_canvas.tag_bind("P45", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P45")])
        self.sub_step_paint_canvas.tag_bind("P46", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P46")])
        self.sub_step_paint_canvas.tag_bind("P47", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P47")])
        self.sub_step_paint_canvas.tag_bind("P48", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P48")])
        self.sub_step_paint_canvas.tag_bind("P50", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P50")])
        self.sub_step_paint_canvas.tag_bind("P51", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P51")])
        self.sub_step_paint_canvas.tag_bind("P53", "<ButtonPress>", func=lambda event : [sub_stepex.Ex4_change_color(event, "P53")])

#endregion sub_step_Explorer

#region Raise
        Solver_frame.tkraise()
#endregion Raise

class Execution:
    def __init__(self):
        self.solution=""
    
    def Paint(self):
        # Canvas -> w=480, h=360
        #White
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), fill = Rt.ColorList[0]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), fill = Rt.ColorList[1]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.11111), fill = Rt.ColorList[2]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), fill = Rt.ColorList[3]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), fill = Rt.ColorList[4]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.22222), fill = Rt.ColorList[5]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.32777), fill = Rt.ColorList[6]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.32777), fill = Rt.ColorList[7]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.32777), fill = Rt.ColorList[8])
        
        #Green
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[9]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[10]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[11]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[12]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[13]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[14]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[15]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[16]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[17])
        
        #Yellow
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), fill = Rt.ColorList[18]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), fill = Rt.ColorList[19]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.77777), fill = Rt.ColorList[20]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), fill = Rt.ColorList[21]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), fill = Rt.ColorList[22]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.88888), fill = Rt.ColorList[23]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.99444), fill = Rt.ColorList[24]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.99444), fill = Rt.ColorList[25]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.99444), fill = Rt.ColorList[26])
        
        #Orange
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[27]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[28]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[29]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[30]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[31]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[32]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[33]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[34]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[35])
        
        #Red
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[36]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[37]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[38]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[39]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[40]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[41]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[42]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[43]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[44])

        #Blue
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[45]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[46]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.44444), fill = Rt.ColorList[47]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[48]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[49]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.55555), fill = Rt.ColorList[50]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[51]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[52]), \
        Rt.scramble_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.66111), fill = Rt.ColorList[53])

    def Solving_Start(self):
        Rt.var2.set(False)
        Rt.ButtonStart["state"] = tk.DISABLED
        Rt.ButtonExit["state"] = tk.NORMAL
        scramble = Rt.txt_scramble.get()
        self.scramblecheck = scramble.split()
        Scramble_List = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2",\
            "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2"]
        if scramble == "":
            Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput scramble.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.ButtonStart["state"] = tk.NORMAL
            Rt.ButtonExit["state"] = tk.DISABLED
        elif scramble[0] in ("\n", " ", "　"):
            Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nCheck the end of the scramble. New line or space is there.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.ButtonStart["state"] = tk.NORMAL
            Rt.ButtonExit["state"] = tk.DISABLED
        else:
            for i in self.scramblecheck:
                if i in Scramble_List:
                    True
                else:
                    Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                        \nCheck scramble. Unacceptable alphabet is there.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                    Rt.ButtonStart["state"] = tk.NORMAL
                    Rt.ButtonExit["state"] = tk.DISABLED
                    return

            Solution1 = Rt.txt_min_length.get()
            Solution2 = Rt.txt_max_length.get()
            self.Solution3 = Rt.txt_timeout.get()

            if Solution1 == "":
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nDesignate the first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif Solution1.isdigit() == False:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nValue Error with first searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif int(Solution1) < 1:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nInput at least '1' in first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            
            if Solution2 == "":
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nDesignate the max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif Solution2.isdigit() == False:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nValue Error with max searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif int(Solution2) < 1:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nInput at least '1' in max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            
            if exe.Solution3 == "":
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nDesignate the searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif exe.Solution3.isdigit() == False:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nValue Error with searching time. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            elif int(exe.Solution3) < 1:
                Rt.Solution_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nInput at least '1' in searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.ButtonStart["state"] = tk.NORMAL
                Rt.ButtonExit["state"] = tk.DISABLED
                return
            else:
                exe.Solution3 = float(exe.Solution3)
                if Rt.var1.get():
                    Rt.Solution_Box.delete("1.0", "end")
                Rt.ColorList = ["White","White","White","White","White","White","White","White","White", \
                "Green","Green","Green","Green","Green","Green","Green","Green","Green", \
                "Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow","Yellow", \
                "Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange","Dark Orange", \
                "Red","Red","Red","Red","Red","Red","Red","Red","Red", \
                "Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue","Blue"]
                for moves in self.scramblecheck:
                    if moves in {"U", "D", "R", "L", "F", "B"}:
                        Rt.Scramble_Print_Dictionary[moves](rotation = 1)
                    elif moves in{"U2", "D2", "R2", "L2", "F2", "B2"}:
                        Rt.Scramble_Print_Dictionary[moves](rotation = 2)
                    elif moves in {"U'", "D'", "R'", "L'", "F'", "B'"}:
                        Rt.Scramble_Print_Dictionary[moves](rotation = 3)
                exe.Paint()

                global ID

                if Rt.select_axis_var.get() == 0:
                    scrambled_state_UD = scramble2state()
                    scrambled_state_RL = scramble2state_RL()
                    scrambled_state_FB = scramble2state_FB()

                    arg_cp_UD = scrambled_state_UD.cp
                    arg_co_UD = scrambled_state_UD.co
                    arg_ep_UD = scrambled_state_UD.ep
                    arg_eo_UD = scrambled_state_UD.eo

                    arg_cp_RL = scrambled_state_RL.cp
                    arg_co_RL = scrambled_state_RL.co
                    arg_ep_RL = scrambled_state_RL.ep
                    arg_eo_RL = scrambled_state_RL.eo

                    arg_cp_FB = scrambled_state_FB.cp
                    arg_co_FB = scrambled_state_FB.co
                    arg_ep_FB = scrambled_state_FB.ep
                    arg_eo_FB = scrambled_state_FB.eo

                    arg_CP_UD = " ".join(map(str, arg_cp_UD))
                    arg_CO_UD = " ".join(map(str, arg_co_UD))
                    arg_EP_UD = " ".join(map(str, arg_ep_UD))
                    arg_EO_UD = " ".join(map(str, arg_eo_UD))

                    arg_CP_RL = " ".join(map(str, arg_cp_RL))
                    arg_CO_RL = " ".join(map(str, arg_co_RL))
                    arg_EP_RL = " ".join(map(str, arg_ep_RL))
                    arg_EO_RL = " ".join(map(str, arg_eo_RL))

                    arg_CP_FB = " ".join(map(str, arg_cp_FB))
                    arg_CO_FB = " ".join(map(str, arg_co_FB))
                    arg_EP_FB = " ".join(map(str, arg_ep_FB))
                    arg_EO_FB = " ".join(map(str, arg_eo_FB))

                    cmd = "CubeSE.exe " + arg_CP_UD + " " +  arg_CO_UD + " " + arg_EP_UD + " " + arg_EO_UD + " " + \
                        arg_CP_RL + " " + arg_CO_RL + " " + arg_EP_RL + " " + arg_EO_RL + " " + \
                            arg_CP_FB + " " + arg_CO_FB + " " + arg_EP_FB + " " + arg_EO_FB + " " + \
                                Solution1 + " " + Solution2 + " " + "0"
                    
                    #print(cmd)

                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                    Rt.Solution_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
                    #a = time.perf_counter()
                    
                    ID = root.after(int((exe.Solution3 + 1.457) * 1000), Rt.Exit_thread)
                    self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
                    for line in iter(exe.search.stdout.readline, b''):
                        #print(time.perf_counter() - a)
                        Rt.Solution_Box.insert("end", line.rstrip().decode('sjis') + "\n")
                        Rt.Solution_Box.see("end")

                    """self.solution = search.start_search(min_length = int(Solution1), \
                        max_length = int(Solution2))"""
                    #print(time.perf_counter() - a)
                    Rt.Solution_Box.insert("end", f"Finished!\n")
                    Rt.ButtonStart["state"] = tk.NORMAL
                    Rt.ButtonExit["state"] = tk.DISABLED
                    
                elif Rt.select_axis_var.get() == 1:
                    scrambled_state = scramble2state()
                    arg_cp = scrambled_state.cp
                    arg_co = scrambled_state.co
                    arg_ep = scrambled_state.ep
                    arg_eo = scrambled_state.eo

                    arg_CP = " ".join(map(str, arg_cp))
                    arg_CO = " ".join(map(str, arg_co))
                    arg_EP = " ".join(map(str, arg_ep))
                    arg_EO = " ".join(map(str, arg_eo))

                    cmd = "CubeSE.exe " + arg_CP + " " +  arg_CO + " " + arg_EP + " " + arg_EO + " " + Solution1 + " " + Solution2 + " " + "1"
                    
                    #print(cmd)
                    
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                    Rt.Solution_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
                    #a = time.perf_counter()

                    ID = root.after(int((exe.Solution3 + 1.457) * 1000), Rt.Exit_thread)
                    self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
                    for line in iter(exe.search.stdout.readline, b''):
                        #print(time.perf_counter() - a)
                        Rt.Solution_Box.insert("end", line.rstrip().decode('sjis') + "\n")
                        Rt.Solution_Box.see("end")

                    """self.solution = search.start_search(min_length = int(Solution1), \
                        max_length = int(Solution2))"""
                    #print(time.perf_counter() - a)
                    Rt.Solution_Box.insert("end", f"Finished!\n")
                    Rt.ButtonStart["state"] = tk.NORMAL
                    Rt.ButtonExit["state"] = tk.DISABLED

                elif Rt.select_axis_var.get() == 2:
                    scrambled_state = scramble2state_RL()
                    arg_cp = scrambled_state.cp
                    arg_co = scrambled_state.co
                    arg_ep = scrambled_state.ep
                    arg_eo = scrambled_state.eo

                    arg_CP = " ".join(map(str, arg_cp))
                    arg_CO = " ".join(map(str, arg_co))
                    arg_EP = " ".join(map(str, arg_ep))
                    arg_EO = " ".join(map(str, arg_eo))

                    cmd = "CubeSE.exe " + arg_CP + " " +  arg_CO + " " + arg_EP + " " + arg_EO + " " + Solution1 + " " + Solution2 + " " + "2"

                    #print(cmd)

                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                    Rt.Solution_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
                    #a = time.perf_counter()

                    ID = root.after(int((exe.Solution3 + 1.457) * 1000), Rt.Exit_thread)
                    self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
                    for line in iter(exe.search.stdout.readline, b''):
                        #print(time.perf_counter() - a)
                        Rt.Solution_Box.insert("end", line.rstrip().decode('sjis') + "\n")
                        Rt.Solution_Box.see("end")

                    """self.solution = search.start_search(min_length = int(Solution1), \
                        max_length = int(Solution2))"""
                    #print(time.perf_counter() - a)
                    Rt.Solution_Box.insert("end", f"Finished!\n")
                    Rt.ButtonStart["state"] = tk.NORMAL
                    Rt.ButtonExit["state"] = tk.DISABLED

                elif Rt.select_axis_var.get() == 3:
                    scrambled_state = scramble2state_FB()
                    arg_cp = scrambled_state.cp
                    arg_co = scrambled_state.co
                    arg_ep = scrambled_state.ep
                    arg_eo = scrambled_state.eo

                    arg_CP = " ".join(map(str, arg_cp))
                    arg_CO = " ".join(map(str, arg_co))
                    arg_EP = " ".join(map(str, arg_ep))
                    arg_EO = " ".join(map(str, arg_eo))

                    cmd = "CubeSE.exe " + arg_CP + " " +  arg_CO + " " + arg_EP + " " + arg_EO + " " + Solution1 + " " + Solution2 + " " + "3"

                    #print(cmd)

                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                    Rt.Solution_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
                    #a = time.perf_counter()

                    ID = root.after(int((exe.Solution3 + 1.457) * 1000), Rt.Exit_thread)
                    self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
                    for line in iter(exe.search.stdout.readline, b''):
                        #print(time.perf_counter() - a)
                        Rt.Solution_Box.insert("end", line.rstrip().decode('sjis') + "\n")
                        Rt.Solution_Box.see("end")

                    """self.solution = search.start_search(min_length = int(Solution1), \
                        max_length = int(Solution2))"""
                    #print(time.perf_counter() - a)
                    Rt.Solution_Box.insert("end", f"Finished!\n")
                    Rt.ButtonStart["state"] = tk.NORMAL
                    Rt.ButtonExit["state"] = tk.DISABLED

class B_Execution:
    def __init__(self):
        self.lbltext = tk.StringVar()
        self.cp = []
        self.co = []
        self.ep = []
        self.eo = []

    def Show_Rotation_pic(self, index):
        move_name_list = ["U", "U2", "U'", "D", "D2", "D'", "R", "R2", "R'", "L", "L2", "L'", "F", "F2", "F'", "B", "B2", "B'", "Hide"]
        global show_rotation_path
        show_rotation_path = ("RP\\" + move_name_list[index])
        Rt.rotation_image = Image.open(show_rotation_path + ".png")
        Rt.resize_image = Rt.rotation_image.resize((round(WIDTH * 0.36923077), round(HEIGHT * 0.3375)))
        Rt.show_rotation_img = ImageTk.PhotoImage(Rt.resize_image)
        Rt.show_img.config(image=Rt.show_rotation_img)
        # Rt.show_rotation_img.config(file=show_rotation_path + ".png")
        # print(Rt.show_rotation_img.width())
        # print(Rt.show_rotation_img.height())

    def check_parity(self, cp, ep):
        cp_counter = 0
        ep_counter = 0
        for i in range(8):
            if i == cp[i]:
                continue
            left = cp[i]
            min_e = min(cp[i+1:])
            min_e_index = cp.index(min_e)
            cp[i], cp[min_e_index] = min_e, left
            cp_counter+=1
        
        for k in range(12):
            if k == ep[k]:
                continue
            left2 = ep[k]
            min_e2 = min(ep[k+1:])
            min_e_index2 = ep.index(min_e2)
            ep[k], ep[min_e_index2] = min_e2, left2
            ep_counter+=1
        
        if cp_counter % 2 == ep_counter % 2:
            return True
        else:
            return False

    def dicision(self):
        #a = tm.perf_counter()
        self.cp = []
        self.co = []
        self.ep = []
        self.eo = []
        Rt.B_Start_Button["state"] = DISABLED
        self.index_color_cp_list = [{"White", "Blue", "Dark Orange"}, {"White", "Blue", "Red"}, 
                                    {"White", "Green", "Red"}, {"White", "Green", "Dark Orange"},
                                    {"Yellow", "Blue", "Dark Orange"}, {"Yellow", "Blue", "Red"},
                                    {"Yellow", "Green", "Red"}, {"Yellow", "Green", "Dark Orange"}]
        self.index_color_ep_list = [{"Blue", "Dark Orange"}, {"Blue", "Red"},
                                    {"Green", "Red"}, {"Green", "Dark Orange"},
                                    {"White", "Blue"}, {"White", "Red"},
                                    {"White", "Green"}, {"White", "Dark Orange"},
                                    {"Yellow", "Blue"}, {"Yellow", "Red"},
                                    {"Yellow", "Green"}, {"Yellow", "Dark Orange"}]


        if {Rt.B_paint_canvas.itemcget("N0", "fill"), Rt.B_paint_canvas.itemcget("N27", "fill"), Rt.B_paint_canvas.itemcget("N47", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N0", "fill"), Rt.B_paint_canvas.itemcget("N27", "fill"), Rt.B_paint_canvas.itemcget("N47", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N2", "fill"), Rt.B_paint_canvas.itemcget("N38", "fill"), Rt.B_paint_canvas.itemcget("N45", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N2", "fill"), Rt.B_paint_canvas.itemcget("N38", "fill"), Rt.B_paint_canvas.itemcget("N45", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N8", "fill"), Rt.B_paint_canvas.itemcget("N11", "fill"), Rt.B_paint_canvas.itemcget("N36", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N8", "fill"), Rt.B_paint_canvas.itemcget("N11", "fill"), Rt.B_paint_canvas.itemcget("N36", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N6", "fill"), Rt.B_paint_canvas.itemcget("N29", "fill"), Rt.B_paint_canvas.itemcget("N9", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N6", "fill"), Rt.B_paint_canvas.itemcget("N29", "fill"), Rt.B_paint_canvas.itemcget("N9", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N24", "fill"), Rt.B_paint_canvas.itemcget("N53", "fill"), Rt.B_paint_canvas.itemcget("N33", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N24", "fill"), Rt.B_paint_canvas.itemcget("N53", "fill"), Rt.B_paint_canvas.itemcget("N33", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N26", "fill"), Rt.B_paint_canvas.itemcget("N44", "fill"), Rt.B_paint_canvas.itemcget("N51", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N26", "fill"), Rt.B_paint_canvas.itemcget("N44", "fill"), Rt.B_paint_canvas.itemcget("N51", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N20", "fill"), Rt.B_paint_canvas.itemcget("N17", "fill"), Rt.B_paint_canvas.itemcget("N42", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N20", "fill"), Rt.B_paint_canvas.itemcget("N17", "fill"), Rt.B_paint_canvas.itemcget("N42", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N18", "fill"), Rt.B_paint_canvas.itemcget("N15", "fill"), Rt.B_paint_canvas.itemcget("N35", "fill")} in self.index_color_cp_list:
            self.cp.append(self.index_color_cp_list.index({Rt.B_paint_canvas.itemcget("N18", "fill"), Rt.B_paint_canvas.itemcget("N15", "fill"), Rt.B_paint_canvas.itemcget("N35", "fill")}))

        if len(set(self.cp)) != 8:
            bexe.lbltext.set("Some thing is wrong with colors of corners.")
            Rt.B_Start_Button["state"] = NORMAL
            return False
        #b = tm.perf_counter()
        if {Rt.B_paint_canvas.itemcget("N50", "fill"), Rt.B_paint_canvas.itemcget("N30", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N50", "fill"), Rt.B_paint_canvas.itemcget("N30", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N48", "fill"), Rt.B_paint_canvas.itemcget("N41", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N48", "fill"), Rt.B_paint_canvas.itemcget("N41", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N14", "fill"), Rt.B_paint_canvas.itemcget("N39", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N14", "fill"), Rt.B_paint_canvas.itemcget("N39", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N12", "fill"), Rt.B_paint_canvas.itemcget("N32", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N12", "fill"), Rt.B_paint_canvas.itemcget("N32", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N1", "fill"), Rt.B_paint_canvas.itemcget("N46", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N1", "fill"), Rt.B_paint_canvas.itemcget("N46", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N5", "fill"), Rt.B_paint_canvas.itemcget("N37", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N5", "fill"), Rt.B_paint_canvas.itemcget("N37", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N7", "fill"), Rt.B_paint_canvas.itemcget("N10", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N7", "fill"), Rt.B_paint_canvas.itemcget("N10", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N3", "fill"), Rt.B_paint_canvas.itemcget("N28", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N3", "fill"), Rt.B_paint_canvas.itemcget("N28", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N25", "fill"), Rt.B_paint_canvas.itemcget("N52", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N25", "fill"), Rt.B_paint_canvas.itemcget("N52", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N23", "fill"), Rt.B_paint_canvas.itemcget("N43", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N23", "fill"), Rt.B_paint_canvas.itemcget("N43", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N19", "fill"), Rt.B_paint_canvas.itemcget("N16", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N19", "fill"), Rt.B_paint_canvas.itemcget("N16", "fill")}))
        if {Rt.B_paint_canvas.itemcget("N21", "fill"), Rt.B_paint_canvas.itemcget("N34", "fill")} in self.index_color_ep_list:
            self.ep.append(self.index_color_ep_list.index({Rt.B_paint_canvas.itemcget("N21", "fill"), Rt.B_paint_canvas.itemcget("N34", "fill")}))
        
        if len(set(self.ep)) != 12:
            bexe.lbltext.set("Some thing is wrong with colors of edges.")
            Rt.B_Start_Button["state"] = NORMAL
            return False
        #c = tm.perf_counter()
        if Rt.B_paint_canvas.itemcget("N0", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N27", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N2", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N45", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N8", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N36", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N6", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N9", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N24", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N53", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N26", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N44", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N20", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N17", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)
        if Rt.B_paint_canvas.itemcget("N18", "fill") in {"White", "Yellow"}:
            self.co.append(0)
        elif Rt.B_paint_canvas.itemcget("N35", "fill") in {"White", "Yellow"}:
            self.co.append(1)
        else:
            self.co.append(2)

        if sum(self.co) % 3 != 0:
            bexe.lbltext.set("Some thing is wrong with colors of corners.")
            Rt.B_Start_Button["state"] = NORMAL
            return False
        #d = tm.perf_counter()
        if "White" in {Rt.B_paint_canvas.itemcget("N50", "fill"), Rt.B_paint_canvas.itemcget("N30", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N50", "fill"), Rt.B_paint_canvas.itemcget("N30", "fill")}:
            if Rt.B_paint_canvas.itemcget("N50", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N50", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if ("White" in {Rt.B_paint_canvas.itemcget("N48", "fill"), Rt.B_paint_canvas.itemcget("N41", "fill")}) or ("Yellow" in {Rt.B_paint_canvas.itemcget("N48", "fill"), Rt.B_paint_canvas.itemcget("N41", "fill")}):
            if Rt.B_paint_canvas.itemcget("N48", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N48", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N14", "fill"), Rt.B_paint_canvas.itemcget("N39", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N14", "fill"), Rt.B_paint_canvas.itemcget("N39", "fill")}:
            if Rt.B_paint_canvas.itemcget("N14", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N14", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N12", "fill"), Rt.B_paint_canvas.itemcget("N32", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N12", "fill"), Rt.B_paint_canvas.itemcget("N32", "fill")}:
            if Rt.B_paint_canvas.itemcget("N12", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N12", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N1", "fill"), Rt.B_paint_canvas.itemcget("N46", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N1", "fill"), Rt.B_paint_canvas.itemcget("N46", "fill")}:
            if Rt.B_paint_canvas.itemcget("N1", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N1", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N5", "fill"), Rt.B_paint_canvas.itemcget("N37", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N5", "fill"), Rt.B_paint_canvas.itemcget("N37", "fill")}:
            if Rt.B_paint_canvas.itemcget("N5", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N5", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N10", "fill"), Rt.B_paint_canvas.itemcget("N7", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N10", "fill"), Rt.B_paint_canvas.itemcget("N7", "fill")}:
            if Rt.B_paint_canvas.itemcget("N7", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N7", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N3", "fill"), Rt.B_paint_canvas.itemcget("N28", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N3", "fill"), Rt.B_paint_canvas.itemcget("N28", "fill")}:
            if Rt.B_paint_canvas.itemcget("N3", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N3", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N25", "fill"), Rt.B_paint_canvas.itemcget("N52", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N25", "fill"), Rt.B_paint_canvas.itemcget("N52", "fill")}:
            if Rt.B_paint_canvas.itemcget("N25", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N25", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N23", "fill"), Rt.B_paint_canvas.itemcget("N43", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N23", "fill"), Rt.B_paint_canvas.itemcget("N43", "fill")}:
            if Rt.B_paint_canvas.itemcget("N23", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N23", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N19", "fill"), Rt.B_paint_canvas.itemcget("N16", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N19", "fill"), Rt.B_paint_canvas.itemcget("N16", "fill")}:
            if Rt.B_paint_canvas.itemcget("N19", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N19", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)
        if "White" in {Rt.B_paint_canvas.itemcget("N21", "fill"), Rt.B_paint_canvas.itemcget("N34", "fill")} or "Yellow" in {Rt.B_paint_canvas.itemcget("N21", "fill"), Rt.B_paint_canvas.itemcget("N34", "fill")}:
            if Rt.B_paint_canvas.itemcget("N21", "fill") in {"White", "Yellow"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
        elif Rt.B_paint_canvas.itemcget("N21", "fill") in {"Green", "Blue"}:
            self.eo.append(0)
        else:
            self.eo.append(1)

        if sum(self.eo) % 2 != 0:
            bexe.lbltext.set("Some thing is wrong with colors of edges.")
            Rt.B_Start_Button["state"] = NORMAL
            return False
        #e = tm.perf_counter()
        arg_cp = list(self.cp)
        arg_ep = list(self.ep)

        if not bexe.check_parity(arg_cp, arg_ep):
            bexe.lbltext.set("Some thing is wrong or this Rubik's cube cannot solve.")
            Rt.B_Start_Button["state"] = NORMAL
            return False
        #f = tm.perf_counter()
        arg_CP = " ".join(map(str, self.cp))
        arg_CO = " ".join(map(str, self.co))
        arg_EP = " ".join(map(str, self.ep))
        arg_EO = " ".join(map(str, self.eo))

        cmd = "CubeSE.exe " + arg_CP + " " +  arg_CO + " " + arg_EP + " " + arg_EO + " " + "1" + " " + "23" + " " + "4"
        #g = tm.perf_counter()
        #print(arg_CP + " " +  arg_CO + " " + arg_EP + " " + arg_EO)
        #h = tm.perf_counter()
        #print(cmd)
        self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        for line in iter(bexe.search.stdout.readline, b''):
            #print(time.perf_counter() - a)
            self.lbltext.set(line.rstrip().decode('sjis'))
        Rt.B_Start_Button["state"] = NORMAL
        #print(h-g, g-f, f-e, e-d, d-c, c-b, b-a)

    def B_Paint(self):
        # 720 540
        #U
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.003703), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.111111), fill="Gray", tags="N0")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.003703), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.111111), fill="Gray", tags="N1")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.003703), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.111111), fill="Gray", tags="N2")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.111111), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.222222), fill="Gray", tags="N3")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.111111), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.222222), fill="White")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.111111), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.222222), fill="Gray", tags="N5")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.222222), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.32963), fill="Gray", tags="N6")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.222222), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.32963), fill="Gray", tags="N7")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.222222), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.32963), fill="Gray", tags="N8")
        #F
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N9")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N10")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N11")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N12")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.55555), fill="Green")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N14")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N15")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N16")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N17")
        #D
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.67037), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.77777), fill="Gray", tags="N18")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.67037), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.77777), fill="Gray", tags="N19")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.67037), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.77777), fill="Gray", tags="N20")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.88888), fill="Gray", tags="N21")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.88888), fill="Yellow")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.77777), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.88888), fill="Gray", tags="N23")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.25277), round(BCVHEIGHT * 0.88888), round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.99629), fill="Gray", tags="N24")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.33333), round(BCVHEIGHT * 0.88888), round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.99629), fill="Gray", tags="N25")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.41666), round(BCVHEIGHT * 0.88888), round(BCVWIDTH * 0.49722), round(BCVHEIGHT * 0.99629), fill="Gray", tags="N26")
        #L
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.0027777), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N27")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N28")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.24722), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N29")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.0027777), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N30")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.55555), fill="Dark Orange")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.24722), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N32")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.0027777), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N33")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.083333), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N34")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.1666), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.24722), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N35")
        #R
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.50277), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N36")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N37")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.74722), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N38")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.50277), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N39")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.55555), fill="Red")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.74722), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N41")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.50277), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N42")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.58333), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N43")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.66666), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.74722), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N44")
        #B
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.75277), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N45")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N46")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.33703), round(BCVWIDTH * 0.99722), round(BCVHEIGHT * 0.44444), fill="Gray", tags="N47")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.75277), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N48")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.55555), fill="Blue")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.44444), round(BCVWIDTH * 0.99722), round(BCVHEIGHT * 0.55555), fill="Gray", tags="N50")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.75277), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N51")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.83333), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N52")
        Rt.B_paint_canvas.create_rectangle(round(BCVWIDTH * 0.91666), round(BCVHEIGHT * 0.55555), round(BCVWIDTH * 0.99722), round(BCVHEIGHT * 0.662963), fill="Gray", tags="N53")

    def B_Paint_reset(self):
        for i in range(54):
            if i in (4, 13, 22, 31, 40, 49):
                pass
            else:
                Rt.B_paint_canvas.itemconfig("N" + str(i), fill="Gray")

    def B_Paint_solved(self):
        #U
        for i in range(8):
            Rt.B_selected_color = "White"
            Rt.B_paint_canvas.itemconfig("N0", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N1", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N2", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N3", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N5", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N6", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N7", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N8", fill=Rt.B_selected_color)
        #F
        for i in range(8):
            Rt.B_selected_color = "Green"
            Rt.B_paint_canvas.itemconfig("N9", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N10", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N11", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N12", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N14", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N15", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N16", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N17", fill=Rt.B_selected_color)
        #D
        for i in range(8):
            Rt.B_selected_color = "Yellow"
            Rt.B_paint_canvas.itemconfig("N18", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N19", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N20", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N21", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N23", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N24", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N25", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N26", fill=Rt.B_selected_color)
        #L
        for i in range(8):
            Rt.B_selected_color = "Dark Orange"
            Rt.B_paint_canvas.itemconfig("N27", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N28", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N29", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N30", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N32", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N33", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N34", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N35", fill=Rt.B_selected_color)
        #R
        for i in range(8):
            Rt.B_selected_color = "Red"
            Rt.B_paint_canvas.itemconfig("N36", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N37", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N38", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N39", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N41", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N42", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N43", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N44", fill=Rt.B_selected_color)
        #B
        for i in range(8):
            Rt.B_selected_color = "Blue"
            Rt.B_paint_canvas.itemconfig("N45", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N46", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N47", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N48", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N50", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N51", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N52", fill=Rt.B_selected_color)
            Rt.B_paint_canvas.itemconfig("N53", fill=Rt.B_selected_color)
        Rt.B_selected_color = "White"
        Rt.B_paint_canvas.itemconfig("show", fill = "White")

    def B_change_color(self, event, arg):
        event.widget.itemconfig(arg, fill = Rt.B_selected_color)

    def B_select_color_white(self, event):
        Rt.B_selected_color = "White"
        event.widget.itemconfig("show", fill=Rt.B_selected_color)

    def B_select_color_yellow(self, event):
        Rt.B_selected_color = "Yellow"
        event.widget.itemconfig("show", fill = Rt.B_selected_color)

    def B_select_color_red(self, event):
        Rt.B_selected_color = "Red"
        event.widget.itemconfig("show", fill = Rt.B_selected_color)

    def B_select_color_orange(self, event):
        Rt.B_selected_color = "Dark Orange"
        event.widget.itemconfig("show", fill = Rt.B_selected_color)

    def B_select_color_blue(self, event):
        Rt.B_selected_color = "Blue"
        event.widget.itemconfig("show", fill = Rt.B_selected_color)

    def B_select_color_green(self, event):
        Rt.B_selected_color = "Green"
        event.widget.itemconfig("show", fill = Rt.B_selected_color)

class PLL_Ex:
    PLL_args = [
        #Aa
        [
            "1 2 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 5 1 6 7 0 0 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 2 4 5 3 7 0 0 1 2 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 2 3 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 0 2 3 4 1 6 7 0 2 0 0 0 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 7 2 0 0 1 0 0 0 2 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "2 1 3 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 0 2 3 1 5 6 7 1 2 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 7 3 0 0 0 0 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 3 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 5 0 6 7 1 0 0 0 2 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 2 4 5 6 3 0 0 0 2 0 0 0 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Ab
        [
            "2 0 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 1 4 6 7 0 2 0 0 0 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 6 4 5 2 7 0 0 1 0 0 0 2 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 3 1 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 5 2 3 4 0 6 7 1 2 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 2 6 0 0 0 0 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "3 1 0 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 4 2 3 0 5 6 7 1 0 0 0 2 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 3 6 0 0 0 2 0 0 0 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "3 0 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 0 4 6 7 0 0 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 7 4 5 6 2 0 0 1 2 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #E
        [
            "3 2 1 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 5 2 3 0 1 6 7 1 2 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 7 4 5 2 3 0 0 1 2 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 5 4 6 7 1 2 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 7 6 0 0 1 2 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "3 2 1 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 5 2 3 0 1 6 7 1 2 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 7 4 5 2 3 0 0 1 2 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 5 4 6 7 1 2 0 0 2 1 0 0 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 7 6 0 0 1 2 0 0 2 1 0 1 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #F
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Ga
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 7 5 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 8 0 2 3 1 5 6 7 4 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 3 6 4 5 10 7 8 9 2 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 7 4 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 4 0 2 3 8 5 6 7 1 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 3 10 4 5 2 7 8 9 6 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 6 4 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 1 4 2 3 8 5 6 7 0 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 10 2 4 5 3 7 8 9 6 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 4 7 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 1 8 2 3 0 5 6 7 4 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 6 2 4 5 10 7 8 9 3 11 0 0 1 0 0 0 0 0 0 0 1 0"
        ],
        #Gb
        [
            "3 0 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 7 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 0 4 6 7 0 0 0 0 2 1 0 0 8 0 2 3 4 5 6 7 1 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 3 7 4 5 6 2 0 0 1 2 0 0 0 0 0 1 3 6 4 5 2 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "2 0 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 6 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 1 4 6 7 0 2 0 0 0 1 0 0 0 4 2 3 8 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 3 6 4 5 2 7 0 0 1 0 0 0 2 0 0 1 10 3 4 5 2 7 8 9 6 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "0 3 1 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 7 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 5 2 3 4 0 6 7 1 2 0 0 0 0 0 0 1 4 2 3 0 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 2 6 0 0 0 0 0 0 2 1 0 1 10 2 4 5 6 7 8 9 3 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "3 1 0 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 7 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 4 2 3 0 5 6 7 1 0 0 0 2 0 0 0 8 1 2 3 0 5 6 7 4 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 3 6 0 0 0 2 0 0 0 1 0 1 2 6 4 5 10 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0 1"
        ],
        #Gc
        [
            "2 0 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 7 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 1 4 6 7 0 2 0 0 0 1 0 0 8 0 2 3 4 5 6 7 1 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 3 6 4 5 2 7 0 0 1 0 0 0 2 0 0 1 3 6 4 5 2 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "0 3 1 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 6 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 5 2 3 4 0 6 7 1 2 0 0 0 0 0 0 0 4 2 3 8 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 7 3 4 5 2 6 0 0 0 0 0 0 2 1 0 1 10 3 4 5 2 7 8 9 6 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "3 1 0 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 7 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 4 2 3 0 5 6 7 1 0 0 0 2 0 0 0 1 4 2 3 0 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 3 6 0 0 0 2 0 0 0 1 0 1 10 2 4 5 6 7 8 9 3 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "3 0 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 7 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 0 4 6 7 0 0 0 0 2 1 0 0 8 1 2 3 0 5 6 7 4 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 3 7 4 5 6 2 0 0 1 2 0 0 0 0 0 1 2 6 4 5 10 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0"
        ],
        #Gd
        [
            "1 2 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 4 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 5 1 6 7 0 0 0 0 2 1 0 0 1 8 2 3 4 5 6 7 0 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 6 2 4 5 3 7 0 0 1 2 0 0 0 0 0 1 6 2 4 5 3 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "0 2 3 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 4 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 0 2 3 4 1 6 7 0 2 0 0 0 1 0 0 0 8 2 3 1 5 6 7 4 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 7 2 0 0 1 0 0 0 2 0 0 1 6 3 4 5 10 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "2 1 3 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 5 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 0 2 3 1 5 6 7 1 2 0 0 0 0 0 0 4 0 2 3 1 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 7 3 0 0 0 0 0 0 2 1 0 1 3 10 4 5 6 7 8 9 2 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "1 3 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 4 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 5 0 6 7 1 0 0 0 2 0 0 0 4 1 2 3 8 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 7 2 4 5 6 3 0 0 0 2 0 0 0 1 0 1 2 10 4 5 3 7 8 9 6 11 0 0 0 1 0 0 1 0 0 0 0 0"
        ],
        #H
        [
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 7 4 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 7 4 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 7 4 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 7 4 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Ja
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0"
        ],
        #Jb
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0"
        ],
        #Na
        [
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Nb
        [
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Ra
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0"
        ],
        #Rb
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0"
        ],
        #T
        [
            "0 2 1 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 5 2 3 4 1 6 7 0 2 0 0 0 1 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 6 3 4 5 2 7 0 0 1 0 0 0 2 0 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 1 2 0 0 0 0 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 7 6 0 0 0 0 0 0 2 1 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "3 1 2 0 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "4 1 2 3 0 5 6 7 1 0 0 0 2 0 0 0 1 0 2 3 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 7 4 5 6 3 0 0 0 2 0 0 0 1 0 1 3 2 4 5 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "1 0 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 5 4 6 7 0 0 0 0 2 1 0 0 0 1 2 3 8 5 6 7 4 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 3 2 4 5 6 7 0 0 1 2 0 0 0 0 0 1 2 3 4 5 10 7 8 9 6 11 0 0 0 0 0 0 0 0 0 0 0 0"
        ],
        #Ua
        [
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 7 5 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 4 0 2 3 1 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 10 4 5 6 7 8 9 2 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 4 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 4 1 2 3 8 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 10 4 5 3 7 8 9 6 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 4 6 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 8 2 3 4 5 6 7 0 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 6 2 4 5 3 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 4 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 8 2 3 1 5 6 7 4 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 6 3 4 5 10 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0"
        ],
        #Ub
        [
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 7 5 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 1 4 2 3 0 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 10 2 4 5 6 7 8 9 3 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 6 5 7 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 8 1 2 3 0 5 6 7 4 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 6 4 5 10 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 7 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 8 0 2 3 4 5 6 7 1 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 3 6 4 5 2 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 6 4 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 4 2 3 8 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 10 3 4 5 2 7 8 9 6 11 0 0 1 0 0 0 1 0 0 0 0 0"
        ],
        #V
        [
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0"
        ],
        #Y
        [
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 5 6 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 8 1 2 3 4 5 6 7 0 9 10 11 1 0 0 0 0 0 0 0 1 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 2 6 4 5 3 7 8 9 10 11 0 0 0 1 0 0 1 0 0 0 0 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 6 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 0 8 2 3 4 5 6 7 1 9 10 11 0 1 0 0 0 0 0 0 1 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 6 3 4 5 2 7 8 9 10 11 0 0 1 0 0 0 1 0 0 0 0 0",
            "2 1 0 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 6 5 7 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 4 2 3 1 5 6 7 0 0 0 0 0 0 0 0 0 4 2 3 1 5 6 7 8 9 10 11 0 1 0 0 1 0 0 0 0 0 0 0",
            "0 1 2 6 4 5 3 7 0 0 0 0 0 0 0 0 0 1 10 3 4 5 6 7 8 9 2 11 0 0 1 0 0 0 0 0 0 0 1 0",
            "0 3 2 1 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 4 5 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "5 1 2 3 4 0 6 7 0 0 0 0 0 0 0 0 4 1 2 3 0 5 6 7 8 9 10 11 1 0 0 0 1 0 0 0 0 0 0 0",
            "0 1 7 3 4 5 6 2 0 0 0 0 0 0 0 0 0 1 2 10 4 5 6 7 8 9 3 11 0 0 0 1 0 0 0 0 0 0 1 0"
        ],
        #Z
        [
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 6 5 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 8 4 2 3 1 5 6 7 0 9 10 11 1 1 0 0 1 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 10 6 4 5 3 7 8 9 2 11 0 0 1 1 0 0 1 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 4 8 2 3 0 5 6 7 1 9 10 11 1 1 0 0 1 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 6 10 4 5 2 7 8 9 3 11 0 0 1 1 0 0 1 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 7 6 5 4 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 8 4 2 3 1 5 6 7 0 9 10 11 1 1 0 0 1 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 10 6 4 5 3 7 8 9 2 11 0 0 1 1 0 0 1 0 0 0 1 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 2 3 5 4 7 6 8 9 10 11 0 0 0 0 0 0 0 0 0 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 4 8 2 3 0 5 6 7 1 9 10 11 1 1 0 0 1 0 0 0 1 0 0 0",
            "0 1 2 3 4 5 6 7 0 0 0 0 0 0 0 0 0 1 6 10 4 5 2 7 8 9 3 11 0 0 1 1 0 0 1 0 0 0 1 0"
        ]
    ]

    def showPLLpic(self, event):
        Rt.selected_PLL.set("Selected PLL : " + Rt.Ex_commbobox_PLL.get())
        global show_PLL_path
        show_PLL_path = Rt.Ex_commbobox_PLL.get()
        Rt.PLL_image = Image.open("RP\\" + show_PLL_path + "perm.png")
        Rt.resize_image_PLL = Rt.PLL_image.resize((round(WIDTH * 0.473077), round(HEIGHT * 0.76875)))
        Rt.show_PLL_img = ImageTk.PhotoImage(Rt.resize_image_PLL)
        Rt.show_img2.config(image=Rt.show_PLL_img)
        # print(Rt.show_PLL_pic.height())
        # print(Rt.show_PLL_pic.width())

    def PLLarg_dicision(self):
        # global ID !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Rt.Button_explor_PLL_exit["state"] = tk.NORMAL
        Rt.Button_explor_PLL_start["state"] = tk.DISABLED
        if Rt.Ex_var16.get():
            Rt.explor_PLL_Box.delete("1.0", "end")

        i = Rt.Ex_commbobox_PLL.current()
        j = Rt.Ex_startfrom1_PLL_comb.current() * 3 + Rt.Ex_startfrom2_PLL_comb.current()

        Solution1 = Rt.Ex_txt_min_length.get()
        Solution2 = Rt.Ex_txt_max_length.get()
        Solution3 = Rt.Ex_txt_timeout.get()

        if Solution1 == "":
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif Solution1.isdigit() == False:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with first searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution1) < 1:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        
        if Solution2 == "":
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif Solution2.isdigit() == False:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with max searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution2) < 1:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        
        if Solution3 == "":
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif Solution3.isdigit() == False:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with searching time. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution3) < 1:
            Rt.explor_PLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_PLL_start["state"] = tk.NORMAL
            Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
            return

        Ex_available_list = [str(int(Rt.Ex_var1.get())),
                        str(int(Rt.Ex_var2.get())),
                        str(int(Rt.Ex_var3.get())),
                        str(int(Rt.Ex_var4.get())),
                        str(int(Rt.Ex_var5.get())),
                        str(int(Rt.Ex_var6.get())),
                        str(int(Rt.Ex_var7.get())),
                        str(int(Rt.Ex_var8.get())),
                        str(int(Rt.Ex_var9.get())),
                        str(int(Rt.Ex_var10.get())),
                        str(int(Rt.Ex_var11.get())),
                        str(int(Rt.Ex_var12.get())),
                        str(int(Rt.Ex_var13.get())),
                        str(int(Rt.Ex_var14.get())),
                        str(int(Rt.Ex_var15.get()))
                        ]

        forbid_list = [0, 15, 12]
        forbidden = str(forbid_list[j % 3])

        cmd = "CubeSE.exe " + pllex.PLL_args[i][j] + " 0 1 2 3 4 5 " + " ".join(Ex_available_list) + " " + Solution1 + " " + Solution2 + " " + Solution3 + " " + str(int(Rt.Ex_var0.get()) * 2 + Rt.htm_var.get()) + " " + forbidden + " " + str(Rt.auf_var.get()) + " 0"

        # print(cmd)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        Rt.explor_PLL_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
        #a = time.perf_counter()

        #ID = root.after(int((Solution3 + 1.457) * 1000), Rt.Explorer_Exit_thread)

        self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
        for line in iter(pllex.search.stdout.readline, b''):
            #print(time.perf_counter() - a)
            Rt.explor_PLL_Box.insert("end", line.rstrip().decode('sjis') + "\n")
            Rt.explor_PLL_Box.see("end")

        """self.solution = search.start_search(min_length = int(Solution1), \
            max_length = int(Solution2))"""
        #print(time.perf_counter() - a)
        Rt.explor_PLL_Box.insert("end", f"Finished!\n")
        Rt.Button_explor_PLL_start["state"] = tk.NORMAL
        Rt.Button_explor_PLL_exit["state"] = tk.DISABLED
    
    def allow_to_check(self):
        if Rt.Ex_var0.get():
            Rt.Ex_available_gen7["state"] = tk.NORMAL
            Rt.Ex_available_gen8["state"] = tk.NORMAL
            Rt.Ex_available_gen9["state"] = tk.NORMAL
            Rt.Ex_available_gen10["state"] = tk.NORMAL
            Rt.Ex_available_gen11["state"] = tk.NORMAL
            Rt.Ex_available_gen12["state"] = tk.NORMAL
            Rt.Ex_available_gen13["state"] = tk.NORMAL
            Rt.Ex_available_gen14["state"] = tk.NORMAL
            Rt.Ex_available_gen15["state"] = tk.NORMAL
            Rt.Ex_var7.set(1)
            Rt.Ex_var8.set(1)
            Rt.Ex_var9.set(1)
            Rt.Ex_var10.set(1)
            Rt.Ex_var11.set(1)
            Rt.Ex_var12.set(1)
            Rt.Ex_var13.set(1)
            Rt.Ex_var14.set(1)
            Rt.Ex_var15.set(1)
        else:
            Rt.Ex_available_gen7["state"] = tk.DISABLED
            Rt.Ex_available_gen8["state"] = tk.DISABLED
            Rt.Ex_available_gen9["state"] = tk.DISABLED
            Rt.Ex_available_gen10["state"] = tk.DISABLED
            Rt.Ex_available_gen11["state"] = tk.DISABLED
            Rt.Ex_available_gen12["state"] = tk.DISABLED
            Rt.Ex_available_gen13["state"] = tk.DISABLED
            Rt.Ex_available_gen14["state"] = tk.DISABLED
            Rt.Ex_available_gen15["state"] = tk.DISABLED
            Rt.Ex_var7.set(0)
            Rt.Ex_var8.set(0)
            Rt.Ex_var9.set(0)
            Rt.Ex_var10.set(0)
            Rt.Ex_var11.set(0)
            Rt.Ex_var12.set(0)
            Rt.Ex_var13.set(0)
            Rt.Ex_var14.set(0)
            Rt.Ex_var15.set(0)

class OLL_Ex:
    def __init__(self):
        self.cp = [-1, -1, -1, -1, 0, 1, 2, 3]
        self.co = []
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.eo = []

    def allow_to_check(self):
        if Rt.Ex2_var0.get():
            Rt.Ex2_available_gen7["state"] = tk.NORMAL
            Rt.Ex2_available_gen8["state"] = tk.NORMAL
            Rt.Ex2_available_gen9["state"] = tk.NORMAL
            Rt.Ex2_available_gen10["state"] = tk.NORMAL
            Rt.Ex2_available_gen11["state"] = tk.NORMAL
            Rt.Ex2_available_gen12["state"] = tk.NORMAL
            Rt.Ex2_available_gen13["state"] = tk.NORMAL
            Rt.Ex2_available_gen14["state"] = tk.NORMAL
            Rt.Ex2_available_gen15["state"] = tk.NORMAL
            Rt.Ex2_var7.set(1)
            Rt.Ex2_var8.set(1)
            Rt.Ex2_var9.set(1)
            Rt.Ex2_var10.set(1)
            Rt.Ex2_var11.set(1)
            Rt.Ex2_var12.set(1)
            Rt.Ex2_var13.set(1)
            Rt.Ex2_var14.set(1)
            Rt.Ex2_var15.set(1)
        else:
            Rt.Ex2_available_gen7["state"] = tk.DISABLED
            Rt.Ex2_available_gen8["state"] = tk.DISABLED
            Rt.Ex2_available_gen9["state"] = tk.DISABLED
            Rt.Ex2_available_gen10["state"] = tk.DISABLED
            Rt.Ex2_available_gen11["state"] = tk.DISABLED
            Rt.Ex2_available_gen12["state"] = tk.DISABLED
            Rt.Ex2_available_gen13["state"] = tk.DISABLED
            Rt.Ex2_available_gen14["state"] = tk.DISABLED
            Rt.Ex2_available_gen15["state"] = tk.DISABLED
            Rt.Ex2_var7.set(0)
            Rt.Ex2_var8.set(0)
            Rt.Ex2_var9.set(0)
            Rt.Ex2_var10.set(0)
            Rt.Ex2_var11.set(0)
            Rt.Ex2_var12.set(0)
            Rt.Ex2_var13.set(0)
            Rt.Ex2_var14.set(0)
            Rt.Ex2_var15.set(0)

    def OLL_change_color(self, event, arg):
        if event.widget.itemcget(arg, "fill") == "Gray":
            event.widget.itemconfig(arg, fill="Yellow")
        else:
            event.widget.itemconfig(arg, fill="Gray")

    def Paint_reset(self):
        for i in range(21):
            if i == 16:
                pass
            else:
                Rt.OLL_paint_canvas.itemconfig("M" + str(i), fill="Gray")

    def OLLarg_dicision(self):
        Rt.Button_explor_OLL_exit["state"] = tk.NORMAL
        Rt.Button_explor_OLL_start["state"] = tk.DISABLED
        if Rt.Ex2_var16.get():
            Rt.explor_OLL_Box.delete("1.0", "end")

        m = Rt.Ex2_startfrom1_OLL_comb.current()
        n = Rt.Ex2_startfrom2_OLL_comb.current()

        Solution1 = Rt.Ex2_txt_min_length.get()
        Solution2 = Rt.Ex2_txt_max_length.get()
        Solution3 = Rt.Ex2_txt_timeout.get()

        if Solution1 == "":
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif Solution1.isdigit() == False:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with first searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution1) < 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        
        if Solution2 == "":
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif Solution2.isdigit() == False:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with max searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution2) < 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        
        if Solution3 == "":
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif Solution3.isdigit() == False:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with searching time. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        elif int(Solution3) < 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return

        self.co = []
        self.eo = []

        count = 0
        for i in ["M12", "M0", "M6"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M12", "M0", "M6"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.co.append(orient)

        count = 0
        for i in ["M14", "M8", "M3"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M14", "M8", "M3"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.co.append(orient)

        count = 0
        for i in ["M20", "M5", "M11"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M20", "M5", "M11"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.co.append(orient)

        count = 0
        for i in ["M18", "M9", "M2"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M18", "M9", "M2"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.co.append(orient)
        
        if sum(self.co) % 3 == 0:
            self.co += [0, 0, 0, 0]
        else:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return

        count = 0
        for i in ["M13", "M7"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M13", "M7"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.eo.append(orient)

        count = 0
        for i in ["M17", "M4"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M17", "M4"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.eo.append(orient)

        count = 0
        for i in ["M19", "M10"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M19", "M10"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.eo.append(orient)

        count = 0
        for i in ["M15", "M1"]:
            if Rt.OLL_paint_canvas.itemcget(i, "fill") == "Yellow":
                count += 1
                orient = ["M15", "M1"].index(i)
        if count != 1:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return
        else:
            self.eo.append(orient)

        if sum(self.eo) % 2 == 0:
            self.eo = [0, 0, 0, 0] + self.eo + [0, 0, 0, 0]
        else:
            Rt.explor_OLL_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_OLL_start["state"] = tk.NORMAL
            Rt.Button_explor_OLL_exit["state"] = tk.DISABLED
            return

        if m == 1:
            self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[7], self.eo[4], self.eo[5], self.eo[6]            
            self.co[0], self.co[1], self.co[2], self.co[3] = self.co[3], self.co[0], self.co[1], self.co[2]
            # self.eo[6], self.eo[7] = self.eo[7], self.eo[6]
            # self.eo[5], self.eo[6] = self.eo[6], self.eo[5]
            # self.eo[5], self.eo[4] = self.eo[4], self.eo[5]

            # self.co[2], self.co[3] = self.co[3], self.co[2]
            # self.co[1], self.co[2] = self.co[2], self.co[1]
            # self.co[0], self.co[1] = self.co[1], self.co[0]

        elif m == 2:
            self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[6], self.eo[7], self.eo[4], self.eo[5]            
            self.co[0], self.co[1], self.co[2], self.co[3] = self.co[2], self.co[3], self.co[0], self.co[1]
            # self.eo[4], self.eo[6] = self.eo[6], self.eo[4]
            # self.eo[5], self.eo[7] = self.eo[7], self.eo[5]

            # self.co[0], self.co[2] = self.co[2], self.co[0]
            # self.co[1], self.co[3] = self.co[3], self.co[1]

        elif m == 3:
            self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[5], self.eo[6], self.eo[7], self.eo[4]
            self.co[0], self.co[1], self.co[2], self.co[3] = self.co[1], self.co[2], self.co[3], self.co[0]
            # self.eo[4], self.eo[5] = self.eo[5], self.eo[4]
            # self.eo[5], self.eo[6] = self.eo[6], self.eo[5]
            # self.eo[6], self.eo[7] = self.eo[7], self.eo[6]

            # self.co[0], self.co[1] = self.co[1], self.co[0]
            # self.co[1], self.co[2] = self.co[2], self.co[1]
            # self.co[2], self.co[3] = self.co[3], self.co[2]

        # print(self.eo)
        # print(self.co)

        Ex_available_list = [str(int(Rt.Ex2_var1.get())),
                        str(int(Rt.Ex2_var2.get())),
                        str(int(Rt.Ex2_var3.get())),
                        str(int(Rt.Ex2_var4.get())),
                        str(int(Rt.Ex2_var5.get())),
                        str(int(Rt.Ex2_var6.get())),
                        str(int(Rt.Ex2_var7.get())),
                        str(int(Rt.Ex2_var8.get())),
                        str(int(Rt.Ex2_var9.get())),
                        str(int(Rt.Ex2_var10.get())),
                        str(int(Rt.Ex2_var11.get())),
                        str(int(Rt.Ex2_var12.get())),
                        str(int(Rt.Ex2_var13.get())),
                        str(int(Rt.Ex2_var14.get())),
                        str(int(Rt.Ex2_var15.get()))
                        ]

        arg_CP = " ".join(map(str, self.cp))
        arg_CO = " ".join(map(str, self.co))
        arg_EP = " ".join(map(str, self.ep))
        arg_EO = " ".join(map(str, self.eo))

        forbid_list = [0, 15, 12]
        forbidden = str(forbid_list[n])

        cmd = "CubeSE.exe " + arg_CP +  " " + arg_CO + " " + arg_EP + " " + arg_EO + " 0 1 2 3 4 5 " + " ".join(Ex_available_list) + " " + Solution1 + " " + Solution2 + " " + Solution3 + " " + str(int(Rt.Ex2_var0.get()) * 2 + Rt.htm_var2.get()) + " " + forbidden + " " + str(Rt.auf_var2.get()) + " 1"

        # print(cmd)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        Rt.explor_OLL_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
        #a = time.perf_counter()

        #ID = root.after(int((Solution3 + 1.457) * 1000), Rt.Explorer_Exit_thread)

        self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
        for line in iter(ollex.search.stdout.readline, b''):
            #print(time.perf_counter() - a)
            Rt.explor_OLL_Box.insert("end", line.rstrip().decode('sjis') + "\n")
            Rt.explor_OLL_Box.see("end")

        """self.solution = search.start_search(min_length = int(Solution1), \
            max_length = int(Solution2))"""
        #print(time.perf_counter() - a)
        Rt.explor_OLL_Box.insert("end", f"Finished!\n")
        Rt.Button_explor_OLL_start["state"] = tk.NORMAL
        Rt.Button_explor_OLL_exit["state"] = tk.DISABLED

class F2L_Ex:
    def __init__(self):
        self.cp = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.co = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.ep = [-1, -1, -1, -1, -1, -1, -1, -1, 8, 9, 10, 11]
        self.eo = [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0]
    
    def allow_to_check(self):
        if Rt.Ex3_var0.get():
            Rt.Ex3_available_gen7["state"] = tk.NORMAL
            Rt.Ex3_available_gen8["state"] = tk.NORMAL
            Rt.Ex3_available_gen9["state"] = tk.NORMAL
            Rt.Ex3_available_gen10["state"] = tk.NORMAL
            Rt.Ex3_available_gen11["state"] = tk.NORMAL
            Rt.Ex3_available_gen12["state"] = tk.NORMAL
            Rt.Ex3_available_gen13["state"] = tk.NORMAL
            Rt.Ex3_available_gen14["state"] = tk.NORMAL
            Rt.Ex3_available_gen15["state"] = tk.NORMAL
            Rt.Ex3_var7.set(1)
            Rt.Ex3_var8.set(1)
            Rt.Ex3_var9.set(1)
            Rt.Ex3_var10.set(1)
            Rt.Ex3_var11.set(1)
            Rt.Ex3_var12.set(1)
            Rt.Ex3_var13.set(1)
            Rt.Ex3_var14.set(1)
            Rt.Ex3_var15.set(1)
        else:
            Rt.Ex3_available_gen7["state"] = tk.DISABLED
            Rt.Ex3_available_gen8["state"] = tk.DISABLED
            Rt.Ex3_available_gen9["state"] = tk.DISABLED
            Rt.Ex3_available_gen10["state"] = tk.DISABLED
            Rt.Ex3_available_gen11["state"] = tk.DISABLED
            Rt.Ex3_available_gen12["state"] = tk.DISABLED
            Rt.Ex3_available_gen13["state"] = tk.DISABLED
            Rt.Ex3_available_gen14["state"] = tk.DISABLED
            Rt.Ex3_available_gen15["state"] = tk.DISABLED
            Rt.Ex3_var7.set(0)
            Rt.Ex3_var8.set(0)
            Rt.Ex3_var9.set(0)
            Rt.Ex3_var10.set(0)
            Rt.Ex3_var11.set(0)
            Rt.Ex3_var12.set(0)
            Rt.Ex3_var13.set(0)
            Rt.Ex3_var14.set(0)
            Rt.Ex3_var15.set(0)

    def Paint(self):
        #U
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), fill="Gray", tags="O0", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), fill="Gray", tags="O1", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.11111), fill="Gray", tags="O2", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), fill="Gray", tags="O3", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), fill="Yellow")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.22222), fill="Gray", tags="O5", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.32777), fill="Gray", tags="O6", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.32777), fill="Gray", tags="O7", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.32777), fill="Gray", tags="O8", state=tk.NORMAL)
        
        #F
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), fill="Gray", tags="O9", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), fill="Gray", tags="O10", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.44444), fill="Gray", tags="O11", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), fill="Gray", tags="O12", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), fill="Blue")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.55555), fill="Gray", tags="O14", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.66111), fill="Gray", tags="O15", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.66111), fill="Blue")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.66111), fill="Gray", tags="O17", state=tk.NORMAL)
        
        #D
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), fill="Gray", tags="O18", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), fill="White")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.77777), fill="Gray", tags="O20", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), fill="White")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), fill="White")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.88888), fill="White")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.99444), fill="Gray", tags="O24", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.99444), fill="White")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.99444), fill="Gray", tags="O26", state=tk.NORMAL)
        
        #L
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), fill="Gray", tags="O27", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), fill="Gray", tags="O28", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.44444), fill="Gray", tags="O29", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), fill="Gray", tags="O30", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), fill="Dark Orange")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.55555), fill="Gray", tags="O32", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.66111), fill="Gray", tags="O33", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.66111), fill="Dark Orange")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.66111), fill="Gray", tags="O35", state=tk.NORMAL)
        
        #R
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), fill="Gray", tags="O36", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), fill="Gray", tags="O37", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.44444), fill="Gray", tags="O38", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), fill="Gray", tags="O39", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), fill="Red")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.55555), fill="Gray", tags="O41", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.66111), fill="Gray", tags="O42", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.66111), fill="Red")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.66111), fill="Gray", tags="O44", state=tk.NORMAL)

        #B
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), fill="Gray", tags="O45", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), fill="Gray", tags="O46", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.44444), fill="Gray", tags="O47", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), fill="Gray", tags="O48", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), fill="Green")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.55555), fill="Gray", tags="O50", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.66111), fill="Gray", tags="O51", state=tk.NORMAL)
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.66111), fill="Green")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.66111), fill="Gray", tags="O53", state=tk.NORMAL)

        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.041666), round(CVHEIGHT * 0.74074), round(CVWIDTH * 0.20833), round(CVHEIGHT * 0.962963), fill=Rt.Ex3_selected_color, tags="Ex3_show")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.627775), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.70555), round(CVHEIGHT * 0.88518), fill=Rt.Ex3_slot_color_set[0], tags="Select0")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.711105), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.788885), round(CVHEIGHT * 0.88518), fill=Rt.Ex3_slot_color_set[1], tags="Select1")
        Rt.F2L_paint_canvas.create_rectangle(round(CVWIDTH * 0.79444), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.872215), round(CVHEIGHT * 0.88518), fill=Rt.Ex3_slot_color_set[2], tags="Select2")

    def Paint_reset(self):
        for i in range(54):
            if i in (4, 13, 16, 19, 21, 22, 23, 25, 31, 34, 40, 43, 49, 52):
                pass
            else:
                Rt.F2L_paint_canvas.itemconfig("O" + str(i), fill="Gray")
        
        for i in range(3):
            Rt.F2L_paint_canvas.itemconfig("Select" + str(i), fill=Rt.Ex3_slot_color_set[i])

        Rt.F2L_paint_canvas.itemconfig("Ex3_show", fill="White")
        Rt.Ex3_selected_color = "White"

        if Rt.solved_slot_var0.get():
            Rt.solved_slot_var0.set(0)
            f2lex.paint_slots(0)
        
        if Rt.solved_slot_var1.get():
            Rt.solved_slot_var1.set(0)
            f2lex.paint_slots(1)
        
        if Rt.solved_slot_var2.get():
            Rt.solved_slot_var2.set(0)
            f2lex.paint_slots(2)

        if Rt.solved_slot_var3.get():
            Rt.solved_slot_var3.set(0)
            f2lex.paint_slots(3)

    def Ex3_change_color(self, event, arg):
        if event.widget.itemcget(arg, "fill") == "Gray":
            event.widget.itemconfig(arg, fill=Rt.Ex3_selected_color)
        elif event.widget.itemcget(arg, "fill") == Rt.Ex3_selected_color:
            event.widget.itemconfig(arg, fill="Gray")
        else:
            event.widget.itemconfig(arg, fill=Rt.Ex3_selected_color)

    def Ex3_select_color0(self, event):
        Rt.Ex3_selected_color = Rt.Ex3_slot_color_set[0]
        event.widget.itemconfig("Ex3_show", fill=Rt.Ex3_selected_color)

    def Ex3_select_color1(self, event):
        Rt.Ex3_selected_color = Rt.Ex3_slot_color_set[1]
        event.widget.itemconfig("Ex3_show", fill=Rt.Ex3_selected_color)

    def Ex3_select_color2(self, event):
        Rt.Ex3_selected_color = Rt.Ex3_slot_color_set[2]
        event.widget.itemconfig("Ex3_show", fill=Rt.Ex3_selected_color)

    def select_slot(self, event):
        slot = Rt.F2L_list.index(Rt.F2L_var.get())
        if slot == 0:
            if Rt.solved_slot_var0.get() == 1:
                Rt.solved_slot_var0.set(0)
                f2lex.paint_slots(0)
            Rt.solved_slot0["state"] = tk.DISABLED
            Rt.solved_slot1["state"] = tk.NORMAL
            Rt.solved_slot2["state"] = tk.NORMAL
            Rt.solved_slot3["state"] = tk.NORMAL
            Rt.Ex3_slot_color_set = ["White", "Blue", "Red"]

        if slot == 1:
            if Rt.solved_slot_var1.get() == 1:
                Rt.solved_slot_var1.set(0)
                f2lex.paint_slots(1)
            Rt.solved_slot0["state"] = tk.NORMAL
            Rt.solved_slot1["state"] = tk.DISABLED
            Rt.solved_slot2["state"] = tk.NORMAL
            Rt.solved_slot3["state"] = tk.NORMAL
            Rt.Ex3_slot_color_set = ["White", "Blue", "Dark Orange"]

        if slot == 2:
            if Rt.solved_slot_var2.get() == 1:
                Rt.solved_slot_var2.set(0)
                f2lex.paint_slots(2)
            Rt.solved_slot0["state"] = tk.NORMAL
            Rt.solved_slot1["state"] = tk.NORMAL
            Rt.solved_slot2["state"] = tk.DISABLED
            Rt.solved_slot3["state"] = tk.NORMAL
            Rt.Ex3_slot_color_set = ["White", "Green", "Red"]

        if slot == 3:
            if Rt.solved_slot_var3.get() == 1:
                Rt.solved_slot_var3.set(0)
                f2lex.paint_slots(3)
            Rt.solved_slot0["state"] = tk.NORMAL
            Rt.solved_slot1["state"] = tk.NORMAL
            Rt.solved_slot2["state"] = tk.NORMAL
            Rt.solved_slot3["state"] = tk.DISABLED
            Rt.Ex3_slot_color_set = ["White", "Green", "Dark Orange"]

        f2lex.Paint_reset()

    def paint_slots(self, index):
        if index == 0:
            if str(Rt.F2L_paint_canvas.itemcget("O14", "state")) == tk.NORMAL:
                Rt.F2L_paint_canvas.itemconfig("O14", fill="Blue", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O17", fill="Blue", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O20", fill="White", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O39", fill="Red", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O42", fill="Red", state=tk.DISABLED)
            else:
                Rt.F2L_paint_canvas.itemconfig("O14", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O17", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O20", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O39", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O42", fill="Gray", state=tk.NORMAL)

        elif index == 1:
            if str(Rt.F2L_paint_canvas.itemcget("O12", "state")) == tk.NORMAL:
                Rt.F2L_paint_canvas.itemconfig("O12", fill="Blue", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O15", fill="Blue", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O18", fill="White", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O32", fill="Dark Orange", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O35", fill="Dark Orange", state=tk.DISABLED)
            else:
                Rt.F2L_paint_canvas.itemconfig("O12", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O15", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O18", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O32", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O35", fill="Gray", state=tk.NORMAL)

        elif index == 2:
            if str(Rt.F2L_paint_canvas.itemcget("O41", "state")) == tk.NORMAL:
                Rt.F2L_paint_canvas.itemconfig("O41", fill="Red", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O44", fill="Red", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O26", fill="White", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O48", fill="Green", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O51", fill="Green", state=tk.DISABLED)
            else:
                Rt.F2L_paint_canvas.itemconfig("O41", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O44", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O26", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O48", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O51", fill="Gray", state=tk.NORMAL)

        elif index == 3:
            if str(Rt.F2L_paint_canvas.itemcget("O30", "state")) == tk.NORMAL:
                Rt.F2L_paint_canvas.itemconfig("O30", fill="Dark Orange", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O33", fill="Dark Orange", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O24", fill="White", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O50", fill="Green", state=tk.DISABLED)
                Rt.F2L_paint_canvas.itemconfig("O53", fill="Green", state=tk.DISABLED)
            else:
                Rt.F2L_paint_canvas.itemconfig("O30", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O33", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O24", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O50", fill="Gray", state=tk.NORMAL)
                Rt.F2L_paint_canvas.itemconfig("O53", fill="Gray", state=tk.NORMAL)

    def F2Larg_dicision(self):
        Rt.Button_explor_F2L_exit["state"] = tk.NORMAL
        Rt.Button_explor_F2L_start["state"] = tk.DISABLED
        if Rt.Ex3_var16.get():
            Rt.explor_F2L_Box.delete("1.0", "end")

        m = Rt.Ex3_startfrom1_F2L_comb.current()

        Solution1 = Rt.Ex3_txt_min_length.get()
        Solution2 = Rt.Ex3_txt_max_length.get()
        Solution3 = Rt.Ex3_txt_timeout.get()

        if Solution1 == "":
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif Solution1.isdigit() == False:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with first searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif int(Solution1) < 1:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        
        if Solution2 == "":
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif Solution2.isdigit() == False:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with max searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif int(Solution2) < 1:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        
        if Solution3 == "":
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif Solution3.isdigit() == False:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with searching time. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return
        elif int(Solution3) < 1:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return

        corner_list = [["O0", "O27", "O47"], ["O2", "O45", "O38"], ["O8", "O36", "O11"], ["O6", "O9", "O29"], ["O24", "O53", "O33"], ["O26", "O44", "O51"], ["O20", "O17", "O42"], ["O18", "O35", "O15"]]
        edge_list = [["O50", "O30"], ["O48", "O41"], ["O14", "O39"], ["O12", "O32"], ["O1", "O46"], ["O5", "O37"], ["O7", "O10"], ["O3", "O28"]]
        solved_slot_list = [Rt.solved_slot_var0, Rt.solved_slot_var1, Rt.solved_slot_var2, Rt.solved_slot_var3]
        num = 0
        x = Rt.F2L_list.index(Rt.F2L_var.get())

        self.cp = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.co = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.ep = [-1, -1, -1, -1, -1, -1, -1, -1, 8, 9, 10, 11]
        self.eo = [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0]

        for index, value in enumerate(corner_list):
            get_colors = [Rt.F2L_paint_canvas.itemcget(value[0], "fill"), Rt.F2L_paint_canvas.itemcget(value[1], "fill"), Rt.F2L_paint_canvas.itemcget(value[2], "fill")]
            if str(Rt.F2L_paint_canvas.itemcget(value[0], "state")) == tk.NORMAL and (not ("Gray" in get_colors)) and len(set(get_colors)) == 3:
                num += 1
                # returns 0 -> 6, 1 -> 7, 2 -> 5, 3 -> 4
                self.cp[index] = round((4 * x ** 3 - 21 * x ** 2 + 23 * x + 36) / 6)
                for i in range(3):
                    if get_colors[i] == "White":
                        self.co[index] = i

        if num != 1:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \n2 or more corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return

        num = 0

        for index, value in enumerate(edge_list):
            get_colors = [Rt.F2L_paint_canvas.itemcget(value[0], "fill"), Rt.F2L_paint_canvas.itemcget(value[1], "fill")]
            if str(Rt.F2L_paint_canvas.itemcget(value[0], "state")) == tk.NORMAL and (not ("Gray" in get_colors)) and len(set(get_colors)) == 2:
                num += 1
                # returns 0 -> 2, 1 -> 3, 2 -> 1, 3 -> 0
                self.ep[index] = round((4 * x ** 3 - 21 * x ** 2 + 23 * x + 12) / 6)
                if get_colors[0] in ("Blue", "Green"):
                    self.eo[index] = 0
                else:
                    self.eo[index] = 1
        
        if num != 1:
            Rt.explor_F2L_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \n2 or more edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_F2L_start["state"] = tk.NORMAL
            Rt.Button_explor_F2L_exit["state"] = tk.DISABLED
            return

        pattern = set()

        for index, value in enumerate(solved_slot_list):
            if value.get() == 1:
                pattern.add(round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 12) / 6))
                self.cp[round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 36) / 6)] = round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 36) / 6)
                self.co[round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 36) / 6)] = 0
                self.ep[round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 12) / 6)] = round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 12) / 6)
                self.eo[round((4 * index ** 3 - 21 * index ** 2 + 23 * index + 12) / 6)] = 0

        pattern.add(round((4 * Rt.F2L_list.index(Rt.Ex3_commbobox_F2L.get()) ** 3 - 21 * Rt.F2L_list.index(Rt.Ex3_commbobox_F2L.get()) ** 2 + 23 * Rt.F2L_list.index(Rt.Ex3_commbobox_F2L.get()) + 12) / 6))

        pattern_sets = [
            {0}, {1}, {2}, {3},
            {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3},
            {0, 1, 2}, {0, 1, 3}, {0, 2, 3}, {1, 2, 3},
            {0, 1, 2, 3}
        ]

        if m == 1:
            self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
            self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
            self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
            self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]
            pattern = {i + 1 if i < 3 else i - 3 for i in pattern}

        elif m == 2:
            self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
            self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
            self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
            self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]
            pattern = {i + 2 if i < 2 else i - 2 for i in pattern}

        elif m == 3:
            self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
            self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
            self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
            self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]
            pattern = {i + 3 if i < 1 else i - 1 for i in pattern}

        for i in range(15):
            if pattern == pattern_sets[i]:
                pattern = str(i)

        for i in range(8):
            if self.cp[i] < 4 and self.cp[i] != -1:
                if self.cp[i] + m >= 4:
                    self.cp[i] = self.cp[i] + m - 4
                else:
                    self.cp[i] += m
            elif self.cp[i] >= 4:
                if self.cp[i] + m >= 8:
                    self.cp[i] = self.cp[i] + m - 4
                else:
                    self.cp[i] += m

            if self.ep[i] < 4 and self.ep[i] != -1:
                if self.ep[i] + m >= 4:
                    self.ep[i] = self.ep[i] + m - 4
                else:
                    self.ep[i] += m
            elif self.ep[i] >= 4:
                if self.ep[i] + m >= 8:
                    self.ep[i] = self.ep[i] + m - 4
                else:
                    self.ep[i] += m

        for i in range(4, 8):
            if self.eo[i] != -1:
                self.eo[i] = (self.eo[i] + m) % 2

        # alt_cp = [i for i in range(7 - self.cp.count(-1), -1, -1)]
        # print(alt_cp)
        # print(heapq.nlargest(len(alt_cp), self.cp))
        # for i in heapq.nlargest(len(alt_cp), self.cp):
        #     self.cp[self.cp.index(i)] = alt_cp[0]
        #     alt_cp.pop(0)

        if self.eo.count(1) % 2 == 0:
            self.eo = [i if i != -1 else 0 for i in self.eo]
        else:
            for i in range(8):
                if self.eo[i] == -1:
                    self.eo[i] = 1
                    break
            self.eo = [i if i != -1 else 0 for i in self.eo]

        ep_diff = [i for i in range(12) if not(i in self.ep)]
        for i in range(12):
            if self.ep[i] == -1:
                self.ep[i] = ep_diff[0]
                ep_diff.pop(0)

        # print(self.cp)
        # print(self.co)
        # print(self.ep)
        # print(self.eo)

        Ex_available_list = [str(int(Rt.Ex3_var1.get())),
                        str(int(Rt.Ex3_var2.get())),
                        str(int(Rt.Ex3_var3.get())),
                        str(int(Rt.Ex3_var4.get())),
                        str(int(Rt.Ex3_var5.get())),
                        str(int(Rt.Ex3_var6.get())),
                        str(int(Rt.Ex3_var7.get())),
                        str(int(Rt.Ex3_var8.get())),
                        str(int(Rt.Ex3_var9.get())),
                        str(int(Rt.Ex3_var10.get())),
                        str(int(Rt.Ex3_var11.get())),
                        str(int(Rt.Ex3_var12.get())),
                        str(int(Rt.Ex3_var13.get())),
                        str(int(Rt.Ex3_var14.get())),
                        str(int(Rt.Ex3_var15.get()))
                        ]

        arg_CP = " ".join(map(str, self.cp))
        arg_CO = " ".join(map(str, self.co))
        arg_EP = " ".join(map(str, self.ep))
        arg_EO = " ".join(map(str, self.eo))

        cmd = "CubeSE.exe " + arg_CP +  " " + arg_CO + " " + arg_EP + " " + arg_EO + " 0 1 2 3 4 5 " + " ".join(Ex_available_list) + " " + Solution1 + " " + Solution2 + " " + Solution3 + " " + str(int(Rt.Ex3_var0.get()) * 2 + Rt.htm_var3.get()) + " " + pattern

        # print(cmd)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        Rt.explor_F2L_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")

        self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
        for line in iter(f2lex.search.stdout.readline, b''):
            #print(time.perf_counter() - a)
            Rt.explor_F2L_Box.insert("end", line.rstrip().decode('sjis') + "\n")
            Rt.explor_F2L_Box.see("end")

        """self.solution = search.start_search(min_length = int(Solution1), \
            max_length = int(Solution2))"""
        #print(time.perf_counter() - a)
        Rt.explor_F2L_Box.insert("end", f"Finished!\n")
        Rt.Button_explor_F2L_start["state"] = tk.NORMAL
        Rt.Button_explor_F2L_exit["state"] = tk.DISABLED

class sub_step_Ex:
    def _init_(self):
        self.cp = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.co = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.ep = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.eo = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    def allow_to_check(self):
        if Rt.Ex4_var0.get():
            Rt.Ex4_available_gen7["state"] = tk.NORMAL
            Rt.Ex4_available_gen8["state"] = tk.NORMAL
            Rt.Ex4_available_gen9["state"] = tk.NORMAL
            Rt.Ex4_available_gen10["state"] = tk.NORMAL
            Rt.Ex4_available_gen11["state"] = tk.NORMAL
            Rt.Ex4_available_gen12["state"] = tk.NORMAL
            Rt.Ex4_available_gen13["state"] = tk.NORMAL
            Rt.Ex4_available_gen14["state"] = tk.NORMAL
            Rt.Ex4_available_gen15["state"] = tk.NORMAL
            Rt.Ex4_var7.set(1)
            Rt.Ex4_var8.set(1)
            Rt.Ex4_var9.set(1)
            Rt.Ex4_var10.set(1)
            Rt.Ex4_var11.set(1)
            Rt.Ex4_var12.set(1)
            Rt.Ex4_var13.set(1)
            Rt.Ex4_var14.set(1)
            Rt.Ex4_var15.set(1)
        else:
            Rt.Ex4_available_gen7["state"] = tk.DISABLED
            Rt.Ex4_available_gen8["state"] = tk.DISABLED
            Rt.Ex4_available_gen9["state"] = tk.DISABLED
            Rt.Ex4_available_gen10["state"] = tk.DISABLED
            Rt.Ex4_available_gen11["state"] = tk.DISABLED
            Rt.Ex4_available_gen12["state"] = tk.DISABLED
            Rt.Ex4_available_gen13["state"] = tk.DISABLED
            Rt.Ex4_available_gen14["state"] = tk.DISABLED
            Rt.Ex4_available_gen15["state"] = tk.DISABLED
            Rt.Ex4_var7.set(0)
            Rt.Ex4_var8.set(0)
            Rt.Ex4_var9.set(0)
            Rt.Ex4_var10.set(0)
            Rt.Ex4_var11.set(0)
            Rt.Ex4_var12.set(0)
            Rt.Ex4_var13.set(0)
            Rt.Ex4_var14.set(0)
            Rt.Ex4_var15.set(0)

    def select_sub_step(self, event):
        name = Rt.sub_step_var.get()

        if name in ("OLL + PLL", "OLL + CPLL"):
            Rt.sub_step_paint_canvas.itemconfig("Select_white", state=tk.HIDDEN)
            Rt.sub_step_paint_canvas.itemconfig("Select_yellow", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_red", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_orange", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_blue", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_green", state=tk.NORMAL)
            Rt.Ex4_startfrom2_sub_step_comb["state"] = "readonly"
            Rt.usebracket_button4["state"] = tk.NORMAL
            Rt.unusebracket_button4["state"] = tk.NORMAL

            for i in range(54):
                if i in (4, 12, 13, 15, 16, 18, 19, 21, 22, 23, 25, 31, 32, 34, 35, 40, 43, 49, 52):
                    pass
                elif i in (14, 17):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Blue", state=tk.DISABLED)
                elif i in (20, 24, 26):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="White", state=tk.DISABLED)
                elif i in (30, 33):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Dark Orange", state=tk.DISABLED)
                elif i in (39, 41, 42, 44):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Red", state=tk.DISABLED)
                elif i in (48, 50, 51, 53):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Green", state=tk.DISABLED)
                else:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Gray", state=tk.NORMAL)

            Rt.sub_step_paint_canvas.itemconfig("Ex4_show", fill="Yellow")
            Rt.Ex4_selected_color = "Yellow"
        
        elif name in ("LS + EOLL", "LS + OLL"):
            Rt.sub_step_paint_canvas.itemconfig("Select_white", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_yellow", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_red", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_orange", state=tk.HIDDEN)
            Rt.sub_step_paint_canvas.itemconfig("Select_blue", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_green", state=tk.HIDDEN)
            Rt.Ex4_startfrom2_sub_step_comb.current(0)
            Rt.Ex4_startfrom2_sub_step_comb["state"] = tk.DISABLED
            Rt.auf_var4.set(1)
            Rt.usebracket_button4["state"] = tk.DISABLED
            Rt.unusebracket_button4["state"] = tk.DISABLED

            for i in range(54):
                if i in (4, 12, 13, 15, 16, 18, 19, 21, 22, 23, 25, 31, 32, 34, 35, 40, 43, 49, 52):
                    pass
                elif i in (24, 26):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="White", state=tk.DISABLED)
                elif i in (30, 33):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Dark Orange", state=tk.DISABLED)
                elif i in (41, 44):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Red", state=tk.DISABLED)
                elif i in (48, 50, 51, 53):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Green", state=tk.DISABLED)
                else:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Gray", state=tk.NORMAL)

            Rt.sub_step_paint_canvas.itemconfig("Ex4_show", fill="Yellow")
            Rt.Ex4_selected_color = "Yellow"

        elif name == "Advanced F2L (Adj)":
            Rt.sub_step_paint_canvas.itemconfig("Select_white", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_yellow", state=tk.HIDDEN)
            Rt.sub_step_paint_canvas.itemconfig("Select_red", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_orange", state=tk.HIDDEN)
            Rt.sub_step_paint_canvas.itemconfig("Select_blue", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_green", state=tk.NORMAL)
            Rt.Ex4_startfrom2_sub_step_comb.current(0)
            Rt.Ex4_startfrom2_sub_step_comb["state"] = tk.DISABLED
            Rt.auf_var4.set(1)
            Rt.usebracket_button4["state"] = tk.DISABLED
            Rt.unusebracket_button4["state"] = tk.DISABLED

            for i in range(54):
                if i in (4, 12, 13, 15, 16, 18, 19, 21, 22, 23, 25, 31, 32, 34, 35, 40, 43, 49, 52):
                    pass
                elif i == 24:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="White", state=tk.DISABLED)
                elif i in (30, 33):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Dark Orange", state=tk.DISABLED)
                elif i in (50, 53):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Green", state=tk.DISABLED)
                else:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Gray", state=tk.NORMAL)

            Rt.sub_step_paint_canvas.itemconfig("Ex4_show", fill="White")
            Rt.Ex4_selected_color = "White"

        elif name == "Advanced F2L (Opp)":
            Rt.sub_step_paint_canvas.itemconfig("Select_white", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_yellow", state=tk.HIDDEN)
            Rt.sub_step_paint_canvas.itemconfig("Select_red", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_orange", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_blue", state=tk.NORMAL)
            Rt.sub_step_paint_canvas.itemconfig("Select_green", state=tk.NORMAL)
            Rt.Ex4_startfrom2_sub_step_comb.current(0)
            Rt.Ex4_startfrom2_sub_step_comb["state"] = tk.DISABLED
            Rt.auf_var4.set(1)
            Rt.usebracket_button4["state"] = tk.DISABLED
            Rt.unusebracket_button4["state"] = tk.DISABLED

            for i in range(54):
                if i in (4, 12, 13, 15, 16, 18, 19, 21, 22, 23, 25, 31, 32, 34, 35, 40, 43, 49, 52):
                    pass
                elif i == 26:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="White", state=tk.DISABLED)
                elif i in (41, 44):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Red", state=tk.DISABLED)
                elif i in (48, 51):
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Green", state=tk.DISABLED)
                else:
                    Rt.sub_step_paint_canvas.itemconfig("P" + str(i), fill="Gray", state=tk.NORMAL)

            Rt.sub_step_paint_canvas.itemconfig("Ex4_show", fill="White")
            Rt.Ex4_selected_color = "White"

    def Paint(self):
        #U
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), fill="Gray", tags="P0", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), fill="Gray", tags="P1", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.00555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.11111), fill="Gray", tags="P2", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), fill="Gray", tags="P3", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), fill="Yellow")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.11111), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.22222), fill="Gray", tags="P5", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.32777), fill="Gray", tags="P6", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.32777), fill="Gray", tags="P7", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.22222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.32777), fill="Gray", tags="P8", state=tk.NORMAL)
        
        #F
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), fill="Gray", tags="P9", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), fill="Gray", tags="P10", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.44444), fill="Gray", tags="P11", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), fill="Blue", tags="P12")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), fill="Blue")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.55555), fill="Blue", tags="P14", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.66111), fill="Blue", tags="P15")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.66111), fill="Blue", tags="P16")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.66111), fill="Blue", tags="P17", state=tk.DISABLED)
        
        #D
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), fill="White", tags="P18")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), fill="White", tags="P19")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.67222), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.77777), fill="White", tags="P20", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), fill="White", tags="P21")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), fill="White")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.88888), fill="White", tags="P23")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.25416), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.99444), fill="White", tags="P24", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.33333), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.99444), fill="White", tags="P25")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.41666), round(CVHEIGHT * 0.88888), round(CVWIDTH * 0.49583), round(CVHEIGHT * 0.99444), fill="White", tags="P26", state=tk.DISABLED)
        
        #L
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), fill="Gray", tags="P27", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), fill="Gray", tags="P28", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.44444), fill="Gray", tags="P29", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), fill="Dark Orange", tags="P30", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), fill="Dark Orange")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.55555), fill="Dark Orange", tags="P32")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.0041667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.66111), fill="Dark Orange", tags="P33", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.08333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.66111), fill="Dark Orange", tags="P34")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.16667), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.24583), round(CVHEIGHT * 0.66111), fill="Dark Orange", tags="P35")
        
        #R
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), fill="Gray", tags="P36", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), fill="Gray", tags="P37", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.44444), fill="Gray", tags="P38", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), fill="Red", tags="P39", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), fill="Red")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.55555), fill="Red", tags="P41", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.50416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.66111), fill="Red", tags="P42", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.58333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.66111), fill="Red", tags="P43")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.66666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.74583), round(CVHEIGHT * 0.66111), fill="Red", tags="P44", state=tk.DISABLED)

        #B
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), fill="Gray", tags="P45", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), fill="Gray", tags="P46", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.33889), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.44444), fill="Gray", tags="P47", state=tk.NORMAL)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), fill="Green", tags="P48", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), fill="Green")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.44444), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.55555), fill="Green", tags="P50", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.75416), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.66111), fill="Green", tags="P51", state=tk.DISABLED)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.83333), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.66111), fill="Green", tags="P52")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.91666), round(CVHEIGHT * 0.55555), round(CVWIDTH * 0.99583), round(CVHEIGHT * 0.66111), fill="Green", tags="P53", state=tk.DISABLED)

        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.041666), round(CVHEIGHT * 0.74074), round(CVWIDTH * 0.20833), round(CVHEIGHT * 0.962963), fill=Rt.Ex4_selected_color, tags="Ex4_show")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.50277), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.58055), round(CVHEIGHT * 0.88518), fill="White", tags="Select_white", state=tk.HIDDEN)
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.58611), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.66388), round(CVHEIGHT * 0.88518), fill="Yellow", tags="Select_yellow")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.66944), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.74722), round(CVHEIGHT * 0.88518), fill="Red", tags="Select_red")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.75277), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.83055), round(CVHEIGHT * 0.88518), fill="Dark Orange", tags="Select_orange")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.83611), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.91388), round(CVHEIGHT * 0.88518), fill="Blue", tags="Select_blue")
        Rt.sub_step_paint_canvas.create_rectangle(round(CVWIDTH * 0.91944), round(CVHEIGHT * 0.77777), round(CVWIDTH * 0.99722), round(CVHEIGHT * 0.88518), fill="Green", tags="Select_green")

    def Ex4_change_color(self, event, arg):
        if event.widget.itemcget(arg, "fill") == "Gray":
            event.widget.itemconfig(arg, fill=Rt.Ex4_selected_color)
        elif event.widget.itemcget(arg, "fill") == Rt.Ex4_selected_color:
            event.widget.itemconfig(arg, fill="Gray")
        else:
            event.widget.itemconfig(arg, fill=Rt.Ex4_selected_color)

    def Ex4_select_color_white(self, event):
        Rt.Ex4_selected_color = "White"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)
    
    def Ex4_select_color_yellow(self, event):
        Rt.Ex4_selected_color = "Yellow"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)
    
    def Ex4_select_color_red(self, event):
        Rt.Ex4_selected_color = "Red"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)
    
    def Ex4_select_color_orange(self, event):
        Rt.Ex4_selected_color = "Dark Orange"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)
    
    def Ex4_select_color_blue(self, event):
        Rt.Ex4_selected_color = "Blue"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)
    
    def Ex4_select_color_green(self, event):
        Rt.Ex4_selected_color = "Green"
        event.widget.itemconfig("Ex4_show", fill=Rt.Ex4_selected_color)

    def sub_steps_arg_dicision(self):
        Rt.Button_explor_sub_step_exit["state"] = tk.NORMAL
        Rt.Button_explor_sub_step_start["state"] = tk.DISABLED
        if Rt.Ex4_var16.get():
            Rt.explor_sub_step_Box.delete("1.0", "end")

        m = Rt.Ex4_startfrom1_sub_step_comb.current()
        n = Rt.Ex4_startfrom2_sub_step_comb.current()

        Solution1 = Rt.Ex4_txt_min_length.get()
        Solution2 = Rt.Ex4_txt_max_length.get()
        Solution3 = Rt.Ex4_txt_timeout.get()

        pattern = Rt.sub_step_list.index(Rt.sub_step_var.get())

        if Solution1 == "":
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif Solution1.isdigit() == False:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with first searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif int(Solution1) < 1:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in first searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        
        if Solution2 == "":
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif Solution2.isdigit() == False:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with max searching depth. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif int(Solution2) < 1:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in max searching depth.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        
        if Solution3 == "":
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nDesignate the searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif Solution3.isdigit() == False:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nValue Error with searching time. Please input number.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        elif int(Solution3) < 1:
            Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                \nInput at least '1' in searching time.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
            Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
            return
        
        if pattern == 0:
            self.cp = []
            self.co = []
            self.ep = []
            self.eo = []
            self.index_color_cp_list = [{"Yellow", "Green", "Dark Orange"}, {"Yellow", "Green", "Red"}, 
                                        {"Yellow", "Blue", "Red"}, {"Yellow", "Blue", "Dark Orange"},
                                        {"White", "Green", "Dark Orange"}, {"White", "Green", "Red"},
                                        {"White", "Blue", "Red"}, {"White", "Blue", "Dark Orange"}]
            self.index_color_ep_list = [{"Green", "Dark Orange"}, {"Green", "Red"},
                                        {"Blue", "Red"}, {"Blue", "Dark Orange"},
                                        {"Yellow", "Green"}, {"Yellow", "Red"},
                                        {"Yellow", "Blue"}, {"Yellow", "Dark Orange"},
                                        {"White", "Green"}, {"White", "Red"},
                                        {"White", "Blue"}, {"White", "Dark Orange"}]


            if {Rt.sub_step_paint_canvas.itemcget("P0", "fill"), Rt.sub_step_paint_canvas.itemcget("P27", "fill"), Rt.sub_step_paint_canvas.itemcget("P47", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P0", "fill"), Rt.sub_step_paint_canvas.itemcget("P27", "fill"), Rt.sub_step_paint_canvas.itemcget("P47", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P2", "fill"), Rt.sub_step_paint_canvas.itemcget("P38", "fill"), Rt.sub_step_paint_canvas.itemcget("P45", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P2", "fill"), Rt.sub_step_paint_canvas.itemcget("P38", "fill"), Rt.sub_step_paint_canvas.itemcget("P45", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P8", "fill"), Rt.sub_step_paint_canvas.itemcget("P11", "fill"), Rt.sub_step_paint_canvas.itemcget("P36", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P8", "fill"), Rt.sub_step_paint_canvas.itemcget("P11", "fill"), Rt.sub_step_paint_canvas.itemcget("P36", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P6", "fill"), Rt.sub_step_paint_canvas.itemcget("P29", "fill"), Rt.sub_step_paint_canvas.itemcget("P9", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P6", "fill"), Rt.sub_step_paint_canvas.itemcget("P29", "fill"), Rt.sub_step_paint_canvas.itemcget("P9", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P24", "fill"), Rt.sub_step_paint_canvas.itemcget("P53", "fill"), Rt.sub_step_paint_canvas.itemcget("P33", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P24", "fill"), Rt.sub_step_paint_canvas.itemcget("P53", "fill"), Rt.sub_step_paint_canvas.itemcget("P33", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P26", "fill"), Rt.sub_step_paint_canvas.itemcget("P44", "fill"), Rt.sub_step_paint_canvas.itemcget("P51", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P26", "fill"), Rt.sub_step_paint_canvas.itemcget("P44", "fill"), Rt.sub_step_paint_canvas.itemcget("P51", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P20", "fill"), Rt.sub_step_paint_canvas.itemcget("P17", "fill"), Rt.sub_step_paint_canvas.itemcget("P42", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P20", "fill"), Rt.sub_step_paint_canvas.itemcget("P17", "fill"), Rt.sub_step_paint_canvas.itemcget("P42", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P18", "fill"), Rt.sub_step_paint_canvas.itemcget("P15", "fill"), Rt.sub_step_paint_canvas.itemcget("P35", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P18", "fill"), Rt.sub_step_paint_canvas.itemcget("P15", "fill"), Rt.sub_step_paint_canvas.itemcget("P35", "fill")}))

            if len(set(self.cp)) != 8:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False
            #b = tm.perf_counter()
            if {Rt.sub_step_paint_canvas.itemcget("P50", "fill"), Rt.sub_step_paint_canvas.itemcget("P30", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P50", "fill"), Rt.sub_step_paint_canvas.itemcget("P30", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P48", "fill"), Rt.sub_step_paint_canvas.itemcget("P41", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P48", "fill"), Rt.sub_step_paint_canvas.itemcget("P41", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P14", "fill"), Rt.sub_step_paint_canvas.itemcget("P39", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P14", "fill"), Rt.sub_step_paint_canvas.itemcget("P39", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P12", "fill"), Rt.sub_step_paint_canvas.itemcget("P32", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P12", "fill"), Rt.sub_step_paint_canvas.itemcget("P32", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P1", "fill"), Rt.sub_step_paint_canvas.itemcget("P46", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P1", "fill"), Rt.sub_step_paint_canvas.itemcget("P46", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P5", "fill"), Rt.sub_step_paint_canvas.itemcget("P37", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P5", "fill"), Rt.sub_step_paint_canvas.itemcget("P37", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P7", "fill"), Rt.sub_step_paint_canvas.itemcget("P10", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P7", "fill"), Rt.sub_step_paint_canvas.itemcget("P10", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P3", "fill"), Rt.sub_step_paint_canvas.itemcget("P28", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P3", "fill"), Rt.sub_step_paint_canvas.itemcget("P28", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P25", "fill"), Rt.sub_step_paint_canvas.itemcget("P52", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P25", "fill"), Rt.sub_step_paint_canvas.itemcget("P52", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P23", "fill"), Rt.sub_step_paint_canvas.itemcget("P43", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P23", "fill"), Rt.sub_step_paint_canvas.itemcget("P43", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P19", "fill"), Rt.sub_step_paint_canvas.itemcget("P16", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P19", "fill"), Rt.sub_step_paint_canvas.itemcget("P16", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P21", "fill"), Rt.sub_step_paint_canvas.itemcget("P34", "fill")} in self.index_color_ep_list:
                self.ep.append(self.index_color_ep_list.index({Rt.sub_step_paint_canvas.itemcget("P21", "fill"), Rt.sub_step_paint_canvas.itemcget("P34", "fill")}))
            
            if len(set(self.ep)) != 12:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False
            #c = tm.perf_counter()
            if Rt.sub_step_paint_canvas.itemcget("P0", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P27", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P2", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P45", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P8", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P36", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P6", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P9", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P24", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P53", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P26", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P44", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P20", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P17", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)
            if Rt.sub_step_paint_canvas.itemcget("P18", "fill") in {"Yellow", "White"}:
                self.co.append(0)
            elif Rt.sub_step_paint_canvas.itemcget("P35", "fill") in {"Yellow", "White"}:
                self.co.append(1)
            else:
                self.co.append(2)

            if sum(self.co) % 3 != 0:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False
            #d = tm.perf_counter()
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P50", "fill"), Rt.sub_step_paint_canvas.itemcget("P30", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P50", "fill"), Rt.sub_step_paint_canvas.itemcget("P30", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P50", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P50", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if ("Yellow" in {Rt.sub_step_paint_canvas.itemcget("P48", "fill"), Rt.sub_step_paint_canvas.itemcget("P41", "fill")}) or ("White" in {Rt.sub_step_paint_canvas.itemcget("P48", "fill"), Rt.sub_step_paint_canvas.itemcget("P41", "fill")}):
                if Rt.sub_step_paint_canvas.itemcget("P48", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P48", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P14", "fill"), Rt.sub_step_paint_canvas.itemcget("P39", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P14", "fill"), Rt.sub_step_paint_canvas.itemcget("P39", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P14", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P14", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P12", "fill"), Rt.sub_step_paint_canvas.itemcget("P32", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P12", "fill"), Rt.sub_step_paint_canvas.itemcget("P32", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P12", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P12", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P1", "fill"), Rt.sub_step_paint_canvas.itemcget("P46", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P1", "fill"), Rt.sub_step_paint_canvas.itemcget("P46", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P1", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P1", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P5", "fill"), Rt.sub_step_paint_canvas.itemcget("P37", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P5", "fill"), Rt.sub_step_paint_canvas.itemcget("P37", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P5", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P5", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P10", "fill"), Rt.sub_step_paint_canvas.itemcget("P7", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P10", "fill"), Rt.sub_step_paint_canvas.itemcget("P7", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P7", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P7", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P3", "fill"), Rt.sub_step_paint_canvas.itemcget("P28", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P3", "fill"), Rt.sub_step_paint_canvas.itemcget("P28", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P3", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P3", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P25", "fill"), Rt.sub_step_paint_canvas.itemcget("P52", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P25", "fill"), Rt.sub_step_paint_canvas.itemcget("P52", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P25", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P25", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P23", "fill"), Rt.sub_step_paint_canvas.itemcget("P43", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P23", "fill"), Rt.sub_step_paint_canvas.itemcget("P43", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P23", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P23", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P19", "fill"), Rt.sub_step_paint_canvas.itemcget("P16", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P19", "fill"), Rt.sub_step_paint_canvas.itemcget("P16", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P19", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P19", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)
            if "Yellow" in {Rt.sub_step_paint_canvas.itemcget("P21", "fill"), Rt.sub_step_paint_canvas.itemcget("P34", "fill")} or "White" in {Rt.sub_step_paint_canvas.itemcget("P21", "fill"), Rt.sub_step_paint_canvas.itemcget("P34", "fill")}:
                if Rt.sub_step_paint_canvas.itemcget("P21", "fill") in {"Yellow", "White"}:
                    self.eo.append(0)
                else:
                    self.eo.append(1)
            elif Rt.sub_step_paint_canvas.itemcget("P21", "fill") in {"Blue", "Green"}:
                self.eo.append(0)
            else:
                self.eo.append(1)

            if sum(self.eo) % 2 != 0:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False
            #e = tm.perf_counter()
            arg_cp = list(self.cp)
            arg_ep = list(self.ep)

            if not bexe.check_parity(arg_cp, arg_ep):
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSome thing is wrong or this Rubik's cube cannot solve.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False

            if m == 1:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

                if self.ep[i] < 4 and self.ep[i] != -1:
                    if self.ep[i] + m >= 4:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
                elif self.ep[i] >= 4:
                    if self.ep[i] + m >= 8:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        elif pattern == 1:
            self.cp = []
            self.co = []
            self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.eo = []

            self.index_color_cp_list = [{"Yellow", "Green", "Dark Orange"}, {"Yellow", "Green", "Red"}, 
                                        {"Yellow", "Blue", "Red"}, {"Yellow", "Blue", "Dark Orange"},
                                        {"White", "Green", "Dark Orange"}, {"White", "Green", "Red"},
                                        {"White", "Blue", "Red"}, {"White", "Blue", "Dark Orange"}]

            if {Rt.sub_step_paint_canvas.itemcget("P0", "fill"), Rt.sub_step_paint_canvas.itemcget("P27", "fill"), Rt.sub_step_paint_canvas.itemcget("P47", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P0", "fill"), Rt.sub_step_paint_canvas.itemcget("P27", "fill"), Rt.sub_step_paint_canvas.itemcget("P47", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P2", "fill"), Rt.sub_step_paint_canvas.itemcget("P38", "fill"), Rt.sub_step_paint_canvas.itemcget("P45", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P2", "fill"), Rt.sub_step_paint_canvas.itemcget("P38", "fill"), Rt.sub_step_paint_canvas.itemcget("P45", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P8", "fill"), Rt.sub_step_paint_canvas.itemcget("P11", "fill"), Rt.sub_step_paint_canvas.itemcget("P36", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P8", "fill"), Rt.sub_step_paint_canvas.itemcget("P11", "fill"), Rt.sub_step_paint_canvas.itemcget("P36", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P6", "fill"), Rt.sub_step_paint_canvas.itemcget("P29", "fill"), Rt.sub_step_paint_canvas.itemcget("P9", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P6", "fill"), Rt.sub_step_paint_canvas.itemcget("P29", "fill"), Rt.sub_step_paint_canvas.itemcget("P9", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P24", "fill"), Rt.sub_step_paint_canvas.itemcget("P53", "fill"), Rt.sub_step_paint_canvas.itemcget("P33", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P24", "fill"), Rt.sub_step_paint_canvas.itemcget("P53", "fill"), Rt.sub_step_paint_canvas.itemcget("P33", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P26", "fill"), Rt.sub_step_paint_canvas.itemcget("P44", "fill"), Rt.sub_step_paint_canvas.itemcget("P51", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P26", "fill"), Rt.sub_step_paint_canvas.itemcget("P44", "fill"), Rt.sub_step_paint_canvas.itemcget("P51", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P20", "fill"), Rt.sub_step_paint_canvas.itemcget("P17", "fill"), Rt.sub_step_paint_canvas.itemcget("P42", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P20", "fill"), Rt.sub_step_paint_canvas.itemcget("P17", "fill"), Rt.sub_step_paint_canvas.itemcget("P42", "fill")}))
            if {Rt.sub_step_paint_canvas.itemcget("P18", "fill"), Rt.sub_step_paint_canvas.itemcget("P15", "fill"), Rt.sub_step_paint_canvas.itemcget("P35", "fill")} in self.index_color_cp_list:
                self.cp.append(self.index_color_cp_list.index({Rt.sub_step_paint_canvas.itemcget("P18", "fill"), Rt.sub_step_paint_canvas.itemcget("P15", "fill"), Rt.sub_step_paint_canvas.itemcget("P35", "fill")}))

            if len(set(self.cp)) != 8:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return False

            arg_cp = list(self.cp)
            arg_ep = list(self.ep)

            if not bexe.check_parity(arg_cp, arg_ep):
                self.ep[4], self.ep[5] = self.ep[5], self.ep[4]

            count = 0
            for i in ["P0", "P27", "P47"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P0", "P27", "P47"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.co.append(orient)

            count = 0
            for i in ["P2", "P45", "P38"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P2", "P45", "P38"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.co.append(orient)

            count = 0
            for i in ["P8", "P36", "P11"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P8", "P36", "P11"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.co.append(orient)

            count = 0
            for i in ["P6", "P9", "P29"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P6", "P9", "P29"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.co.append(orient)
            
            if sum(self.co) % 3 == 0:
                self.co += [0, 0, 0, 0]
            else:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with corners.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            count = 0
            for i in ["P1", "P46"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P1", "P46"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.eo.append(orient)

            count = 0
            for i in ["P5", "P37"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P5", "P37"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.eo.append(orient)

            count = 0
            for i in ["P7", "P10"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P7", "P10"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.eo.append(orient)

            count = 0
            for i in ["P3", "P28"]:
                if Rt.sub_step_paint_canvas.itemcget(i, "fill") == "Yellow":
                    count += 1
                    orient = ["P3", "P28"].index(i)
            if count != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return
            else:
                self.eo.append(orient)

            if sum(self.eo) % 2 == 0:
                self.eo = [0, 0, 0, 0] + self.eo + [0, 0, 0, 0]
            else:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nSomething is wrong with edges.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if m == 1:
                self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[7], self.eo[4], self.eo[5], self.eo[6]            
                self.co[0], self.co[1], self.co[2], self.co[3] = self.co[3], self.co[0], self.co[1], self.co[2]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[6], self.eo[7], self.eo[4], self.eo[5]            
                self.co[0], self.co[1], self.co[2], self.co[3] = self.co[2], self.co[3], self.co[0], self.co[1]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3] = self.co[1], self.co[2], self.co[3], self.co[0]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        elif pattern == 2:
            corner_list = [["P0", "P27", "P47"], ["P2", "P45", "P38"], ["P8", "P36", "P11"], ["P6", "P9", "P29"], ["P24", "P53", "P33"], ["P26", "P44", "P51"], ["P20", "P17", "P42"], ["P18", "P35", "P15"]]
            edge_list = [["P50", "P30"], ["P48", "P41"], ["P14", "P39"], ["P12", "P32"], ["P1", "P46"], ["P5", "P37"], ["P7", "P10"], ["P3", "P28"]]
            num = 0

            self.cp = [-1, -1, -1, -1, 4, 5, -1, 7]
            self.co = [-1, -1, -1, -1, 0, 0, -1, 0]
            self.ep = [0, 1, -1, 3, -1, -1, -1, -1, 8, 9, 10, 11]
            self.eo = [0, 0, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0]

            for index, value in enumerate(corner_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill"), Rt.sub_step_paint_canvas.itemcget(value[2], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"White", "Blue", "Red"}:
                    num += 1
                    self.cp[index] = 6
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i

            if num != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n2 or more LS corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"Blue", "Red"}:
                    num += 1
                    self.ep[index] = 2
                    if get_colors[0] == "Blue":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1
            
            if num != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n2 or more LS edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                if index in (2, 4, 5, 6, 7):
                    get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                    if "Yellow" in get_colors:
                        num += 1
                        if get_colors[0] == "Yellow":
                            self.eo[index] = 0
                        else:
                            self.eo[index] = 1
            
            if num != 4:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nless edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if m == 1:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

                if self.ep[i] < 4 and self.ep[i] != -1:
                    if self.ep[i] + m >= 4:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
                elif self.ep[i] >= 4:
                    if self.ep[i] + m >= 8:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
        
            for i in self.ep:
                if i == (2 + m) % 4 and 3 < self.ep.index(i) < 8:
                    self.eo[self.ep.index(i)] = (self.eo[self.ep.index(i)] + m) % 2
                    self.eo[i] = (self.eo[i] + m) % 2

            if sum(self.eo) % 2 == 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nedges miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            ep_diff = [i for i in range(12) if not(i in self.ep)]
            for i in range(12):
                if self.ep[i] == -1:
                    self.ep[i] = ep_diff[0]
                    ep_diff.pop(0)

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        elif pattern == 3:
            corner_list = [["P0", "P27", "P47"], ["P2", "P45", "P38"], ["P8", "P36", "P11"], ["P6", "P9", "P29"], ["P24", "P53", "P33"], ["P26", "P44", "P51"], ["P20", "P17", "P42"], ["P18", "P35", "P15"]]
            edge_list = [["P50", "P30"], ["P48", "P41"], ["P14", "P39"], ["P12", "P32"], ["P1", "P46"], ["P5", "P37"], ["P7", "P10"], ["P3", "P28"]]
            num = 0

            self.cp = [-1, -1, -1, -1, 4, 5, -1, 7]
            self.co = [-1, -1, -1, -1, 0, 0, -1, 0]
            self.ep = [0, 1, -1, 3, -1, -1, -1, -1, 8, 9, 10, 11]
            self.eo = [0, 0, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0]

            for index, value in enumerate(corner_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill"), Rt.sub_step_paint_canvas.itemcget(value[2], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"White", "Blue", "Red"}:
                    num += 1
                    self.cp[index] = 6
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i

            if num != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n2 or more LS corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"Blue", "Red"}:
                    num += 1
                    self.ep[index] = 2
                    if get_colors[0] == "Blue":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1

            if num != 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n2 or more LS edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                if index in (2, 4, 5, 6, 7):
                    get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                    if "Yellow" in get_colors:
                        num += 1
                        if get_colors[0] == "Yellow":
                            self.eo[index] = 0
                        else:
                            self.eo[index] = 1

            if num != 4:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nless edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(corner_list):
                if index in (0, 1, 2, 3, 6):
                    get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill"), Rt.sub_step_paint_canvas.itemcget(value[2], "fill")]
                    if "Yellow" in get_colors:
                        num += 1
                        for i in range(3):
                            if get_colors[i] == "Yellow":
                                self.co[index] = i

            if num != 4:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nless corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if m == 1:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

                if self.ep[i] < 4 and self.ep[i] != -1:
                    if self.ep[i] + m >= 4:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
                elif self.ep[i] >= 4:
                    if self.ep[i] + m >= 8:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m

            for i in self.ep:
                if i == (2 + m) % 4 and 3 < self.ep.index(i) < 8:
                    self.eo[self.ep.index(i)] = (self.eo[self.ep.index(i)] + m) % 2
                    self.eo[i] = (self.eo[i] + m) % 2

            if sum(self.eo) % 2 == 1:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \nedges miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if sum(self.co) % 3 != 0:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \ncorners miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            ep_diff = [i for i in range(12) if not(i in self.ep)]
            for i in range(12):
                if self.ep[i] == -1:
                    self.ep[i] = ep_diff[0]
                    ep_diff.pop(0)

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        elif pattern == 4:
            corner_list = [["P0", "P27", "P47"], ["P2", "P45", "P38"], ["P8", "P36", "P11"], ["P6", "P9", "P29"], ["P24", "P53", "P33"], ["P26", "P44", "P51"], ["P20", "P17", "P42"], ["P18", "P35", "P15"]]
            edge_list = [["P50", "P30"], ["P48", "P41"], ["P14", "P39"], ["P12", "P32"], ["P1", "P46"], ["P5", "P37"], ["P7", "P10"], ["P3", "P28"]]
            num = 0

            self.cp = [-1, -1, -1, -1, 4, -1, -1, 7]
            self.co = [-1, -1, -1, -1, 0, -1, -1, 0]
            self.ep = [0, -1, -1, 3, -1, -1, -1, -1, 8, 9, 10, 11]
            self.eo = [0, -1, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0]

            for index, value in enumerate(corner_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill"), Rt.sub_step_paint_canvas.itemcget(value[2], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"White", "Blue", "Red"}:
                    num += 1
                    self.cp[index] = 6
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i
                elif set_get_colors == {"White", "Green", "Red"}:
                    num += 1
                    self.cp[index] = 5
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i

            if num != 2:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n3 or more corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"Blue", "Red"}:
                    num += 1
                    self.ep[index] = 2
                    if get_colors[0] == "Blue":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1
                if set_get_colors == {"Green", "Red"}:
                    num += 1
                    self.ep[index] = 1
                    if get_colors[0] == "Green":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1

            if num != 2:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n3 or more edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if m == 1:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

                if self.ep[i] < 4 and self.ep[i] != -1:
                    if self.ep[i] + m >= 4:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
                elif self.ep[i] >= 4:
                    if self.ep[i] + m >= 8:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m

            for i in range(4, 8):
                if self.eo[i] != -1:
                    self.eo[i] = (self.eo[i] + m) % 2

            if self.eo.count(1) % 2 == 0:
                self.eo = [i if i != -1 else 0 for i in self.eo]
            else:
                for i in range(8):
                    if self.eo[i] == -1:
                        self.eo[i] = 1
                        break
                self.eo = [i if i != -1 else 0 for i in self.eo]

            ep_diff = [i for i in range(12) if not(i in self.ep)]
            for i in range(12):
                if self.ep[i] == -1:
                    self.ep[i] = ep_diff[0]
                    ep_diff.pop(0)

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        elif pattern == 5:
            corner_list = [["P0", "P27", "P47"], ["P2", "P45", "P38"], ["P8", "P36", "P11"], ["P6", "P9", "P29"], ["P24", "P53", "P33"], ["P26", "P44", "P51"], ["P20", "P17", "P42"], ["P18", "P35", "P15"]]
            edge_list = [["P50", "P30"], ["P48", "P41"], ["P14", "P39"], ["P12", "P32"], ["P1", "P46"], ["P5", "P37"], ["P7", "P10"], ["P3", "P28"]]
            num = 0

            self.cp = [-1, -1, -1, -1, -1, 5, -1, 7]
            self.co = [-1, -1, -1, -1, -1, 0, -1, 0]
            self.ep = [-1, 1, -1, 3, -1, -1, -1, -1, 8, 9, 10, 11]
            self.eo = [-1, 0, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0]

            for index, value in enumerate(corner_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill"), Rt.sub_step_paint_canvas.itemcget(value[2], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"White", "Blue", "Red"}:
                    num += 1
                    self.cp[index] = 6
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i
                elif set_get_colors == {"White", "Green", "Dark Orange"}:
                    num += 1
                    self.cp[index] = 4
                    for i in range(3):
                        if get_colors[i] == "White":
                            self.co[index] = i

            if num != 2:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n3 or more corners painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            num = 0

            for index, value in enumerate(edge_list):
                get_colors = [Rt.sub_step_paint_canvas.itemcget(value[0], "fill"), Rt.sub_step_paint_canvas.itemcget(value[1], "fill")]
                set_get_colors = set(get_colors)
                if set_get_colors == {"Blue", "Red"}:
                    num += 1
                    self.ep[index] = 2
                    if get_colors[0] == "Blue":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1
                if set_get_colors == {"Green", "Dark Orange"}:
                    num += 1
                    self.ep[index] = 1
                    if get_colors[0] == "Green":
                        self.eo[index] = 0
                    else:
                        self.eo[index] = 1

            if num != 2:
                Rt.explor_sub_step_Box.insert("end", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \
                    \n3 or more edges painted or miss painted\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
                Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED
                return

            if m == 1:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[3], self.eo[0], self.eo[1], self.eo[2], self.eo[7], self.eo[4], self.eo[5], self.eo[6]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[3], self.co[0], self.co[1], self.co[2], self.co[7], self.co[4], self.co[5], self.co[6]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[3], self.ep[0], self.ep[1], self.ep[2], self.ep[7], self.ep[4], self.ep[5], self.ep[6]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[3], self.cp[0], self.cp[1], self.cp[2], self.cp[7], self.cp[4], self.cp[5], self.cp[6]

            elif m == 2:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[2], self.eo[3], self.eo[0], self.eo[1], self.eo[6], self.eo[7], self.eo[4], self.eo[5]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[2], self.co[3], self.co[0], self.co[1], self.co[6], self.co[7], self.co[4], self.co[5]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[2], self.ep[3], self.ep[0], self.ep[1], self.ep[6], self.ep[7], self.ep[4], self.ep[5]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[2], self.cp[3], self.cp[0], self.cp[1], self.cp[6], self.cp[7], self.cp[4], self.cp[5]

            elif m == 3:
                self.eo[0], self.eo[1], self.eo[2], self.eo[3], self.eo[4], self.eo[5], self.eo[6], self.eo[7] = self.eo[1], self.eo[2], self.eo[3], self.eo[0], self.eo[5], self.eo[6], self.eo[7], self.eo[4]
                self.co[0], self.co[1], self.co[2], self.co[3], self.co[4], self.co[5], self.co[6], self.co[7] = self.co[1], self.co[2], self.co[3], self.co[0], self.co[5], self.co[6], self.co[7], self.co[4]
                self.ep[0], self.ep[1], self.ep[2], self.ep[3], self.ep[4], self.ep[5], self.ep[6], self.ep[7] = self.ep[1], self.ep[2], self.ep[3], self.ep[0], self.ep[5], self.ep[6], self.ep[7], self.ep[4]
                self.cp[0], self.cp[1], self.cp[2], self.cp[3], self.cp[4], self.cp[5], self.cp[6], self.cp[7] = self.cp[1], self.cp[2], self.cp[3], self.cp[0], self.cp[5], self.cp[6], self.cp[7], self.cp[4]

            for i in range(8):
                if self.cp[i] < 4 and self.cp[i] != -1:
                    if self.cp[i] + m >= 4:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m
                elif self.cp[i] >= 4:
                    if self.cp[i] + m >= 8:
                        self.cp[i] = self.cp[i] + m - 4
                    else:
                        self.cp[i] += m

                if self.ep[i] < 4 and self.ep[i] != -1:
                    if self.ep[i] + m >= 4:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m
                elif self.ep[i] >= 4:
                    if self.ep[i] + m >= 8:
                        self.ep[i] = self.ep[i] + m - 4
                    else:
                        self.ep[i] += m

            for i in range(4, 8):
                if self.eo[i] != -1:
                    self.eo[i] = (self.eo[i] + m) % 2

            if self.eo.count(1) % 2 == 0:
                self.eo = [i if i != -1 else 0 for i in self.eo]
            else:
                for i in range(8):
                    if self.eo[i] == -1:
                        self.eo[i] = 1
                        break
                self.eo = [i if i != -1 else 0 for i in self.eo]

            ep_diff = [i for i in range(12) if not(i in self.ep)]
            for i in range(12):
                if self.ep[i] == -1:
                    self.ep[i] = ep_diff[0]
                    ep_diff.pop(0)

            # print(self.co)
            # print(self.cp)
            # print(self.eo)
            # print(self.ep)

        Ex_available_list = [str(int(Rt.Ex4_var1.get())),
                        str(int(Rt.Ex4_var2.get())),
                        str(int(Rt.Ex4_var3.get())),
                        str(int(Rt.Ex4_var4.get())),
                        str(int(Rt.Ex4_var5.get())),
                        str(int(Rt.Ex4_var6.get())),
                        str(int(Rt.Ex4_var7.get())),
                        str(int(Rt.Ex4_var8.get())),
                        str(int(Rt.Ex4_var9.get())),
                        str(int(Rt.Ex4_var10.get())),
                        str(int(Rt.Ex4_var11.get())),
                        str(int(Rt.Ex4_var12.get())),
                        str(int(Rt.Ex4_var13.get())),
                        str(int(Rt.Ex4_var14.get())),
                        str(int(Rt.Ex4_var15.get()))
                        ]

        arg_CP = " ".join(map(str, self.cp))
        arg_CO = " ".join(map(str, self.co))
        arg_EP = " ".join(map(str, self.ep))
        arg_EO = " ".join(map(str, self.eo))

        # print(Rt.usebracket_button4.cget("state"), Rt.Ex4_startfrom2_sub_step_comb["state"])

        forbid_list = [0, 15, 12]
        forbidden = str(forbid_list[n]) if str(Rt.Ex4_startfrom2_sub_step_comb["state"]) == "readonly" else "-1"
        adjust = str(Rt.auf_var4.get()) if str(Rt.usebracket_button4["state"]) == tk.NORMAL else "-1"

        cmd = "CubeSE.exe " + arg_CP +  " " + arg_CO + " " + arg_EP + " " + arg_EO + " 0 1 2 3 4 5 " + " ".join(Ex_available_list) + " " + Solution1 + " " + Solution2 + " " + Solution3 + " " + str(int(Rt.Ex4_var0.get()) * 2 + Rt.htm_var4.get()) + " " + forbidden + " " + adjust + " " + str(pattern) + " " + "sub_step"

        print(cmd)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        Rt.explor_sub_step_Box.insert("end", "・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・・\n")
        #a = time.perf_counter()

        #ID = root.after(int((Solution3 + 1.457) * 1000), Rt.Explorer_Exit_thread)

        self.search = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, startupinfo=startupinfo)
        for line in iter(sub_stepex.search.stdout.readline, b''):
            #print(time.perf_counter() - a)
            Rt.explor_sub_step_Box.insert("end", line.rstrip().decode('sjis') + "\n")
            Rt.explor_sub_step_Box.see("end")

        """self.solution = search.start_search(min_length = int(Solution1), \
            max_length = int(Solution2))"""
        #print(time.perf_counter() - a)
        Rt.explor_sub_step_Box.insert("end", f"Finished!\n")
        Rt.Button_explor_sub_step_start["state"] = tk.NORMAL
        Rt.Button_explor_sub_step_exit["state"] = tk.DISABLED

        return

Rt = Roots()
exe = Execution()
bexe = B_Execution()
pllex = PLL_Ex()
ollex = OLL_Ex()
f2lex = F2L_Ex()
sub_stepex = sub_step_Ex()

Rt.Prepare_Start()

root.mainloop()