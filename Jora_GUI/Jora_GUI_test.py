import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import pandas as pd
import pickle
from PIL import Image, ImageTk
from pandastable import Table, TableModel
import matplotlib.pyplot as plt
import seaborn as sns

# Instantiate GUI and Set Display Dimensions
root = tk.Tk()
root.title('Jora WebScrape Dashboard')
root.geometry("440x840")
folder_path = StringVar()

# Set Up Tabs
tabControl = ttk.Notebook(root)  
tab1 = ttk.Frame(tabControl) 

tabControl.add(tab1, text ='Search') 
tabControl.grid(row=0, column=0) 

def Search_Jora_Button():
	global Kw
	global Ct
	global St

	print(folder_selected)
	os.chdir(str(folder_selected))

	Kw = Keyword_entry.get()
	Ct = City_entry.get()
	St = State_entry.get()
	Path = str(folder_selected)
	Search = [Kw, Ct, St, Path]

	with open("test.txt", "wb") as fp:
		pickle.dump(Search, fp)
		print('Keyword: '+str(Kw))
		print('City: '+str(Ct))
		print('State: '+str(St)+'\n')
		print('Path: '+str(folder_selected))
   
	import Jora_Scrape_test

####### Tab 1 - Search Input and Run Script ##############

# Inputs for the Search
Keyword = tk.Label(tab1, text="Keyword: ").grid(row=0, column=0, sticky='e')
Keyword_entry = tk.Entry(tab1)
Keyword_entry.grid(row=0,column=1,stick='w', columnspan=3)

City = tk.Label(tab1, text="City: ").grid(row=1,column=0, sticky='e')
City_entry = tk.Entry(tab1)
City_entry.grid(row=1,column=1, sticky='w')

State = tk.Label(tab1, text="State: ").grid(row=2,column=0, sticky='e')
State_entry = tk.Entry(tab1)
State_entry.grid(row=2,column=1, sticky='w')


tk.Label(tab1, text="    ").grid(row=0,column=2, sticky='e')
tk.Label(tab1, text="    ").grid(row=0,column=6, sticky='e')






def getFolderPath():
	global folder_selected
	folder_selected = filedialog.askdirectory()
	folder_path.set(folder_selected)
	print(folder_selected)
	





# Add Options
Dictionary = tk.Label(tab1, text="Step 3: ").grid(row=2,column=4, sticky='e')
KInput = tk.Label(tab1, text="Step 2: ").grid(row=1,column=4, sticky='e')
Save = tk.Label(tab1, text="Step 1: ").grid(row=0,column=4, sticky='e')







############## - Filters ##################
def update_salary():
	salsfilter = int(salary.get())
	print(salsfilter)

	# Filter DataFrame
	global df
	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
	df['SalMin'] = df['Salary'].str.replace(",","")
	df['SalMin'] = df.SalMin.str.extract('(\d+)')
	df.dropna(subset=['SalMin'],inplace=True)
	df['SalMin'] = df['SalMin'].astype(int)

	df[df['SalMin'] >= salsfilter].to_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv', index=False) 
	
	# Pandas Table - Update
	LF = tk.LabelFrame(tab1)
	LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
	pt = Table(LF)
	pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
	pt.show()

	# Update Job Titles Based on Salary Filter
	jts = df
	var = tk.StringVar()
	var.set(list(jts['Title'].drop_duplicates()))
	jt = tk.Listbox(tab1, listvariable=var)
	jt.grid(row=11, column=1, sticky='ns')

	# Update Company Based on Salary Filter
	cc = df
	var = tk.StringVar()
	var.set(list(cc['Company'].drop_duplicates()))
	cc = tk.Listbox(tab1, listvariable=var)
	cc.grid(row=13, column=1, sticky='ns')

	# Update Company Based on Salary Filter
	ss = df
	var = tk.StringVar()
	var.set(list(ss['Location'].drop_duplicates()))
	ss = tk.Listbox(tab1, listvariable=var)
	ss.grid(row=15, column=1, sticky='ns')

	############### Update Salary Histogram #########################################################


	def describe_helper(series):
	    splits = str(series.describe()).split()
	    keys, values = "", ""
	    for i in range(0, len(splits), 2):
	    	keys += "{:8}\n".format(splits[i])
	    	values += "{:>.7}\n".format(splits[i+1])
	    return keys, values

	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
	fig, ax = plt.subplots()
	sals = ((df['SalMin'].astype(int))/1000)

	ax.hist(sals)
	plt.figtext(.95, .49, describe_helper(pd.Series(sals))[0])
	plt.figtext(1.05, .49, describe_helper(pd.Series(sals))[1])
	plt.ylabel('Frequency')
	plt.xlabel('Annual Wage')
	sns.set()
	plt.title('Keyword: '+str(Kw)+' '+str(Ct)+' - Salary $K pa (Filtered)')
	plt.savefig(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_Salary_filtered.png',dpi=300, bbox_inches = "tight")

	zoom = 0.16

	# Image 2 - SALARY

	file = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_Salary_filtered.png'
	image = Image.open(file)
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=13, column=3, sticky='we', columnspan=3)

	############ Update Listings Chart ##############################################################

	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
	Date = df.groupby(by=['Listed']).count().reset_index()
	plt.figure(figsize=(10,2))
	plt.plot(Date['Listed'], Date['Company'])
	plt.title('Keyword: '+str(Kw)+' '+str(Ct)+' - Job Listings (filtered)')
	plt.ylabel('Number of New Listings')
	plt.xlabel('Listing Date')
	plt.xticks(Date['Listed'], Date['Listed'], rotation='vertical')
	plt.savefig(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_ListingsDate_Filtered.png',dpi=500, bbox_inches = "tight")

	# Image 1 - LISTING DATE
	zoom = 0.085
	file = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_ListingsDate_Filtered.png'
	image = Image.open(file)
	#multiple image size by zoom
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	# Plots
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=11, column=3, sticky='we', columnspan=3)












