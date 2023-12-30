import tkinter as tk
from tkinter import ttk
from itertools import product
import numexpr # type: ignore
import re

'''Method for adding Button input'''
def write_to_box(char_):
    full_text_box = calc_input.get('1.0','end-1c')
    equation = calc_output.cget('text')

    if (char_ == "." and ("." in full_text_box or full_text_box == "")) or char_ not in "^0123456789.()/*-+": #check if char_ is valid input
        return
    elif char_ in "0123456789.": # check if input(char_) is to append into box(calc_input)
        calc_input.insert('end-1c', char_)
    elif calc_output.cget('text')[-1:] in "/*-+^" and full_text_box == "" and equation != "":
        calc_output.config(text=calc_output.cget('text')[0:-1] + char_)
    else: # if input is not to append in box (is an mathematical character '+-*/') append to the equation label (calc_output) 
        add_to_output(char_)
        clear()

'''Method for evaluation, getting result'''
def evaluating():
    check_key_input()
    add_to_output() # append input to equation
    equation = calc_output.cget('text')
    while equation.count('(') > equation.count(')'):
        equation += ')'
    try:
        result = numexpr.evaluate(equation.replace('^', '**')) # evaluate the equation
        if result == int(result): # check if result "#.0"
            result = int(result)
        calc_output.config(text=equation)
        clear()
        calc_input.insert('1.0',result) # write result into text box
    except: # catch if eqaution has invalid syntax
        print("invalid equation")


'''Methods for clearing'''
def clear_all(): # delete current input box and equation label
    clear()
    calc_output.config(text="")
def clear(): # delete current input box
    calc_input.delete(1.0,"end")

'''Method for adding opening Bracket'''
def bracket_l():
    input_string = calc_input.get('1.0', 'end-1c')
    output_string = calc_output.cget('text')
    if input_string[-1:] in "0123456789" and input_string != "": # check if last character is digit and missed a operator and add '*'
        add_to_output("*(")
    else:
        add_to_output("(")
    clear()

'''Method for adding closing Bracket'''
def bracket_r():
    equation = calc_output.cget('text')
    if equation.count("(") > equation.count(")"):
        if equation[-1:] == "(":
            add_to_output("0)")
        else:
            add_to_output(")")


'''Method for tracking keyboard input into Text box'''
def check_key_input(_=''):
    cleaned = re.sub("[^0123456789\(\)\./*\-+\^]","",calc_input.get('1.0','end-1c'))
    clear()
    calc_input.insert('1.0', cleaned)

'''Method for adding char_ and text box into equation'''
def add_to_output(char_=""):
    if char_ in "^0123456789()./*-+":
        calc_output.config(text= f"{calc_output.cget('text')}{calc_input.get('1.0','end-1c')}{char_}")
        clear()

'''main window'''
root = tk.Tk()
root.title('Calculater Deluxe')

'''Scaling Window and Widgets'''
scale_ = 2.5 #scaling value
root.tk.call('tk', 'scaling', scale_) # scaling window
root.geometry("200x320") # set window pixel size
#root.resizable(0,0)

'''Placing options'''
gap_size_y = 40 # row height -> pixels to next vertical button
gap_size_x = 28 # column width -> pixels to next horizontal button
offset_y = 140 # row offset of Buttons
offset_x = 10 # column offset of Buttons

'''Text box for input'''
calc_input = tk.Text(root, height=1,width=12) # input box
calc_input.place(x=10,y=40)
calc_input.bind('<KeyRelease>', check_key_input)
calc_input.edit_modified(True)

'''Label for equation and result'''
calc_output = ttk.Label(root, text = "", width=12, anchor="e") # label for equation and result
calc_output.place(x=30,y=2)

'''Buttons for digits'''
number_btns = [] # Button 0-9 Container
number_btns.append(ttk.Button(root,text=f"0", command= lambda: write_to_box("0"), width = 3))
number_btns.append(ttk.Button(root,text=f"1", command= lambda: write_to_box("1"), width = 3))
number_btns.append(ttk.Button(root,text=f"2", command= lambda: write_to_box("2"), width = 3))
number_btns.append(ttk.Button(root,text=f"3", command= lambda: write_to_box("3"), width = 3))
number_btns.append(ttk.Button(root,text=f"4", command= lambda: write_to_box("4"), width = 3))
number_btns.append(ttk.Button(root,text=f"5", command= lambda: write_to_box("5"), width = 3))
number_btns.append(ttk.Button(root,text=f"6", command= lambda: write_to_box("6"), width = 3))
number_btns.append(ttk.Button(root,text=f"7", command= lambda: write_to_box("7"), width = 3))
number_btns.append(ttk.Button(root,text=f"8", command= lambda: write_to_box("8"), width = 3))
number_btns.append(ttk.Button(root,text=f"9", command= lambda: write_to_box("9"), width = 3))

