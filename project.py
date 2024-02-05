import tkinter as tk
import os
from subprocess import run
from shutil import rmtree
import tksvg


gui = tk.Tk()
gui.title("File Manager")
dirbox = tk.Entry(gui)
currentDirButtons = []
sb = tk.Scrollbar(gui)
sb.grid(row=2, column=1,  sticky='e')
lsbox = tk.Listbox(gui,height=10,width=20, yscrollcommand = sb.set)
lsbox.grid(row=2,column=1,padx=20,pady=20)
TrashIcon = tksvg.SvgImage(file = "assets/trash.svg")
text = tk.Label(text="File Manager")
indir = "/"







def getPrevDir(Dir):
  character = list(Dir)
  pos = len(character) -1
  done = False
  
  while not done:
    if character[pos] == "/":
      pos
      done = True
    else:
      pos -= 1
  newDir = ""
  x = 0
  while x != pos:
    newDir += character[x]
    x+=1
  return newDir
  
def filesInDir(dir:str):
  files = []
  try:
    scan = os.scandir(dir)
  except:
    lsbox.delete(0,tk.END)
    lsbox.insert(0,"No Such Directory")
    return
  for i in scan:
    files.append(i.name)
  return files

def openDir(dir):

  if not os.path.isdir(dir):
    global indir
    try:
      run(dir)
      return
    except:
      lsbox.delete(0,tk.END)
      lsbox.insert(0,"Cannot Open File")
  lsbox.delete(0,tk.END)
  text=dir
  files = filesInDir(text)
  if files == None:
    return
  x = 2
  for i in files:
    bt = tk.Button(gui,text=i,anchor=tk.CENTER)
    lsbox.insert(tk.END, i)
    currentDirButtons.append(bt)
    x += 1
  sb.config( command = lsbox.yview )
  indir = dirbox.get()
  

previousClick = ""
def onClick(event):
  global previousClick
  selection = event.widget.curselection()
  if selection:
    index = selection[0]
    data = event.widget.get(index)
    if previousClick == data:
      chardir = list(indir)
      if chardir[len(chardir)-1] == "/":
        newDir = indir + data
      else:
        newDir =indir + "/" + data
      openDir(newDir)
      previousClick = ""
      dirbox.delete(0, tk.END)
      dirbox.insert(0, newDir)
    else:
      previousClick = data





lsbox.bind("<<ListboxSelect>>", onClick)

def confirm(event):
  openDir(indir)

gui.bind('<Return>', confirm)



enterButton = tk.Button(gui,text="Enter",command=lambda: openDir(indir) ,anchor=tk.N)

def upDir(dir):
  newDir = getPrevDir(indir)
  dirbox.delete(0,tk.END)
  dirbox.insert(0,newDir)
  openDir(newDir)

def delMode():
  selected = lsbox.get(tk.ACTIVE)
  dir = list(indir)
  if dir[len(dir) -1 == "/"]:
    rmdir = indir + selected
  else:

    rmdir = indir + "/" + selected
  if os.path.isdir(rmdir):

    rmtree(dir + "/" + selected)
    openDir(dir)
  else:
    os.remove(rmdir)



upButton = tk.Button(gui,text="^", command=lambda: upDir(indir))
delButton = tk.Button(gui, text="D", command=delMode, image=TrashIcon)
text.grid(column=1,row=1) 



dirbox.grid(column=1,row=0)
enterButton.grid(column=2,row=0)
upButton.grid(column=3,row=0)
delButton.grid(column=4,row=0)


gui.geometry("250x250")
dirbox.delete(0,tk.END)
dirbox.insert(0,"/")
openDir("/")



gui.mainloop()