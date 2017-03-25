from Tkinter import *
import Tkinter as tk
import ttk
import zipfile
import ImageTk
import tkFont
from PIL import Image
import StringIO
import tkFileDialog as fd
import tkMessageBox
import pickle
import os
import xml.etree.ElementTree as ET

# Indenting problems

def indent(text, amount, ch=' '):
    padding = amount * ch
    return ''.join(padding+line for line in text.splitlines(True))


# Tooltips

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Main windows

root = Tk() # create a Tk root window
root.wm_title("Neural Network Toolbox")
# Window variables
w = 1024 # width for the Tk root
h = 730 # height for the Tk root
tkFont.Font(family="Times", size=10, weight=tkFont.BOLD)
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # set the dimensions of the screen and where it is placed

def debug(o):
    print "debug: "+o

def about():
    print "HELP"

##################

def resize(s):
    print s

# Custom functions

target_directory = None
target_directory_testing = None

def multiple_t(n):
    return "\t"*n

def compile_python():
    global en, xml_reader
    myfile = open("load_dataset_original.py","r")
    load_database_txt = myfile.read()


    myfile = open("network_original.py","r")
    model_txt = myfile.read()



    load_database_txt = load_database_txt.replace("<<SET_LABELS>>", xml_reader[1].replace("\n","\n"+multiple_t(code_part[1][2])).replace("\t","    "))
    load_database_txt = load_database_txt.replace("<<READ_XML_LABELS>>", xml_reader[0].replace("\n","\n"+multiple_t(code_part[0][2])).replace("\t","    "))
    load_database_txt = load_database_txt.replace("<<OTHER>>", xml_reader[2].replace("\n","\n"+multiple_t(code_part[2][2])).replace("\t","    "))
    if en.get() == "":
        target_directory = "<Replace with target directory>"
        load_database_txt = load_database_txt.replace("<<DATA_FOLDER>>", "'"+str(target_directory)+"'")
    else:
        load_database_txt = load_database_txt.replace("<<DATA_FOLDER>>","'"+ str(en.get())+"'")

    model_txt = model_txt.replace("<<TRAIN>>", eval_reader[0].replace("\n","\n"+multiple_t(code_part_eval[0][2])).replace("\t","    "))
    model_txt = model_txt.replace("<<TEST>>", eval_reader[1].replace("\n","\n"+multiple_t(code_part_eval[1][2])).replace("\t","    "))
    model_txt = model_txt.replace("<<OTHER>>", eval_reader[2].replace("\n","\n"+multiple_t(code_part_eval[2][2])).replace("\t","    "))

    text_file = open("load_dataset.py", "w")
    text_file.write("%s" % load_database_txt)
    text_file.close()

    text_file = open("network.py", "w")
    text_file.write("%s" % model_txt)
    text_file.close()



def target_folder():
    global target_directory
    target_directory = fd.askdirectory()+str("/")

def target_folder2():
    global target_directory_testing
    target_directory_testing = fd.askdirectory()+str("/")

# Xml Reader part

event_set = ["Read xml annotations", "Create labels","Other"]
code_part = [("",[800,600]) for i in range(len(event_set))]
code_part[0] =  "\ndef read_annotations(xml_path):" \
                "\n\t" \
                "\n\t# Given the path of the xml file, create the label"\
                "\n\troot = xml.etree.ElementTree.parse(xml_path).getroot()"\
                "\n\tcategory = root[0].attrib['name']"\
                "\n"\
                "\n\t# if this annotation should be skipped, set skip to True"\
                "\n\tskip = False"\
                "\n\treturn int(category),skip",[800,600],0

code_part[1] =  "\n# We have read the xml annotations and category is available." \
                "\n# Change the code below to set a proper target for the datum\n" \
                "\ny[datums,:] = one_hot(category,max_labels=10)",[800,600],3

code_part[2] =  "\n# Miscellaneous code goes here",[800,600],0

# Xml getter
code_text_widget = [None for i in range(len(code_part))]
xml_reader = [code_part[i][0] for i in range(len(code_part))]

def reader(e,index):
    global code_text_getter, xml_reader,code_text_widget
    xml_reader[index] = code_text_widget[index].get("1.0",END)