'''Buttons 0-9'''
counter = 10 #counting flag
for y_, x_ in product(range(3), range(3,0,-1)): # place the Buttons 1-9
    number_btns[counter-1].place(x=offset_x+ (x_-1)*gap_size_x*(scale_-1), y=offset_y+ y_*gap_size_y*(scale_/2.5))
    #making a 3x3           for new new column^^^^              ^^^^^^^^scale factor
    counter-=1
number_btns[0].place(x=offset_x + gap_size_x * 1 *(scale_-1), y= offset_y + gap_size_y *3 *(scale_/2.5)) #Place the Button 0
root.update_idletasks()

''' Button for the decimal dot'''
float_btn = ttk.Button(root, text="0", command= lambda: write_to_box(f"."), width = 3) 
float_btn.place( x= number_btns[1].winfo_x(), y= number_btns[0].winfo_y())
float_btn.config(text=",")

'''Button to clear input box and output label'''
clear_all_btn = ttk.Button(root, text="0", command=clear_all, width = 3)
clear_all_btn.place(x=number_btns[9].winfo_x() + gap_size_x*(scale_-1), y= number_btns[9].winfo_y() - gap_size_y*(scale_/2.5))
clear_all_btn.config(text="CA")
root.update_idletasks()

'''Button to clear input box'''
#clear_btn = ttk.Button(root, text="C", command = clear, width = 3)
#clear_btn.place(x=number_btns[9].winfo_x(), y= clear_all_btn.winfo_y())

'''Buttons for Brackes ()'''
bracket_left_btn = ttk.Button(root, text="0", command=bracket_l, width = 3)
bracket_left_btn.place(x=number_btns[8].winfo_x(), y= clear_all_btn.winfo_y())
bracket_left_btn.config(text="(")
bracket_right_btn = ttk.Button(root, text="0", command=bracket_r, width = 3)
bracket_right_btn.place(x=number_btns[9].winfo_x(), y= clear_all_btn.winfo_y())
bracket_right_btn.config(text=")")

'''Button to power'''
pow_btn = ttk.Button(root, text="0", command= lambda: write_to_box(f"^"), width = 3)
pow_btn.place(x=number_btns[7].winfo_x(), y= clear_all_btn.winfo_y())
pow_btn.config(text="xⁿ")

'''Button to divide'''
div_btn = ttk.Button(root, text="/", command= lambda: write_to_box(f"/"), width = 3)
div_btn.place(x=clear_all_btn.winfo_x(), y= number_btns[7].winfo_y())

'''Button to multiplicate'''
mult_btn = ttk.Button(root, text="X", command= lambda: write_to_box(f"*"), width = 3)
mult_btn.place(x=clear_all_btn.winfo_x(), y= number_btns[4].winfo_y())

'''Button to subtract'''
sub_btn = ttk.Button(root, text="-", command= lambda: write_to_box(f"-"), width = 3)
sub_btn.place(x=clear_all_btn.winfo_x(), y= number_btns[1].winfo_y())

'''Button to add'''
add_btn = ttk.Button(root, text="+", command= lambda: write_to_box(f"+"), width = 3)
add_btn.place(x= clear_all_btn.winfo_x(), y= number_btns[0].winfo_y())

'''Button to evalate, get result'''
equal_btn = ttk.Button(root, text= "0", command = evaluating, width = 3)
equal_btn.place(x= number_btns[9].winfo_x(), y= number_btns[0].winfo_y())
equal_btn.config(text="=")

if __name__ == "__main__":
    root.mainloop()
else:
    root.update()
    root.dooneevent()


'''
Upcoming Features:
+split bracket button () zu ( und )
 >count open brackets -> max 25
+change operator when no new input was given yet
+write operator(auch brackets) only in equation


'''