from tkinter import *
root = Tk()

root.geometry('800x450')

def upper_hue_change(event):
    upper_hue_value = round(upper_hue_slider.get())
    print('The Upper Bound Hue Value is: ', upper_hue_value)

upper_hue_slider = Scale(
    root,
    from_=0,
    to=180,
    length=750,
    tickinterval=10,
    orient='horizontal',
    command=upper_hue_change,
)

upper_hue_label = Label(root,
    text='Upper Bound Hue Value'
)



def lower_hue_change(event):
    lower_hue_value = round(lower_hue_slider.get())
    print('The lower Bound Hue Value is: ', lower_hue_value)

lower_hue_slider = Scale(
    root,
    from_=0,
    to=180,
    length=750,
    tickinterval=10,
    orient='horizontal',
    command=lower_hue_change,
)

lower_hue_label = Label(
    root,
    text='Lower Bound Hue Value'
)


def upper_saturation_change(event):
    upper_saturation_value = round(upper_saturation_slider.get())
    print('The Upper Bound Saturation Value is: ', upper_saturation_value)

upper_saturation_slider = Scale(
    root,
    from_=0,
    to=250,
    length=750,
    tickinterval=10,
    orient='horizontal',
    command=upper_saturation_change,
)

upper_saturation_label = Label(
    root,
    text='Upper Bound Saturation Value'
)



def lower_saturation_change(event):
    lower_saturation_value = round(lower_saturation_slider.get())
    print('The Lower Bound Saturation Value is: ', lower_saturation_value)

lower_saturation_slider = Scale(
    root,
    from_=0,
    to=250,
    length=750,
    tickinterval=10,
    orient='horizontal',
    command=lower_saturation_change,
)

lower_saturation_label = Label(
    root,
    text='Lower Bound Saturation Value'
)



#pack() for upper and lower hue boundaries
upper_hue_label.pack()
upper_hue_slider.pack()
lower_hue_label.pack()
lower_hue_slider.pack()

#pack() for upper and lower saturation boundaries
upper_saturation_label.pack()
upper_saturation_slider.pack()
lower_saturation_label.pack()
lower_saturation_slider.pack()

root.mainloop()