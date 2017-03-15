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

def compile_python():
    global en
    myfile = open("load_database.txt","r")
    load_database_txt = myfile.read()
    load_database_txt = load_database_txt.replace("<<Other>>", xml_reader_other)
    load_database_txt = load_database_txt.replace("<<Replace_xml_parser>>", xml_reader)

    myfile = open("network.txt","r")
    network_txt = myfile.read()
    network_txt = network_txt.replace("<<InputOutput>>", xml_reader_io) # Needs to happen before imsize
    load_database_txt = load_database_txt.replace("<<ReadDatafromannotations>>", xml_reader_data) # Needs to happen before imsize
    if en.get() == "":
        if target_directory == None:
            return
        network_txt = network_txt.replace("<<TrainingFileFolder>>", target_directory)
    else:
        network_txt = network_txt.replace("<<TrainingFileFolder>>", en.get())
    if en2.get() == "":
        if target_directory_testing == None:
            return
        network_txt = network_txt.replace("<<TestingFileFolder>>", target_directory_testing)
    else:
        network_txt = network_txt.replace("<<TestingFileFolder>>", en2.get())
    network_txt = network_txt.replace("<<batch_size>>", str(en_batch.get()))
    network_txt = network_txt.replace("<<max_iterations>>", str(en_iter.get()))
    network_txt = network_txt.replace("<<model_name>>", "'"+str(en_model.get())+"'")
    network_txt = network_txt.replace("<<imsize>>", str(en_size.get()))
    network_txt = network_txt.replace("<<imsize2>>", str(en_size2.get()))
    load_database_txt = load_database_txt.replace("<<imsize>>", str(en_size.get()))
    load_database_txt = load_database_txt.replace("<<imsize2>>", str(en_size2.get()))

    text_file = open("load_database.py", "w")
    text_file.write("%s" % load_database_txt)
    text_file.close()

    text_file = open("network.py", "w")
    text_file.write("%s" % network_txt)
    text_file.close()


def target_folder():
    global target_directory
    target_directory = fd.askdirectory()+str("/")

def target_folder2():
    global target_directory_testing
    target_directory_testing = fd.askdirectory()+str("/")


# Xml Reader part
xml_reader = "def read_annotations(image_file):\n# Given the path of an image file, create the category" \
             "\n# label and give the maximum number of categories" \
             "\n    transformed_xml_path = os.path.splitext('image_file')[0]+str('.xml')" \
             "\n    e = xml.etree.ElementTree.parse(transformed_xml_path).getroot()"\
             "\n    '''if this annotation should be skipped, set skip to True'''\n    skip = False"\
             "\n    return 2,10,skip"

xml_reader_io = "X = tf.placeholder('float', [None, <<imsize>>, <<imsize2>>, 3])\n"\
                "Y = tf.placeholder('float', [None, max_categories])"
xml_reader_data = "category, max_categories, skip = read_annotations(image_list[shuffled_index])\n"\
                        "if skip:\n"\
                        "    continue\n"\
                        "I[datums,:,:,:] = np.asarray(misc.imresize(Image.open(image_list[shuffled_index]),[<<imsize>>,<<imsize2>>,3]))\n"\
                        "y[datums,:] = one_hot(category,max_categories)"
xml_reader_other = ""
xml_reader_other2 = ""

text_xml = None
text_xml_io = None
text_xml_data = None
text_xml_other = None
text_xml_other2 = None

def reader(e):
    global text_xml, xml_reader
    xml_reader = text_xml.get("1.0",END)

def reader_io(e):
    global text_xml_io, xml_reader_io
    xml_reader_io = text_xml_io.get("1.0",END)

def reader_data(e):
    global text_xml_data, xml_reader_data
    xml_reader_data = text_xml_data.get("1.0",END)

def reader_other(e):
    global text_xml_other, xml_reader_other
    xml_reader_other = text_xml_other.get("1.0",END)