def xml_parser_popup(index):
    global xml_reader, code_text_Getter
    toplevel = Toplevel()
    w,h = 650,400
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    code_text_widget[index] = Text(toplevel,width=w)
    code_text_widget[index].grid(column=0,row=0)
    code_text_widget[index].insert(END,xml_reader[index])
    code_text_widget[index].bind('<KeyRelease>', lambda event, i=index: reader(event,i))
    code_text_widget[index].focus_set()


# Canvas nodes, redraws

nodes = []

def visual_position(a,n=0):
    global myzoom, origin_location

    if n == 0:
        a = (a-origin_location[0])
    else:
        a = (a-origin_location[1])

    return a

def draw(module):
    if module.selected:
        w.create_rectangle((module.position[0]-module.width+origin_location[0]),(module.position[1]-40+origin_location[1]), (module.position[0]+module.width+origin_location[0]), (module.position[1]+40+origin_location[1]), fill="red",outline="black",width=1)
    else:
        w.create_rectangle((module.position[0]-module.width+origin_location[0]),(module.position[1]-40+origin_location[1]), (module.position[0]+module.width+origin_location[0]), (module.position[1]+40+origin_location[1]), fill="dim gray",outline="black",width=1)

    w.create_text((module.position[0]+origin_location[0]),(module.position[1]+origin_location[1]), fill="yellow",text=module.name,font=("Purisa", 12,tkFont.BOLD))

    for connection in module.connection_to:
        target = connection.position
        #print module.position[0]+module.width, (target[0]+module.position[0]-connection.width)/2.0+origin_location[0]
        #myline = w.create_line(module.position[0]+origin_location[0]+module.width,module.position[1]+origin_location[1],target[0]+origin_location[0]-connection.width,target[1]+origin_location[1],fill="red",width=4)
        myline = w.create_line(module.position[0]+origin_location[0]+module.width,module.position[1]+origin_location[1],(target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],module.position[1]+origin_location[1],fill="black",width=5)
        myline = w.create_line((target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],target[1]+origin_location[1],target[0]+origin_location[0]-connection.width,target[1]+origin_location[1],fill="black",width=5)
        myline = w.create_line((target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],module.position[1]+origin_location[1],(target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],target[1]+origin_location[1],fill="black",width=5)
        myline = w.create_line(module.position[0]+origin_location[0]+module.width,module.position[1]+origin_location[1],(target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],module.position[1]+origin_location[1],fill="blue",width=3)
        myline = w.create_line((target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],target[1]+origin_location[1],target[0]+origin_location[0]-connection.width,target[1]+origin_location[1],fill="blue",width=3)
        myline = w.create_line((target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],module.position[1]+origin_location[1],(target[0]+module.position[0]+module.width-connection.width)/2.0+origin_location[0],target[1]+origin_location[1],fill="blue",width=3)
        w.tag_raise(myline)
    o1 = w.create_oval((module.position[0]+origin_location[0]-5-module.width),(module.position[1]+origin_location[1]-5), (module.position[0]+origin_location[0]+5-module.width),(module.position[1]+origin_location[1]+5),fill="blue",outline="black",width=1)
    o2 = w.create_oval((module.position[0]+origin_location[0]-5+module.width),(module.position[1]+origin_location[1]-5), (module.position[0]+origin_location[0]+5+module.width),(module.position[1]+origin_location[1]+5),fill="blue",outline="black",width=1)
    w.tag_raise(o1)
    w.tag_raise(o2)

img_background  = None
def update():
    global w, img_background
    w.after(10,update)

    w.delete("all")
    w.create_rectangle(0, 0, 700, 700, fill="black")
    w.create_image(350+origin_location[0]/3.0,0+origin_location[1]/3.0,image=img_background)
    for module in nodes:
        draw(module)

# Create windows

class Lmodule:
    name = "CNN module"
    position = (0,0)
    width = 40
    selected = False
    connection_to = set([])
    connection_from = set([])

    def __init__(self,loc,name,width):
        self.name = name
        self.position = (loc[0],loc[1])
        self.width = width
        self.connection_to = set([])
        self.connection_from = set([])
        self.selected = False

location = 0,0
myzoom = 1
import math
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