def update_ListingDate():
	datefilter = int(ListingDate.get())
	print(datefilter)

	# Pandas Table - Update
	LF = tk.LabelFrame(tab1)
	LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
	df[df['LAge'] < datefilter].to_csv('C:/Users/Toby/Desktop/Webscraping/'+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv', index=False) 
	pt = Table(LF)
	pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
	pt.show()

	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
	Date = df.groupby(by=['Listed']).count().reset_index()
	plt.figure(figsize=(10,2))
	plt.plot(Date['Listed'], Date['Company'])
	plt.title('Keyword: '+str(Kw)+' '+str(Ct)+' - Job Listings (filtered)')
	plt.ylabel('Number of New Listings')
	plt.xlabel('Listing Date')
	plt.xticks(Date['Listed'], Date['Listed'], rotation='vertical')
	plt.savefig(str(folder_selected)+str(Kw)+'_'+str(City)+'_ListingsDate_Filtered.png',dpi=500, bbox_inches = "tight")

	# Image 1 - LISTING DATE
	zoom = 0.085
	file = str(folder_selected)+str(Kw)+'_'+str(City)+'_ListingsDate_Filtered.png'
	image = Image.open(file)
	#multiple image size by zoom
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	# Plots
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=11, column=3, sticky='we', columnspan=3)