def reader_other2(e):
    global text_xml_other2, xml_reader_other2
    xml_reader_other2 = text_xml_other2.get("1.0",END)


def xml_parser_popup_io():
    global io_reader, text_xml_io
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

    text_xml_io = Text(toplevel,width=w)
    text_xml_io.grid(column=0,row=0)
    text_xml_io.insert(END,xml_reader_io)
    text_xml_io.bind('<KeyRelease>', reader_io)
    text_xml_io.focus_set()

def xml_parser_popup():
    global xml_reader, text_xml
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

    text_xml = Text(toplevel,width=w)
    text_xml.grid(column=0,row=0)
    text_xml.insert(END,xml_reader)
    text_xml.bind('<KeyRelease>', reader)
    text_xml.focus_set()

def xml_parser_popup_data():
    global xml_reader_data, text_xml_data
    toplevel = Toplevel()
    w,h = 1024,400
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    text_xml_data = Text(toplevel,width=w)
    text_xml_data.grid(column=0,row=0)
    text_xml_data.insert(END,xml_reader_data)
    text_xml_data.bind('<KeyRelease>', reader_data)
    text_xml_data.focus_set()


def xml_parser_popup_other():
    global xml_reader_other, text_xml_other
    toplevel = Toplevel()
    w,h = 800,400
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    text_xml_other = Text(toplevel,width=w)
    text_xml_other.grid(column=0,row=0)
    text_xml_other.insert(END,xml_reader_other)
    text_xml_other.bind('<KeyRelease>', reader_other)
    text_xml_other.focus_set()

def xml_parser_popup_other2():
    global xml_reader_other2, text_xml_other2
    toplevel = Toplevel()
    w,h = 800,400
    popup_frame = Frame(toplevel, width=w, height=h, bg="grey", colormap="new", relief=FLAT, borderwidth=4)
    popup_frame.grid()
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))

    text_xml_other2 = Text(toplevel,width=w)
    text_xml_other2.grid(column=0,row=0)
    text_xml_other2.insert(END,xml_reader_other2)
    text_xml_other2.bind('<KeyRelease>', reader_other2)
    text_xml_other2.focus_set()

# Create windows
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
w.grid(column=0,row=0,columnspan=1,padx=10,pady=10)
w.create_rectangle(0, 0, 700, 700, fill="black")

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

model_frame = Frame(right_frame, width=270, height=h - 27, colormap="new", relief=FLAT, borderwidth=4)
model_frame.grid_rowconfigure(0, weight=1)
model_frame.grid_columnconfigure(0, weight=1)
model_frame.grid(pady=10, padx=10, column=0, row=0, sticky=N)

network_frame = Frame(right_frame, width=270, height=h - 27, colormap="new", relief=FLAT, borderwidth=4)
network_frame.grid_rowconfigure(0, weight=1)
network_frame.grid_columnconfigure(0, weight=1)
network_frame.grid(pady=10, padx=10, column=0, row=0, sticky=N)

n = ttk.Notebook(button_frame_panel)
n.add(dataset_frame,text="Dataset")
n.add(model_frame,text="Model")
n.add(network_frame,text="Network")
n.grid(column=0,row=0,padx=10,columnspan=1,pady=0,sticky=W+E+N+S)

index = 0
l0 = Label(dataset_frame, text=" ",  width=20, height = 1)
l0.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l0.grid_propagate(False)
index+= 1

l = Label(dataset_frame, text="Training folder",  width=20, height = 1)
l.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l.grid_propagate(False)
index+= 1

b = Button(dataset_frame, text="Set target folder", command=target_folder, width=20, height = 1)
b.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
b.grid_propagate(False)
index+= 1

en = Entry(dataset_frame)
en.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
en.grid_propagate(False)
index+= 1

l = Label(dataset_frame, text="Testing folder",  width=20, height = 1)
l.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l.grid_propagate(False)
index+= 1

b2 = Button(dataset_frame, text="Set target folder", command=target_folder2, width=20, height = 1)
b2.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
b2.grid_propagate(False)
index+= 1

