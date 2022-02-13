import tkinter, tkinter.colorchooser, numpy, amulet_nbt#, threading
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image, ImageTk

#// &0xFF is because the array uses unsigned bytes while java uses signed ones. it converts values like -127 back to values like 129
#short blockid = (short)(blocks[blocknumber] & 0xFF);

class Example():
	def __init__(self):
		self.root = tkinter.Tk()
		#Frame.pack(fill="both", expand=True)
		menubar = tkinter.Menu(self.root)#binds the menubar the the root
		menubar.add_command(label="Open file", command=self.fileopen)
		filemenu = tkinter.Menu(menubar, tearoff=0)
		filemenu.add_command(label="background color", command=self.bgcolorDef)
		filemenu.add_command(label="grid color", command=self.GridColorDef)
		filemenu.add_command(label="bold grid color", command=self.BGridColorDef)
		menubar.add_cascade(label="colors", menu=filemenu)
		self.root.config(menu=menubar)
		self.BGColor = "silver"
		self.GridColor = "black"
		self.BGridColor = "black"
		self.myXBGrid = []
		self.myYBGrid = []
		self.myGrid = []
		self.imagedict = {}
		#self.makecanvas()
		#self.fileopen()
		self.root.bind('<Up>', lambda e:self.somthing('Up'))
		self.root.bind('<Down>', lambda e:self.somthing('Down'))
		self.label = Label(self.root, text="Block Name")
		self.label.grid(sticky='SW', column=0, row=2)
		self.root.mainloop()
	def somthing(self, event):
		if event == 'Up':self.scale1.set(self.scale1.get() + 1)
		if event == 'Down':self.scale1.set(self.scale1.get() - 1)
	#def start_thread(self):
	#	self.thread = threading.Thread(target=self.makecanvas)
	#	self.thread.start()
	#	self.root.after(20, self.check_thread)

	#def check_thread(self):
	#	if self.thread.is_alive():
	#		self.root.after(20, self.check_thread)
	def ColorPicker(self):
		return tkinter.colorchooser.askcolor(title='Pick a color')[1]
	def bgcolorDef(self):
		self.BGColor = self.ColorPicker()
		self.canvas.configure(bg=self.BGColor)
	def GridColorDef(self):
		self.GridColor = self.ColorPicker()
		for i in self.myGrid:
			self.canvas.itemconfig(i, outline=self.GridColor)
	def BGridColorDef(self):
		self.BGridColor = self.ColorPicker()
		for i in self.myXBGrid:
			self.canvas.itemconfig(i, fill=self.BGridColor)
		for i in self.myYBGrid:
			self.canvas.itemconfig(i, fill=self.BGridColor)
	def makecanvas(self):
		self.canvas = tkinter.Canvas(self.root, width=400, height=400, background=self.BGColor)
		self.xsb = tkinter.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
		self.ysb = tkinter.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
		self.canvas.configure(scrollregion=(0,0,1000,1000))

		self.xsb.grid(row=1, column=0, sticky="ew")
		self.ysb.grid(row=0, column=1, sticky="ns")
		self.canvas.grid(row=0, column=0, sticky="nsew")
		#self.root.update()
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.pixel_width = 20
		self.pixel_height = 20
		self.canvas.bind('<Configure>', lambda e: self.updateGrid)
		self.canvas.bind('<Motion>', self.motion)
		self.createGrid()

		#self.canvas.create_text(50,10, anchor="nw", text="Click and drag to move the canvas\nScroll to zoom.")

		# This is what enables using the mouse:
		self.canvas.bind('<ButtonPress-1>', self.move_start)
		self.canvas.bind('<B1-Motion>', self.move_move)
		#windows scroll
		self.canvas.bind('<MouseWheel>',self.zoom)
	def shape(self):
		return int(self.sf['Height']), int(self.sf['Length']), int(self.sf['Width'])
	def fileopen(self):
		self.filename = filedialog.askopenfilename().split("/")[-1]
		#load schematic
		self.sf = amulet_nbt.load(self.filename)
		c = list(self.sf['Data'])
		d = list(self.sf['Blocks'])
		list3 = []
		for x in range(len(d)):
			if d[x] > 0 or d[x] == 0:thing = d[x]
			else:thing = d[x] + 256
			if c[x] != 0:list3.append(f"{thing}:{c[x]}")
			else:list3.append(thing)

		self.b = numpy.reshape(list3, self.shape())
		#print(self.b)
		self.scale1 = tkinter.Scale(self.root, from_=len(self.b)-1, to=0, length=400, command=self.updateGrid)
		self.scale1.grid(column=2, row=0)
	#	print(self.filename)
		self.makecanvas()

	def motion(self, event=None):
		#x, y = event.x, event.y
		try:
			temp = self.canvas.find_withtag("current")
			color = self.canvas.itemcget(temp, "fill")
			if color != '':
				if color == self.BGColor:color = 'Air'
				self.label.configure(text=color)
		except:pass

	def updateGrid(self, event=None):
		try:
			layer = self.scale1.get()
			for i, e in zip(self.myGrid, [y for x in self.b[layer] for y in x]):
				self.recolor(i)
				self.BlockColor(e, i)
		except:pass
	def recolor(self, thing):
		self.canvas.itemconfig(thing, fill=self.BGColor)
	def createGrid(self, event=None):
		#self.scale1.config(length=sh)
		self.canvas.delete("all")
		#Plot some rectangles
		GridLinesListX = []
		GridLinesListY = []
		try:
			c = self.b[0]
			for x in range(len(c)):
				d = c[x]
				for y in range(len(d)):
					x1 = (x * self.pixel_width)
					x2 = (x1 + self.pixel_width)
					y1 = (y * self.pixel_height)
					y2 = (y1 + self.pixel_height)
					e = d[y]
					#print(e)
					Grid = self.canvas.create_rectangle(y1,x1,y2,x2, outline=self.GridColor)
					self.myGrid.append(Grid)
					GridLinesListX.append(x1)
					GridLinesListY.append(y1)
					self.BlockColor(e, Grid)
			#print(GridLinesListX)
			#print(GridLinesListY)
			self.GridLines(GridLinesListX, GridLinesListY)
		except Exception as e:print('e1', e)
		#self.canvas.update()
	def rgb2hex(self, thing):
		try:
			what = '#%02x%02x%02x' % thing
		except:
			r = int(str(thing).replace('(', '').replace(')', '').split(',')[0])
			g = int(str(thing).replace('(', '').replace(')', '').split(',')[1])
			b = int(str(thing).replace('(', '').replace(')', '').split(',')[2])
			what = '#%02x%02x%02x' % (r, g, b)
		return what
	def GetMainColor(self, file):
		img = Image.open(file)
		colors = img.getcolors(256) #put a higher value if there are many colors in your image
		max_occurence, most_present = 0, 0
		colordict = {}
		try:
			for c in colors:
				if c[0] > max_occurence:
					max_occurence, most_present = c
					colordict[max_occurence] = most_present
			clr = list(colordict.keys())
			try:
				if colordict[clr[-1]].count(0) != 4:
					return self.rgb2hex(colordict[clr[-1]])
				else:
					return self.rgb2hex(colordict[clr[-2]])
			except Exception as e:print('e2', e)
		except TypeError:
			raise Exception("Too many colors in the image")
	def BlockColor(self, block, GridSquare):
		#if block == 0:color = self.backgroundcolor
		#else:color = blockIDs['ids'][block]['color']
		color = self.BGColor
		if block != '0':
			try:pilImage = self.imagedict[block]
			except Exception as e:
				name = block.replace(':', '-')
				try:pilImage = self.GetMainColor("textures/{}.png".format(name))
				except Exception as e:print(e)
				self.imagedict[block] = pilImage
			color = self.imagedict[block]
		if block:
			#print(color)
			self.canvas.itemconfig(GridSquare, fill=color, activefill=color)
	def GridLines(self, x1, y1):
		try:
			print('x1', x1[-1])
			print('y1', y1[-1])
			for i in range(100, x1[-1], 100):
				if x1[i] == i:self.myXBGrid.append(self.canvas.create_line((i, x1[i]+20, i, 0), fill=self.BGridColor, width=2))
			for i in range(100, y1[-1], 100):
				if y1[i] == i:self.myYBGrid.append(self.canvas.create_line((0, i, y1[i]+20, i), fill=self.BGridColor, width=2))
		except Exception as e:print('e3', e)
	#move
	def move_start(self, event):
		self.canvas.scan_mark(event.x, event.y)
	def move_move(self, event):
		self.canvas.scan_dragto(event.x, event.y, gain=1)

	#windows zoom
	def zoom(self,event):
		if (event.delta > 0):
			self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
		elif (event.delta < 0):
			self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
		self.canvas.configure(scrollregion = self.canvas.bbox("all"))
if __name__ == "__main__":
	Example()