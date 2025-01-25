import tkinter as tk
from tkinter import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
from tkinter import filedialog
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image

root = tk.Tk()
logo=root.iconbitmap('C:\\Users\\salam\\Downloads\\NPC_ENG.ico')
imagee=Image.open('C:\\Users\\salam\\Downloads\\NPC_ENG.png')
myimage=ImageTk.PhotoImage(imagee)
img_label=Label(root,image=myimage)
img_label.pack()

RadioCentral=StringVar(value='Q[mS/m]V1.0')
label1=Label(root,text='Analiz etmek istediyiniz versiyani secin:').pack()
Radioduz1=Radiobutton(root,text='1 metr-de duzluluq',value='Q[mS/m]V1.0',variable=RadioCentral).pack()
Radioduz1=Radiobutton(root,text='0.5 metr-de duzluluq',value='Q[mS/m]V0.5',variable=RadioCentral).pack()
Radioduz1=Radiobutton(root,text='1 metr-de I',value='I[ppt]V1.0',variable=RadioCentral).pack()
Radioduz1=Radiobutton(root,text='0.5 metr-de I',value='I[ppt]V0.5',variable=RadioCentral).pack()
label2=Label(root,text='Xeritedeki noqte boyukluyunu secin:').pack()
size_of_bubbles=IntVar(value=30)
accuracy=IntVar(value=45)

Radiomarker3=Radiobutton(root,text='15',value=15,variable=size_of_bubbles).pack()
Radiomarker4=Radiobutton(root,text='30',value=30,variable=size_of_bubbles).pack()
Radiomarker5=Radiobutton(root,text='50',value=50,variable=size_of_bubbles).pack()
Radiomarker6=Radiobutton(root,text='75',value=75,variable=size_of_bubbles).pack()
labelaccuracy=Label(root,text='Deqiqlik seviyyesini secin:').pack()
Radioaccuracy1_5=Radiobutton(root,text='1/10',value=10,variable=accuracy).pack()
Radioaccuracy1_15=Radiobutton(root,text='1/15',value=15,variable=accuracy).pack()
Radioaccuracy1_45=Radiobutton(root,text='1/45',value=45,variable=accuracy).pack()
Radioaccuracy1_85=Radiobutton(root,text='1/85',value=85,variable=accuracy).pack()

Label_of_colorcode='Duzluluq'
if RadioCentral.get()=='Q[mS/m]V1.0':
    Label_of_colorcode='1 metr-de duzluluq'
elif RadioCentral.get()=='Q[mS/m]V0.5':
    Label_of_colorcode='0.5 metr-de duzluluq'
elif RadioCentral.get()=='I[ppt]V1.0':
    Label_of_colorcode='1 metr-de I'
elif RadioCentral.get()=='I[ppt]V0.5':
    Label_of_colorcode='0.5 metr-de I'



Label_of_colorcode='1 metr-de duzluluq'




def open_file():
   global file
   file = filedialog.askopenfile(mode='r', filetypes=[('CSV', '*.csv')])
   ttk.Button(root, text="Show Map", command=root.quit).pack(pady=20)
label = Label(root, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)
ttk.Button(root, text="Browse", command=open_file).pack(pady=20)







root.mainloop()

Data=pd.read_csv(file)
number_of_neighbors=int(round(len(Data)/395,0))


All_corr_long=[]
counterr=0
for long in Data['Longitude']:
    counterr=counterr+1
    if counterr%(accuracy.get())==0:
        All_corr_long.append(np.round(long,5))

All_corr_lat=[]
Final_long=[]
for x in All_corr_long:
    z=0
    
    listim=[]
    listim2=[]
    Minim=min(Data[np.round(Data['Longitude'],4)==np.round(x,4)]['Latitude'])
    Maxim=max(Data[np.round(Data['Longitude'],4)==np.round(x,4)]['Latitude'])
    listim=list(np.linspace(Minim,Maxim,len(All_corr_long)))
    while z< len(All_corr_long):
        listim2.append(x)
        z=z+1
    Final_long.append(listim2)
    All_corr_lat.append(listim)
    print(x,Minim,Maxim)

Ffinal_long=[]
for x in Final_long:
    for z in x:
        Ffinal_long.append(z)
Ffinal_lat=[]
for x in All_corr_lat:
    for z in x:
        z=np.round(z,6)
        Ffinal_lat.append(z)
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score,accuracy_score
from sklearn.model_selection import train_test_split
X=Data[['Longitude','Latitude']]
y=Data[RadioCentral.get()]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.05)
from sklearn.neighbors import KNeighborsRegressor
knnR=KNeighborsRegressor(n_neighbors=25)
knnR.fit(X_train,y_train)
y_hat=knnR.predict(X_test)
print(mean_absolute_error(y_test,y_hat), mean_squared_error(y_test,y_hat),r2_score(y_test,y_hat))
r2_score(y_test,y_hat)
for_predict=pd.DataFrame({'Longitude':Ffinal_long,'Latitude':Ffinal_lat})
for_predict=for_predict.drop_duplicates(subset=['Longitude','Latitude'])

Last_df=knnR.predict(for_predict)
ones_of=np.ones(len(for_predict))
ones_of=ones_of*size_of_bubbles.get()

if RadioCentral.get()=='Q[mS/m]V1.0':
    Label_of_colorcode='1 metr-de duzluluq'
elif RadioCentral.get()=='Q[mS/m]V0.5':
    Label_of_colorcode='0.5 metr-de duzluluq'
elif RadioCentral.get()=='I[ppt]V1.0':
    Label_of_colorcode='1 metr-de I'
elif RadioCentral.get()=='I[ppt]V0.5':
    Label_of_colorcode='0.5 metr-de I'







For_prediction_X=pd.DataFrame({'Longitude':for_predict['Longitude'],'Latitude':for_predict['Latitude'],Label_of_colorcode:Last_df,'Priority':ones_of})
For_prediction_X.iloc[0,3]=1
import plotly.express as px
plotly.express.set_mapbox_access_token('pk.eyJ1Ijoic2FsYW1vdmhleWRhciIsImEiOiJjbTAzeTJ4YzkwMnRzMmpxeDF0dDhkczB3In0.pZxxiJuBF1stUo6BMGG04g')
fig = px.scatter_mapbox(For_prediction_X, lat="Latitude", lon="Longitude",color=Label_of_colorcode,zoom=17,size='Priority',size_max=size_of_bubbles.get(),height=1000,opacity=0.3,color_continuous_scale=['White','Red','Black'])
fig.update_layout(mapbox_style="satellite")
fig.update_traces()
#fig.update_traces(marker={'symbol': 'diamond'})



fig.show()

