#!/usr/bin/env python3

import sys
import os
import tkinter

"""
Window class
Manages tkinter GUI elements
"""
class Window:
    def __init__(self, windowTitle):
        self.rootWin = tkinter.Tk()
        self.rootWin.title(windowTitle)
        self.root = self.rootWin
        self.roots = []
        self.elements = {}
        self.gridX = 0
        self.gridY = 0
        self.background = None

    def __setRoot(self, newroot):
        oldroot = [self.root, self.gridX, self.gridY]
        self.roots.append(oldroot)
        self.root = newroot
        self.gridX = 0
        self.gridY = 0

    def __restoreRoot(self):
        oldroot = self.roots.pop()
        self.root = oldroot[0]
        self.gridX = oldroot[1]
        self.gridY = oldroot[2]

    def movePos(self, x, y):
        self.gridX += x
        self.gridY += y

    def setPos(self, x, y):
        self.gridX = x
        self.gridY = y

    def nextPos(self, move):
        if move == 0:
            self.gridY += 1
            self.gridX = 0
        elif move == 1:
            self.gridX += 1

    def setIcon(self, icon):
        self.rootWin.iconbitmap(icon)

    def setResizable(self, x, y):
        self.rootWin.resizable(x, y)
            
    def setMainWindow(self, state):
        if state == True:
            self.rootWin.protocol("WM_DELETE_WINDOW", sys.exit)

    def rowWeight(self, row, weight):
        self.root.rowconfigure(row, weight=weight)

    def columnWeight(self, column, weight):
        self.root.columnconfigure(column, weight=weight)

    def setBackgroundColour(self, colour):
        self.background = colour
        self.root.configure(background=colour)
        for e in self.elements.values():
            e.configure(background=colour)

    def maximise(self):
        try:
            self.rootWin.winfo_toplevel().wm_state("zoomed")
        except:
            w = self.rootWin.winfo_screenwidth()
            h = self.rootWin.winfo_screenheight()
            geom_string = "%dx%d+0+0" % (w,h)
            self.rootWin.winfo_toplevel().wm_geometry(geom_string)

    def startFrame(self, name, type=0, thickness=1, colour="black", move=0, padx=0, pady=0, ipadx=0, ipady=0, sticky=tkinter.W+tkinter.E):
        if type == 0:
            self.elements["frame_"+name] = tkinter.Frame(self.root, highlightbackground=colour, highlightthickness=thickness)
        elif type == 1:
            self.elements["frame_"+name] = tkinter.Frame(self.root, borderwidth=thickness, relief=tkinter.RAISED)
        self.elements["frame_"+name].grid_columnconfigure(0, weight=1)
        self.elements["frame_"+name].grid(row=self.gridY, column=self.gridX, sticky=sticky, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        if self.background is not None:
            self.elements["frame_"+name].configure(background=self.background)
        self.nextPos(move)
        self.__setRoot(self.elements["frame_"+name])

    def setFrameSize(self, name, width, height):
        self.elements["frame_"+name].configure(width=width, height=height)
        self.elements["frame_"+name].grid_propagate(False)

    def endFrame(self):
        self.__restoreRoot()

    def setFrame(self, name):
        self.__setRoot(self.elements["frame_"+name])

    def deleteFrame(self, name):
        if "frame_"+name in self.elements:
            self.elements["frame_"+name].grid_forget()
            self.elements["frame_"+name].destroy()
            del self.elements["frame_"+name]

    def addLabel(self, name, text, move=0, padx=0, pady=0, ipadx=0, ipady=0, font=None, anchor=tkinter.CENTER, justify=tkinter.CENTER, sticky=tkinter.W+tkinter.E):
        self.elements["label_"+name] = tkinter.Label(self.root, text=text, font=font, anchor=anchor, justify=justify)
        self.elements["label_"+name].grid(row=self.gridY, column=self.gridX, sticky=sticky, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        if self.background is not None:
            self.elements["label_"+name].configure(background=self.background)
        self.nextPos(move)

    def editLabel(self, name, text):
        self.elements["label_"+name].config(text=text)

    def addButton(self, name, text, action, move=0, padx=0, pady=0, ipadx=0, ipady=0, font=None, state=tkinter.NORMAL, anchor=tkinter.CENTER, justify=tkinter.CENTER, sticky=tkinter.W+tkinter.E):
        self.elements["button_"+name] = tkinter.Button(self.root, text=text, font=font, command=action, state=state, anchor=anchor, justify=justify)
        self.elements["button_"+name].grid(row=self.gridY, column=self.gridX, sticky=sticky, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        if self.background is not None:
            self.elements["button_"+name].configure(background=self.background)
        self.nextPos(move)

    def editButton(self, name, text, action):
        self.elements["button_"+name].config(text=text, command=action)

    def setButton(self, name, state):
        if "button_"+name in self.elements:
            self.elements["button_"+name].config(state=state)

    def deleteButton(self, name):
        if "button_"+name in self.elements:
            self.elements["button_"+name].grid_forget()
            self.elements["button_"+name].destroy()
            del self.elements["button_"+name]

    def addEntry(self, name, move=0, width=10, padx=0, pady=0, ipadx=0, ipady=0, font=None, sticky=tkinter.W+tkinter.E):
        self.elements["entry_"+name] = tkinter.Entry(self.root, font=font, width=width)
        self.elements["entry_"+name].grid(row=self.gridY, column=self.gridX, sticky=sticky, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        if self.background is not None:
            self.elements["entry_"+name].configure(background=self.background)
        self.nextPos(move)

    def getEntryValue(self, name):
        if "entry_"+name in self.elements:
            return self.elements["entry_"+name].get()

    def addTimer(self, time, action):
        return self.rootWin.after(time, action)

    def delTimer(self, timer):
        self.rootWin.after_cancel(timer)

    def mainloop(self):
        self.rootWin.mainloop()

    def update(self):
        self.rootWin.update()

    def update_idletasks(self):
        self.rootWin.update_idletasks()

    def close(self):
        self.rootWin.destroy()

    def addScrollbar(self, name):
        canvas = tkinter.Canvas(self.root)
        scrollbar = tkinter.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        frame = tkinter.Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas : canvas.configure(scrollregion=canvas.bbox("all")))

        self.elements["canvas_"+name] = canvas
        self.elements["scrollbar_"+name] = scrollbar
        self.elements["scrollbar_frame_"+name] = frame

        self.__setRoot(frame)


def error_dialog(message):
    dialog = Window("Error")
    dialog.addLabel("error_message", message)
    dialog.addButton("ok_button", "OK", sys.exit)
    dialog.mainloop()

def file_label(index, name):
    return "["+str(index)+"] "+os.path.basename(name)

def move(item, direction):
    index = files.index(item)
    other_index = index + direction

    if other_index < 0 or other_index >= len(files):
        return

    item_name = files[index]
    other_item_name = files[other_index]

    item = win.elements["frame_file_"+item_name]
    other_item = win.elements["frame_file_"+other_item_name]

    item.grid(row = other_index)
    win.editLabel("file_label_"+item_name, file_label(other_index, item_name))
    other_item.grid(row = index)
    win.editLabel("file_label_"+other_item_name, file_label(index, other_item_name))

    files[index] = other_item_name
    files[other_index] = item_name

def confirm_rename():
    def confirm_cancel():
        confirm.close()

    def confirm_ok():
        try:
            start = int(confirm.getEntryValue("start_number"))
        except:
            start = None

        if isinstance(start, int):
            do_rename(start, confirm.getEntryValue("prefix"), confirm.getEntryValue("suffix"))
            sys.exit()

    confirm = Window("Confirm Rename?")
    confirm.setResizable(False, False)
    confirm.addLabel("prefix", "Prefix:", 1)
    confirm.addEntry("prefix")
    confirm.addLabel("suffix", "Suffix:", 1)
    confirm.addEntry("suffix")
    confirm.addLabel("start_number", "Start at number:", 1)
    confirm.addEntry("start_number")
    confirm.addButton("rename_ok", "OK", confirm_ok, 1, ipadx=45)
    confirm.addButton("rename_cancel", "CANCEL", confirm_cancel, ipadx=30)
    confirm.mainloop()

def do_rename(start=0, prefix="", suffix=""):
    renames = {}
    secondary_renames = {}
    for item in files:
        # Check if source file exists
        if not os.path.exists(item):
            error_dialog("File "+item+" does not exist")

        path = os.path.dirname(item)
        parts = os.path.basename(item).split(".")
        dest = os.path.join(path, prefix+str(start)+suffix+"."+parts[len(parts)-1])

        # Check if a file with the destination filename already exists
        if os.path.exists(dest):
            if dest in files:
                tmp_dest = dest+'.file_numberer'
                if os.path.exists(tmp_dest):
                    error_dialog("File "+tmp_dest+" already exists")

                secondary_renames[tmp_dest] = dest
                dest = tmp_dest
            else:
                error_dialog("File "+dest+" already exists")

        renames[item] = dest
        start += 1

    rename_files(renames.items())
    rename_files(secondary_renames.items())

def rename_files(items):
    for src, dst in items:
        print(src+" -> "+dst)

        try:
            os.rename(src, dst)
        except:
            error_dialog("Cannot rename "+src+" to "+dst)

files = sys.argv[1:]

if len(files) == 0:
    error_dialog("No input files")

win = Window("File Numberer")
win.setMainWindow(True)
win.setResizable(False, True)
win.addScrollbar("scrollbar")

for index, item in enumerate(files):
    win.startFrame("file_"+item)
    win.addLabel("file_label_"+item, file_label(index, item), 1, padx=100, pady=10)
    win.startFrame("file_buttons_"+item)
    win.addButton("up_"+item, "↑", lambda item=item: move(item, -1))
    win.addButton("down_"+item, "↓", lambda item=item: move(item, 1))
    win.endFrame()
    win.endFrame()

win.addButton("rename", "RENAME", confirm_rename, pady=20)

win.mainloop()