zoomer = False
mouse_pressed = False
slider = False

# Canvas window full of wonderful options for modules

current_module_item = None
def module_popup():
    global current_module_item
    win = Toplevel()

    w,h = 650,400
    popup_frame = Frame(win, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Create a customized window that contains information about a particular module.

# Layer module menu
module_menu = Menu(root, tearoff=0)
module_menu.add_command(label="Properties", command=module_popup)

def module_menu_event(e,m):
    global current_module_item
    current_module_item = m
    module_menu.post(e.x_root,e.y_root)

def canvas_click(e):
    # Select module that is most close to click
    global mouse_pressed, slider

    ee = visual_position(e.x,0),visual_position(e.y,1)
    mouse_pressed = True

    dist = []
    for m in (nodes):
        dist.append((distance(m.position,(ee[0],ee[1])),m))
        m.selected = False
    dist.sort()
    if dist[0][0] < 40:
        dist[0][1].selected = True
    else:
        slider = True

    pass#print e.x,e.y

origin_location = 350,350

def canvas_click_2(e):
    global location
    ee = visual_position(e.x,0),visual_position(e.y,1)
    dist = []
    for m in (nodes):
        dist.append((distance(m.position,(ee[0],ee[1])),m))
    dist.sort()
    if dist[0][0] < 40:
        dist[0][1].selected = True
        module_menu_event(e,dist[0][1])
        return
    #location = ee[0],ee[1]
    right_click_menu(e)

def canvas_motion(e):
    global mouse_pressed, zoomer, location, myzoom, origin_location

    ee = visual_position(e.x,0),visual_position(e.y,1)

    if mouse_pressed:
        for m in (nodes):
            if m.selected :
                m.position = ee
                m.position = (m.position[0]/25)*25,(m.position[1]/25)*25

    if slider == True:
        origin_location = origin_location[0]+(ee[0]-visual_position(location[0],0)), origin_location[1]+(ee[1]-visual_position(location[1],1))

    location = e.x,e.y

    pass#print e.x,e.y
def canvas_press(e):
    pass#print e.x,e.y
def canvas_release(e):
    global mouse_pressed, slider
    mouse_pressed = False
    slider = False
    pass#print e.x,e.y

def zoom(e):
    ee = visual_position(e.x,0),visual_position(e.y,1)
    dist = []
    connect = False
    current_node = None
    for m in nodes:
        if m.selected:
            connect = True
            current_node = m
        dist.append((distance(m.position,(ee[0],ee[1])),m))
    dist.sort()
    if dist[0][0] < 40:
        if not dist[0][1].selected and connect:
            dist[0][1].connection_from.add(current_node)
            current_node.connection_to.add(dist[0][1])
        elif dist[0][1].selected:
            for m in dist[0][1].connection_to:
                m.connection_from.remove(dist[0][1])
            for m in dist[0][1].connection_from:
                m.connection_to.remove(dist[0][1])

            dist[0][1].connection_to = set([])
            dist[0][1].connection_from = set([])

def zoom_stop(e):
    pass

def create_cnn():

    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"CNN",40)
    nodes.append(m)


def create_max_pooling():

    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"Mp",20)
    nodes.append(m)

def create_relu():

    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"Rlu",20)
    nodes.append(m)


def create_fully_connected():

    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"FC",20)
    nodes.append(m)

def create_variational_autoencoder():

    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"VA",50)
    nodes.append(m)

def create_custom():
    m = Lmodule((visual_position(location[0],0),visual_position(location[1],1)),"CU",50)
    nodes.append(m)


m = Lmodule((visual_position(100,0),visual_position(350,1)),"Input",40)
nodes.append(m)
m = Lmodule((visual_position(600,0),visual_position(350,1)),"Output",40)
nodes.append(m)


# Canvas menu
menu = Menu(root, tearoff=0)
menu.add_command(label="CNN layer", command=create_cnn)
menu.add_command(label="Max Pooling layer", command=create_max_pooling)
menu.add_command(label="Relu layer", command=create_relu)
menu.add_command(label="Fully Connected layer", command=create_fully_connected)
menu.add_command(label="Variational Autoencoder", command=create_variational_autoencoder)
menu.add_command(label="Custom layer", command=create_custom)

