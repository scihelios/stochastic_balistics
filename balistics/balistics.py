import tkinter as tk
from tkinter import *
import math as m
import time
from fpdf import FPDF
import random 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits import mplot3d
import customtkinter


class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master=master
		pad=3
		self._geom='200x200+0+0'
		master.geometry("{0}x{1}+0+0".format(
			master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.bind('<Escape>',self.toggle_geom)
	def toggle_geom(self,event):
		geom=self.master.winfo_geometry()
		print(geom,self._geom)
		self.master.geometry(self._geom)
		self._geom=geom


def AD(altitude,g):
	TSL=284.15
	L_rate=6.5*0.001
	M=0.0289644
	R=8.3144598
	ro=1.252

	return ro*(TSL/(TSL+L_rate*altitude))**(1+(g*M)/(R*L_rate))





def calculate_traj(v0,alpha,psi,coeff,mass,prec):
	#constants:
	R=6370000
	g=9.80665
	new_g=[g]

	#prec and airtime in ms
	airtime=0
	prec=prec/1000000
	x_v=v0*m.cos((alpha/180)*m.pi)*m.cos((psi/180)*m.pi)
	y_v=v0*m.cos((alpha/180)*m.pi)*m.sin((psi/180)*m.pi)
	z_v=v0*m.sin((alpha/180)*m.pi)
	
	elev=[0]
	distancex=[0]
	distancey=[0]
	while (z_v>0):
		elev+=[elev[-1]+z_v*prec]
		new_g+=[g*(R/(R+elev[-1]))**2]
		airtime+=prec
		distancex+=[distancex[-1]+x_v*prec]
		distancey+=[distancey[-1]+y_v*prec]
		x_v=x_v+(-(coeff*AD(elev[-1],new_g[-1])/mass)*x_v**2)*prec
		y_v=y_v+(-(coeff*AD(elev[-1],new_g[-1])/mass)*y_v**2)*prec
		z_v=z_v+prec*((-new_g[-1])-(coeff*AD(elev[-1],new_g[-1])/mass)*z_v**2)

	while (elev[-1]>0) :
		elev+=[elev[-1]+z_v*prec]
		new_g+=[g*(R/(R+elev[-1]))**2]
		airtime+=prec
		distancex+=[distancex[-1]+x_v*prec]
		distancey+=[distancey[-1]+y_v*prec]
		x_v=x_v+(-(coeff*AD(elev[-1],new_g[-1])/mass)*x_v**2)*prec
		y_v=y_v+(-(coeff*AD(elev[-1],new_g[-1])/mass)*y_v**2)*prec
		z_v=z_v+prec*((-new_g[-1])+(coeff*AD(elev[-1],new_g[-1])/mass)*z_v**2)	

	distancex=distancex[0:len(elev)]
	distancey=distancey[0:len(elev)]
	print(distancex[-1],distancey[-1])

	return [distancex,distancey,elev]




def calculate_trajectory():
	psi=float(texta.get())
	alpha=float(textb.get())
	v0=float(textc.get())
	mass=float(textd.get())

	'''psi=30
	alpha=70
	v0=800
	mass=9'''
	diam=0.12
	coeff=(0.5*0.25*(diam**2)*m.pi)/4
	prec=300

	g=calculate_traj(v0,alpha,psi,coeff,mass,prec)

	ax = plt.axes(projection='3d')
	
	ax.plot3D(g[0],g[1],g[2])
	ax.plot3D(500*np.sin([i/1000 for i in range(6300)])+np.array([5800 for i in range(6300)]),np.array([8000 for i in range(6300)])+500*np.cos([i/1000 for i in range(6300)]),[0 for i in range(6300)])
	ax.axis([0,10000,0,10000])
	ax.set_zlim(0,10000)

	ax.view_init(23, -109)
	plt.show()	



window=Tk()



window.title("nouvelle composition")

window.geometry('600x600')
window.tk.call("source","azure.tcl")

window.tk.call("set_theme","dark")



texta = Entry(window,width=10,font=("Arial Bold", 15))
textb = Entry(window,width=10,font=("Arial Bold", 15))
textc = Entry(window,width=10,font=("Arial Bold", 15))
textd = Entry(window,width=10,font=("Arial Bold", 15))
texte = Entry(window,width=10,font=("Arial Bold", 15))

lbld = Label(window, text="-----------------New target-------------", font=("Arial Bold", 30))
lbld.place(relx=0.5, rely=0.1, anchor=CENTER)

lblp = Label(window, text="angle acording to x_axes : ",font=("Arial Bold", 15))
lblp.place(relx=0.2, rely=0.3, anchor=W)
texta.place(relx=0.7, rely=0.3, anchor=W)

lbla = Label(window, text="angle acording to z_axes : ",font=("Arial Bold", 15))
lbla.place(relx=0.2, rely=0.4, anchor=W)
textb.place(relx=0.7, rely=0.4, anchor=W)

lblb = Label(window, text="projectile speed :  ",font=("Arial Bold", 15))
lblb.place(relx=0.2, rely=0.5, anchor=W)
textc.place(relx=0.7, rely=0.5, anchor=W)

lblc = Label(window, text="projectile mass : ",font=("Arial Bold", 15))
lblc.place(relx=0.2, rely=0.6, anchor=W)
textd.place(relx=0.7, rely=0.6, anchor=W)
'''
lblv = Label(window, text="Nombre total de mesure  : ",font=("Arial Bold", 15))
lblv.place(relx=0.2, rely=0.7, anchor=W)
texte.place(relx=0.7, rely=0.7, anchor=W)'''


btncomm1 = Button(window, text="FIRE !", command=calculate_trajectory)
btncomm1.place(relx=0.5, rely=0.875, anchor=CENTER)

window.mainloop()


#2d version
'''	#prec and airtime in ms
	airtime=0
	prec=prec/1000000
	x_v=v0*m.cos((alpha/180)*m.pi)
	y_v=v0*m.cos((alpha/180)*m.pi)
	z_v=v0*m.sin((alpha/180)*m.pi)
	
	elev=[0]
	distance=[0]
	while (v_velocity>0):
		elev+=[elev[-1]+v_velocity*prec]
		airtime+=prec
		v_velocity=v_velocity-9.81*prec-((coeff/mass)*v_velocity**2)*prec
	while (elev[-1]>0) :
		elev+=[elev[-1]+v_velocity*prec]
		airtime+=prec
		v_velocity=v_velocity-9.81*prec+((coeff/mass)*v_velocity**2)*prec	
	print(airtime)
	while (airtime>=0) and (h_velocity>=0):
		distance+=[distance[-1]+h_velocity*prec]
		h_velocity=h_velocity-((coeff/mass)*(h_velocity**2))*prec
		airtime+=(-prec)
	distance=distance[0:len(elev)]	
	return [distance,elev]
'''

#excess code
'''
im = plt.imread('canon.png')
fig, ax = plt.subplots()
ax.plot(g[0],g[1])
newax = fig.add_axes([0.075,0.075,0.07,0.07], anchor='S', zorder=1)
newax.imshow(im)
newax.axis('off')

ax.axis([0,10000,0,10000])'''
'''img = mpimg.imread('canon.png')
plt.imshow(img)'''
'''lum_img = img[:, :, 0]
plt.imshow(lum_img)'''