def update_titles():
	# Job Title - Update Database based on Job Title Selection
	global jt
	if jt.curselection():
		for i in jt.curselection():
			jtfilter = jt.get(i)
			print(jtfilter)
		dfFiltered = df[df['Title']==jtfilter] 
		# print(dfFiltered)


		# Pandas Table - Update
		LF = tk.LabelFrame(tab1)
		LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
		df[df['Title']==jtfilter].to_csv('C:/Users/Toby/Desktop/Webscraping/'+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv', index=False) 
		pt = Table(LF)
		pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
		pt.show()

		# Update Job Titles Based on Salary Filter
		jt = df
		var = tk.StringVar()
		var.set(list(jt['Title'].drop_duplicates()))
		
		jt = tk.Listbox(tab1, listvariable=var)
		jt.grid(row=11, column=1, sticky='ns')

		# Update Company Based on Salary Filter
		cc = df
		var = tk.StringVar()
		var.set(list(cc['Company'].drop_duplicates()))
		cc = tk.Listbox(tab1, listvariable=var)
		cc.grid(row=13, column=1, sticky='ns')

	else:
		pass












def update_company():
	# Company - Update Database based on Company Selection
	if cc.curselection():
		for i in cc.curselection():
			ccfilter = cc.get(i)
			print(ccfilter)
		dfFiltered = df[df['Company']==ccfilter] 
		# print(dfFiltered)

		# Pandas Table - Update
		LF = tk.LabelFrame(tab1)
		LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
		df[df['Company']==ccfilter].to_csv('C:/Users/Toby/Desktop/Webscraping/'+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv', index=False) 
		pt = Table(LF)
		pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
		pt.show()

		# Update Job Titles Based on Salary Filter
		global cjts
		cjts = df
		var = tk.StringVar()
		var.set(list(cjts['Title'].drop_duplicates()))
		cjts = tk.Listbox(tab1, listvariable=var)
		cjts.grid(row=11, column=1, sticky='ns')

		# Update Company Based on Salary Filter
		global ccc
		ccc = df
		var = tk.StringVar()
		var.set(list(ccc['Company'].drop_duplicates()))
		ccc= tk.Listbox(tab1, listvariable=var)
		ccc.grid(row=13, column=1, sticky='ns')

	else:
		pass










def update_location():
	# Software - Update Database based on Software Selection
	if ss.curselection():
		for i in ss.curselection():
			ssfilter = ss.get(i)
		print(ssfilter)

		# Pandas Table - Update
		LF = tk.LabelFrame(tab1)
		LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
		df[df['Location']==ssfilter].to_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv', index=False) 
		pt = Table(LF)
		pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Filtered.csv')
		pt.show()
	else:
		pass












def Import_Results():
# try:
	root.geometry("1190x960")
	global df
	df = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv').drop_duplicates()

	# Pandas Table
	LF = tk.LabelFrame(tab1)
	LF.grid(row=11, column=7, rowspan=3, sticky='ns', columnspan=2)
	pt = Table(LF)
	pt.importCSV(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
	pt.show()

	try:
		zoom = 0.165
		software = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/TopKeywords_Software.png'
		image = Image.open(software)
		#multiple image size by zoom
		pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
		# Plots
		photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
		label = Label(tab1, image = photo)
		label.image = photo
		label.grid(row=15, column=7, sticky='n')
	except:
		pass


	# Adding HeatMap Location if Search Does not specify City
	if str(Ct) == "":
		zoom = 0.145
		LocalHeatM = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/JobsLocation_'+str(Kw)+'.png'
		image = Image.open(LocalHeatM)
		#multiple image size by zoom
		pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
		# Plots
		photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
		label = Label(tab1, image = photo)
		label.image = photo
		label.grid(row=15, column=8, sticky='n')
	else:
		try:
			zoom = 0.165
			industries = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/TopKeywords_Industries.png'
			image = Image.open(industries)
			#multiple image size by zoom
			pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
			# Plots
			photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
			label = Label(tab1, image = photo)
			label.image = photo
			label.grid(row=15, column=8, sticky='n')
		except:
			pass

	# Create Salary Scale and Set to 0 until Data is imported and read (Import Data Fuction)
	try:
		sal = pd.read_csv(str(folder_selected)+str(Kw)+"_"+str(Ct)+"/Salary.csv").astype(int)
		lowest = sal.sort_values(by='min', ascending=True).reset_index()
		highest = sal.sort_values(by='min', ascending=False).reset_index()
		global salary
		salary = IntVar()
		sals = Scale(tab1, variable=salary, from_=int(lowest['min'][0]), to=int(highest['min'][0]), orient=HORIZONTAL).grid(row=6,column=1, sticky='w')
	except:
		pass

	# UPDATE EXPERIENCE SLIDER

	try:
		jts = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
		var = tk.StringVar()
		var.set(list(jts['Title'].drop_duplicates()))
		global jt
		jt = tk.Listbox(tab1, listvariable=var)
		jt.grid(row=11, column=1, sticky='ns')
	except:
		pass


	try:
		Comps = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
		var2 = tk.StringVar()
		var2.set(list(Comps['Company'].drop_duplicates()))
		global cc
		cc = tk.Listbox(tab1, listvariable=var2)
		cc.grid(row=13,column=1, sticky='ns')
	except:
		pass


	try:
		Locs = pd.read_csv(str(folder_selected)+str(Kw)+'_'+str(Ct)+'/Data_Downloaded.csv')
		var3 = tk.StringVar()
		var3.set(list(Locs['Location'].drop_duplicates()))
		global ss
		ss = tk.Listbox(tab1, listvariable=var3)
		ss.grid(row=15,column=1, sticky='ns')
	except:
		pass


	# Search Fields
	Output = tk.Label(tab1, text="Keywords: "+str(Kw)).grid(row=6,column=3, sticky='ws')
	Output = tk.Label(tab1, text="City: "+str(Ct)+", "+str(St)).grid(row=7,column=3, sticky='ws')

	count = pd.read_csv(str(folder_selected)+str(Kw)+"_"+str(Ct)+"/dataframe.csv")['Key_Points'].count()
	Output = tk.Label(tab1, text="Jobs Found: "+str(count)).grid(row=8,column=3, sticky='ws')     


	# Image 1 - LISTING DATE
	zoom = 0.085
	file = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_ListingsDate.png'
	image = Image.open(file)
	#multiple image size by zoom
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	# Plots
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=11, column=3, sticky='we', columnspan=3)

	zoom = 0.16

	# Image 2 - SALARY
	file = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_Salary.png'
	image = Image.open(file)
	#multiple image size by zoom
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	# PlotsCheckbutton(tab1, text=" Casual Jobs ", variable=var6).grid(row=1, column=3, sticky='w')
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=13, column=3, sticky='we', columnspan=3)


	# Image 3 - EXPERIENCE
	file = str(folder_selected)+str(Kw)+'_'+str(Ct)+'/'+str(Kw)+'_'+str(Ct)+'_Experience.png'
	image = Image.open(file)
	#multiple image size by zoom
	pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
	# Plots
	photo = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
	label = Label(tab1, image = photo)
	label.image = photo
	label.grid(row=15, column=3, sticky='we', columnspan=3)














# Salary
SalFilter = tk.Label(tab1, text="Salary: ").grid(row=5,column=1, sticky='ws')
w = Scale(tab1, from_=0, to=0, orient=HORIZONTAL).grid(row=6,column=1, sticky='w')

# Listing Age
Date = tk.Label(tab1, text="Listing Age (Days): ").grid(row=8,column=1, sticky='ws')
global ListingDate
ListingDate = IntVar()
Dates = Scale(tab1, variable=ListingDate, from_=0, to=31, orient=HORIZONTAL).grid(row=9,column=1, sticky='w')

Output = tk.Label(tab1, text="Titles: ").grid(row=10,column=1, sticky='ws')
var = tk.StringVar().set("")
tk.Listbox(tab1, listvariable=var).grid(row=11,column=1, sticky='w')


# # Companies
Output = tk.Label(tab1, text="Companies: ").grid(row=12,column=1, sticky='ws')
var2 = tk.StringVar()
var2.set("")
lb = tk.Listbox(tab1, listvariable=var2).grid(row=13,column=1, sticky='w')


# # Location
Output = tk.Label(tab1, text="Location: ").grid(row=14,column=1, sticky='ws')
var3 = tk.StringVar()
var3.set("")
lb = tk.Listbox(tab1, listvariable=var3).grid(row=15,column=1, sticky='e')


# Search
# Output = tk.Label(tab1, text="Search Results: ").grid(row=5,column=3, sticky='ws')
Output = tk.Label(tab1, text="Keywords: ").grid(row=6,column=3, sticky='ws')
Output = tk.Label(tab1, text="City: ").grid(row=7,column=3, sticky='ws')
Output = tk.Label(tab1, text="Jobs Found : ").grid(row=8,column=3, sticky='ws')
Output = tk.Label(tab1, text="       ").grid(row=5,column=2, sticky='w')

# Buttons
Button(tab1, text=' Import Data ', command=Import_Results).grid(row=2,column=5)
Button(tab1, text=' Filter', command=update_salary).grid(row=6,column=0, sticky='ns')
Button(tab1, text=' Filter', command=update_ListingDate).grid(row=9,column=0, sticky='ns')
Button(tab1, text=' Filter', command=update_titles).grid(row=11,column=0, sticky='ns')
Button(tab1, text=' Filter', command=update_company).grid(row=13,column=0, sticky='ns')
Button(tab1, text=' Filter', command=update_location).grid(row=15,column=0, sticky='ns')
Button(tab1, text=' Reset Filters', command=Import_Results).grid(row=20,column=1, sticky='ns')
folderpath = ttk.Button(tab1, text="Save Loc",command = getFolderPath).grid(row=0,column=5)
Run_Scrape =tk.Button(tab1, text=" Search Jora ", command = lambda: Search_Jora_Button()).grid(row=1,column=5)


# MainLoop
root.mainloop()