def right_click_menu(e):
    menu.post(e.x_root,e.y_root)


global_frame = Frame(root,width=w,height=h,relief=SUNKEN,borderwidth=4) # bg="black",
global_frame.grid(column=0,row=0)
global_frame.grid_propagate(False)
global_frame.grid_columnconfigure(0, weight=1)
global_frame.grid_rowconfigure(0, weight=1)

frame_canvas = Frame(global_frame,width=300, height=800,  colormap="new", relief=SUNKEN ,borderwidth =4)
frame_canvas.grid(column=0,row=0)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_rowconfigure(0, weight=1)

w = Canvas(frame_canvas, width=700, height=700)
img_background = PhotoImage(file="./deep_learning.gif")
img_background = img_background.subsample(1,1)
w.grid(column=0,row=0,columnspan=1,padx=10,pady=10)
w.create_rectangle(0, 0, 700, 700, fill="black")
w.bind('<Motion>', canvas_motion)
w.bind('<ButtonPress-1>', canvas_press)
w.bind('<Button-1>', canvas_click)
w.bind('<ButtonRelease-1>', canvas_release)
w.bind('<Button-3>', canvas_click_2)
w.bind('<ButtonPress-2>', zoom)
w.bind('<ButtonRelease-2>', zoom_stop)
w.after(100,update)


right_frame = Frame(global_frame,width=270, height=h-27,  colormap="new", relief=RIDGE ,borderwidth =4)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid(pady=10,padx=10,column=1,row=0)
right_frame.grid_propagate(False)

button_frame_panel = Frame(right_frame, width=270, height=h - 27, colormap="new", relief=FLAT, borderwidth=4)
button_frame_panel.grid_rowconfigure(0, weight=1)
button_frame_panel.grid_columnconfigure(0, weight=1)
button_frame_panel.grid(pady=10, padx=10, column=0, row=0, sticky=N)
button_frame_panel.grid_propagate(False)

dataset_frame = Frame(right_frame, width=270, height=h - 27, colormap="new", relief=FLAT, borderwidth=4)
dataset_frame.grid_columnconfigure(0, weight=1)
dataset_frame.grid(pady=10, padx=10, column=0, row=0, sticky=N)



n = ttk.Notebook(button_frame_panel)
n.add(dataset_frame,text="Utilities")
n.grid(column=0,row=0,padx=10,columnspan=1,pady=0,sticky=W+E+N+S)

index = 0
l0 = Label(dataset_frame, text=" ",  width=20, height = 1)
l0.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l0.grid_propagate(False)
index+= 1

l = Label(dataset_frame, text="Dataset folder",  width=20, height = 1)
l.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l.grid_propagate(False)
index+= 1


en = Entry(dataset_frame)
en.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
en.grid_propagate(False)
index+= 1

l_separation = Label(dataset_frame, text="Coding Tools",  width=20, height = 1)
l_separation.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=10,sticky=W+E+N+S)
l_separation.grid_propagate(False)
index+= 1

# Xml Reader part
event_set_model = ["Other"]
code_part_model = [("",[800,600],0) for i in range(len(event_set_model))]
code_part_model[0] =  "\n# Miscellaneous code goes here",[800,600],0

# Xml getter
code_text_widget_model = [None for i in range(len(code_part_model))]
model_reader = [code_part_model[i][0] for i in range(len(code_part_model))]

def reader(e,index):
    global code_text_getter, model_reader,code_text_widget_model
    model_reader[index] = code_text_widget_model[index].get("1.0",END)

def network_model_popup(index):
    global model_reader, code_text_Getter
    toplevel = Toplevel()
    w,h = 650,400
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    code_text_widget_model[index] = Text(toplevel,width=w)
    code_text_widget_model[index].grid(column=0,row=0)
    code_text_widget_model[index].insert(END,model_reader[index])
    code_text_widget_model[index].bind('<KeyRelease>', lambda event, i=index: reader(event,i))
    code_text_widget_model[index].focus_set()

def codeEvent(event):
    global dd_variable, event_set
    dd_variable.set("Code")
    index = event_set.index(event)
    xml_parser_popup(index)
    print event