en2 = Entry(dataset_frame)
en2.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
en2.grid_propagate(False)
index+= 1


l_batch = Label(dataset_frame, text="Batch Size",  width=10, height = 1)
l_batch.grid(column=0,row=index,columnspan=1,rowspan=1,padx=1,pady=1,sticky=E+W)
l_batch.grid_propagate(False)

l_batch = Label(dataset_frame, text="Iterations",  width=10, height = 1)
l_batch.grid(column=1,row=index,columnspan=1,rowspan=1,padx=1,pady=1,sticky=E+W)
l_batch.grid_propagate(False)
index+=1

en_batch = Entry(dataset_frame,width=5)
en_batch.grid(column=0,row=index,columnspan=1,rowspan=1,padx=30,pady=1,sticky=W)
en_batch.grid_propagate(False)

en_iter = Entry(dataset_frame,width=5)
en_iter.grid(column=1,row=index,columnspan=1,rowspan=1,padx=30,pady=1,sticky=E)
en_iter.grid_propagate(False)
index+= 1

l_model = Label(dataset_frame, text="Model Name",  width=20, height = 1)
l_model.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l_model.grid_propagate(False)
index+= 1

en_model = Entry(dataset_frame)
en_model.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
en_model.grid_propagate(False)
index+= 1
l_model = Label(dataset_frame, text="Image Size (w x h)",  width=20, height = 1)
l_model.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=1,sticky=W+E+N+S)
l_model.grid_propagate(False)
index+= 1

en_size = Entry(dataset_frame,width=5)
en_size.grid(column=0,row=index,columnspan=1,rowspan=1,padx=30,pady=1,sticky=W)
en_size.grid_propagate(False)
en_size2 = Entry(dataset_frame,width=5)
en_size2.grid(column=1,row=index,columnspan=1,rowspan=1,padx=30,pady=1,sticky=E)
en_size2.grid_propagate(False)
index+= 1
l_separation = Label(dataset_frame, text="Coding Tools",  width=20, height = 1)
l_separation.grid(column=0,row=index,columnspan=2,rowspan=1,padx=30,pady=10,sticky=W+E+N+S)
l_separation.grid_propagate(False)
index+= 1


def codeEvent(event):
    global dd_variable
    dd_variable.set("Code manipulation")
    event_set = ["Xml Parser", "Input Output Variable Sizes", "Annotation to data","Other Code (Database)","Other Code (Network)"]
    print event

dd_variable = StringVar(dataset_frame)
dd_variable.set("Code manipulation")
dd = OptionMenu(dataset_frame, dd_variable, "Xml Parser", "Input Output Variable Sizes", "Annotation to data","Other Code (Database)","Other Code (Network)",command = codeEvent)
dd.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
dd.grid_propagate(False)
index+= 1

'''
b2 = Button(button_frame, text="Xml Parser", command=xml_parser_popup, width=20, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
b2.grid_propagate(False)
index+= 1
b2 = Button(button_frame, text="Input Output Variable Sizes", command=xml_parser_popup_io, width=20, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
b2.grid_propagate(False)
index+= 1
b2 = Button(button_frame, text="Annotation to data", command=xml_parser_popup_data, width=20, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
b2.grid_propagate(False)
index+= 1
b2 = Button(button_frame, text="Other Code (Database)", command=xml_parser_popup_other, width=20, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
b2.grid_propagate(False)
index+=1
b2 = Button(button_frame, text="Other Code (Network)", command=xml_parser_popup_other2, width=20, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=0,sticky=W+E+N+S)
b2.grid_propagate(False)
index+=1
'''
b2 = Button(dataset_frame, text="Compile to python", command=compile_python, width=17, height = 1)
b2.grid(column=0,row=index,padx=10,columnspan=2,pady=30,sticky=S)
b2.grid_propagate(False)
index+= 1
root.mainloop() # starts the mainloop