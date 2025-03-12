import tkinter as tk
root = tk.Tk()
import random
import webbrowser

oldnum_array = []
oldnum_array.clear()
oldnum_array.append('10')

score = 0
score_array = []
score_array.clear()
score_array.append('0')

print(' your current number is: 10')

#command definitions 
def higher():
    new_num=random.randint(1,20)
    old_num = int(oldnum_array[0])
    if new_num>old_num:
        score = int(score_array[0])
        score = score+1
        score_array.clear()
        score_array.append(score)
        print('correct')
        print('your score is: ', score_array[0])

        old_num = new_num
        print('your current number is: ', old_num)
        oldnum_array.clear()
        oldnum_array.append(old_num)


    elif new_num<old_num:
        score = int(score_array[0])
        score = score-1
        score_array.clear()
        score_array.append(score)
        print('incorrect')
        print('your score is: ', score_array[0])

        old_num = new_num
        print('your current number is: ', old_num)
        oldnum_array.clear()
        oldnum_array.append(old_num)

        print(' ')

def lower():
    new_num=random.randint(1,20)
    old_num = int(oldnum_array[0])
    if new_num>old_num:
        score = int(score_array[0])
        score = score-1
        score_array.clear()
        score_array.append(score)
        print('incorrect')
        print('your score is: ', score_array[0])

        old_num = new_num
        print('your current number is: ', old_num)
        oldnum_array.clear()
        oldnum_array.append(old_num)

        print(' ')

    elif new_num<old_num:
        score = int(score_array[0])
        score = score+1
        score_array.clear()
        score_array.append(score)
        print(score_array[0])

        old_num = new_num
        print('your current number is: ', old_num)
        print('correct')
        print('your score is: ', score_array[0])

        print(' ')

def name_append():
    name = entry1.get()

    name_list = open('scores.txt','a')
    name_list.write('\n' + name)
    name_list.close()

    but_backout['state'] = tk.NORMAL
    but_high['state'] = tk.NORMAL
    but_low['state'] = tk.NORMAL

    but_namecheck['state'] = tk.DISABLED

def back_out():
    score = score_array[0]
    score_list = open('scores.txt','a')
    score_list.write(' - ')
    score_list.write(str(score))
    score_list.close()

    root.destroy()

    print('your score is: ', score)

#button definitions
but_high = tk.Button(root,
                    text = 'Higher', 
                    bg = 'green',
                    padx= 90,
                    pady=160, 
                    highlightbackground = '#009600', 
                    activebackground = '#009600', 
                    command = higher,
                    state = tk.DISABLED
                    )

but_low = tk.Button(root, 
                    text = 'lower',
                    bg = 'red', 
                    padx= 94, 
                    pady= 160,
                    highlightbackground = '#960000', 
                    activebackground= '#960000', 
                    command = lower,
                    state = tk.DISABLED
                    )

but_backout = tk.Button(root,
                    text = 'back-out',
                    command = back_out,
                    padx = 50,
                    pady = 60,
                    state = tk.DISABLED
                    )

but_namecheck = tk.Button(root, 
                    text = 'check name', 
                    command = name_append,
                    padx = 41,
                    pady = 60
                    )

entry1 = tk.Entry(root)
#button grid
but_high.grid(row=0,
            column=0, 
            rowspan=3)

but_low.grid(row=0,
            column=2, 
            rowspan=3)

but_backout.grid(row=0,
            column=1)

but_namecheck.grid(row=2,
            column=1)

entry1.grid(row=1,
            column=1)

root.mainloop()