dd_variable = StringVar(dataset_frame)
dd_variable.set("Code")
dd = OptionMenu(dataset_frame, dd_variable, *event_set,command = codeEvent)
dd.grid(column=0,row=index,padx=30,columnspan=2,pady=0,sticky=W+E+N+S)
dd.grid_propagate(False)
index+= 1

# Model panel  ######################################################################################################
#index = 0




# Evaluate panel ######################################################################################################
#index = 0


# Evaluator Part

# You need to define the train_op operator

event_set_eval = ["Train","Test","Other"]
code_part_eval = [("",[800,450],0) for i in range(len(event_set_eval))]
code_part_eval[0] = "\nwith tf.Session() as sess:"\
                    "\n    # you need to initialize all variables"\
                    "\n    init = tf.initialize_all_variables()"\
                    "\n    saver = tf.train.Saver()"\
                    "\n    sess.run(init)"\
                    "\n    batch_size = 32"\
                    "\n    input_shape = [28,28,1]"\
                    "\n    output_shape = [10]"\
                    "\n    for i in range(1000):"\
                    "\n        print i, '/',1000"\
                    "\n        training_batch = load_database.return_batch(batch_size=batch_size,mymode='training',input_shape = input_shape,output_shape = output_shape)"\
                    "\n        sess.run(train_op, feed_dict={X: training_batch[0], Y: training_batch[1]})" \
                    "\n    save_path = saver.save(sess, './models/<<MODEL_NAME>>'+str(i)+'.ckpt')",[1024,450],0


code_part_eval[2] =  "\n# Miscellaneous code goes here",[800,600],0

# Xml getter

l = Label(dataset_frame, text="Model name",  width=20, height =1)
l.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l.grid_propagate(False)
index+= 1

en_model = Entry(dataset_frame)
en_model.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
en_model.grid_propagate(False)
index+= 1

code_text_widget_eval = [None for i in range(len(code_part_eval))]
eval_reader = [code_part_eval[i][0] for i in range(len(code_part_eval))]

l_separation = Label(dataset_frame, text="Coding Tools",  width=20, height = 1)
l_separation.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=10,sticky=W+E+N+S)
l_separation.grid_propagate(False)
index+= 1


def eval_popup(index):
    toplevel = Toplevel()
    print code_part_eval[index][1][0]
    w,h = code_part_eval[index][1][0],code_part_eval[index][1][1]
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    code_text_widget_eval[index] = Text(toplevel,width=w)
    code_text_widget_eval[index].grid(column=0,row=0)
    code_text_widget_eval[index].insert(END,eval_reader[index])
    code_text_widget_eval[index].bind('<KeyRelease>', lambda event, i=index: reader(event,i))
    code_text_widget_eval[index].focus_set()

def codeEvent_eval(event):
    global dd3_variable, event_set_eval
    dd3_variable.set("Code")
    index = event_set_eval.index(event)
    eval_popup(index)
    print event

dd3_variable = StringVar(dataset_frame)
dd3_variable.set("Code")
dd3 = OptionMenu(dataset_frame, dd3_variable, *event_set_eval,command = codeEvent_eval)
dd3.grid(column=0,row=index,padx=30,columnspan=2,pady=0,sticky=W+E+N+S)
dd3.grid_propagate(False)
index+= 1

def save():
    global nodes

    pickle.dump( nodes, open( "nodes.p", "wb" ) )
    pass

def load():
    global nodes
    nodes = pickle.load( open( "nodes.p", "rb" ) )
    pass



b2 = Button(dataset_frame, text="Save", command=save, width=7, height = 1)
b2.grid(column=0,row=index,padx=30,columnspan=2,pady=5,sticky=W+S)
b2.grid_propagate(False)
b2 = Button(dataset_frame, text="Load", command=load, width=7, height = 1)
b2.grid(column=1,row=index,padx=30,columnspan=2,pady=5,sticky=E+S)
b2.grid_propagate(False)
index+= 1

b2 = Button(dataset_frame, text="Compile to python", command=compile_python, width=20, height = 1)
b2.grid(column=0,row=index,padx=30,columnspan=2,pady=5,sticky=S)
b2.grid_propagate(False)
index+= 1
root.mainloop() # starts the mainloop