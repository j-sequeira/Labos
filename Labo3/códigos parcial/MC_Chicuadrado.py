import numpy as np
from numpy import random
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import chi2

def lineal(x,m,b):
	return m*x+b

def coef_determinacion(x,y,m,b):
	R2=1-sum((y-m*x-b)**2)/sum((y-np.mean(y))**2)
	return R2

def ajustelineal(x,y,dy):
	w=1/dy**2
	SX=np.sum(x*w)
	SY=np.sum(w*y)
	SX2=np.sum(w*(x**2))
	SXY=np.sum(w*x*y)
	SW=np.sum(w)
	Xmed=SX/SW
	Ymed=SY/SW
	Varx=SX2/SW-Xmed**2
	delta=(SW**2)*Varx
	m=(SXY*SW-SX*SY)/delta
	b=(SX2*SY-SX*SXY)/delta
	Varm=np.sum(w*((y-m*x-b)**2))/((len(x)-2)*SW*Varx )
	Varb=Varm * SX2 / SW
	R2=1-sum((y-m*x-b)**2)/sum((y-np.mean(y))**2)#coeficiente de indeterminacion
	return m,b,Varm,Varb, R2

def chicuadrado(x,y,dy,m,b):
	w=1/dy**2
	chicuadrado=np.sum(w*(y-m*x-b)**2)
	return chicuadrado

def ajustes_graf(x,y,dy,m,b,varm,varb):
	ajuste_lb = 'm = (' + str(round(m,2)) + ' \xB1 ' + str(round(np.sqrt(varm),2)) + ') k$\\Omega$  b = (' + str(round(b,2)) + ' \xB1 ' + str(round(np.sqrt(varb),2)) + ') V'
	archivo_nombre = 'ohm_con_ajuste_' + str(j)+'.png'
	titled = 'R^{2} = ' + str(round(R2))
	plt.figure(1,figsize=(9,5))
	plt.errorbar(x,y,yerr=dy,marker='h',markersize=4, ls='None', color='b', label='Datos')
	plt.plot(x,m*x+b,color='red', label=ajuste_lb)
	plt.tick_params(direction='in')
	plt.xlabel("I [mA]",fontsize=16)
	plt.ylabel("$V_{R}$ [V]",fontsize=16)
	plt.legend(fontsize=12, loc= 4)
	plt.grid(linestyle='--', linewidth=1)
	plt.xlim([0,n+1])
	plt.ylim([-0.5,n+1])
	plt.savefig(archivo_nombre)
	plt.show(block=False)
	plt.title(titled)
	plt.pause(0.5)
	plt.close()

def histo_graf():
	archivo_nombre = 'histo_chi2_ohm_' + str(j)+'.png'
	title = 'N = ' + str(j)
	plt.figure(2,figsize=(9,5))
	plt.hist(chicuad_h, bins=25,density=True,color='green', label='Muestreo')
	plt.plot(Xi_chi2,ajustechi2(Xi_chi2,n-2),color='red', label='pdf')
	plt.legend(fontsize=12, loc= 1)
	plt.xlim([0,4*(n-2)])
	#plt.ylim([0,0.25])
	plt.xlabel("χ$^{2}_{ν}$ ",fontsize=14)
	plt.ylabel("$\\frac{f}{N\\Delta χ^{2}}$ ",fontsize=16, rotation = 0, labelpad=20,y=0.85)
	plt.title(title)
	plt.show(block=False)
	plt.savefig(archivo_nombre)
	plt.pause(0.1)
	plt.close()

def ajustechi2(x,k):
	return chi2.pdf(x,k)

N=1								#Tamaño de la muestra del histograma de Chi-Cuadrado
n=10							#cantidad de valores de corriente inyectados al circuito
corriente=np.linspace(1,n,n)	#[mA]
R=1.0							#[kOhm]
#VR=np.array([])
VR=R*corriente					#esperanza de la variable aleatoria "caída de tensión en el resistor"
dVR=np.zeros(n)+0.2				#incerteza en la medición de VR
VRmed=np.zeros(n)				#Montecarlo de VR
VRmed2=np.zeros(n)				#Rotación de VRmed
chicuad_h = []					#histograma de Chicuadrado

Xi_chi2=np.linspace(0,4*(n-2),100) #realización de la v.a. chi2,gl(n-2)

#Simulo N mediciones con n datos cada una y en cada caso obtengo el ajuste lineal por cuadrados mínimos
#Guardo en un array el minimo de chicuadrado de cada ajuste para hacer un histograma
"""for j in range(N):
	for i in range(n):
		VRmed[i]=random.normal(VR[i],dVR[i])

	m, b, varm, varb , R2 = ajustelineal(corriente,VRmed,dVR)
	ajustes_graf()
	chicuad_h.append(chicuadrado(corriente,VRmed,dVR,m,b))
	
	#if j%10 == 0:	histo_graf()"""

#Una medición
for i in range(n):
	VRmed[i]=random.normal(VR[i],dVR[i])

#print(VRmed)
j=0
m, b, varm, varb , R2 = ajustelineal(corriente,VRmed,dVR)
ajustes_graf(corriente,VRmed,dVR,m,b,varm,varb)
#print(m,b, R2)
pvalor=1-chi2.cdf(chicuadrado(corriente,VRmed,dVR,m,b),n-2)
print(pvalor)
print(chicuadrado(corriente,VRmed,dVR,m,b))

#print(chi2.sf(chicuadrado(corriente,VRmed,dVR,m,b),n-2))
promedio=chi2.mean(n-2)
mediana=chi2.median(n-2)
varianza=chi2.var(n-2)
desvest=chi2.std(n-2)
#Display
plt.figure(2,figsize=(9,5))
x = np.linspace(chi2.ppf(0.01, n-2),chi2.ppf(0.99, n-2), 100)
plt.ylim([0,0.12])
plt.xlim([0,4*(n-2)])
plt.plot(Xi_chi2, chi2.pdf(Xi_chi2, n-2), scaley = False, color='red', lw=2, label='χ$^{2}_{8}$ pdf')
px=np.linspace(chicuadrado(corriente,VRmed,dVR,m,b),30,100)
plt.fill_between(px, chi2.pdf(px, n-2) , alpha = 0.6)
plt.xticks(np.arange(0, 4*(n-2), 2))
plt.tick_params(direction="in")
plt.axvline(x = chicuadrado(corriente,VRmed,dVR,m,b), color = 'b', label = 'χ$^{2}_{min}$')#, ymin=0.0, ymax=vlyuplim
plt.axvline(x = promedio, color = 'green', label = 'Valor medio')
plt.legend(fontsize=12, loc= 1)
plt.xlabel("χ$^{2}_{8}$ ",fontsize=14)
plt.ylabel("$\\frac{f}{N\\Delta χ^{2}}$ ",fontsize=16, rotation = 0, labelpad=20,y=0.85)
plt.savefig('chi2pdf_pvalor' + '.png')
plt.show()

#histo_graf()

#print(coef_determinacion(corriente,VRmed,m,b))
#print(chicuad_h)
popt, pcov = curve_fit(lineal,corriente,VRmed,sigma=dVR, absolute_sigma=True)
#print(popt, pcov)