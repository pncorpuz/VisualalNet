from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls import url
import somlib as sl
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import parlib as pl
import natsort
import os, shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.


def home(request):
    return render(request,'home.html')


def delete(folder):
    
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

        
def process(request):
    
    if "GET" == request.method:
        return HttpResponse("error")

    myfile  = request.FILES["pcap_file"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name,myfile)
    uploaded_file_url = fs.url(filename)
    
    maps = os.path.join(settings.BASE_DIR,'static/img/map')
    pies = os.path.join(settings.BASE_DIR,'static/img/pie')
    chaps = os.path.join(settings.BASE_DIR,'static/chap')
    
    delete(maps)
    delete(pies)
    delete(chaps)
    
   #classpercent = SOM(uploaded_file_url)
    time,hits = SOM(uploaded_file_url)
    fs.delete(filename)
    
    
    som_pic = os.listdir(os.path.join(settings.BASE_DIR,'static/img/map')) 
    pie_pic = os.listdir(os.path.join(settings.BASE_DIR,'static/img/pie')) 
    
    sorted_som = natsort.natsorted(som_pic)
    sorted_pie = natsort.natsorted(pie_pic)
    
    
    print(sorted_som)
    print(sorted_pie)
    context={
        'sorted_som':sorted_som,
        'sorted_pie':sorted_pie,
        'data':zip(sorted_som,sorted_pie,time,hits),
        'time':time,
        'hits':hits,
    }
    
    print(time)
    print(hits)
    return render(request,'process.html',context)

def normalized(csv):
#NORMALIZE PART#
	#print(csv)
	scaler = MinMaxScaler()
	scaler.fit(csv)
	scaler.data_max_
	np.set_printoptions(precision=3)
	np.set_printoptions(suppress=True)
	a = scaler.transform(csv) #normalized array
	return a

def SOM(som):
    
    print("starting")
    pcapname = som
    directory = os.path.join(settings.BASE_DIR,"static/chap/")
    img_directory = os.path.join(settings.BASE_DIR,"static/img/")
    filename = "csv"
    somsize = 10
    ksize = 6

    timestamp = pl.csv5(directory+filename,pcapname)
    tmparr=[]
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            tmparr.append(filename)
        else:
            continue
    visual_list = natsort.natsorted(tmparr)

    label = np.load(os.path.join(settings.BASE_DIR,"static/npy/labels.npy")) 
    kmap = np.load(os.path.join(settings.BASE_DIR,"static/npy/map.npy"))  
    weights = np.load( os.path.join(settings.BASE_DIR,"static/npy/weights.npy"))   
    count = 0
    hitout = []
    
    for x in visual_list:
        temp = directory+x
        count = count+1
        csv = sl.opencsv(temp)
        norm = sl.normalized(csv)
        hits = sl.som_hits(weights, norm)
        name = (os.path.join(settings.BASE_DIR,"static/img/map/") + x + ".png")
        sl.hit_overlap(kmap,hits,count,img_directory)
        sl.disp(kmap,name,hits,label)
        hitout.append(sl.total_hit(kmap,hits))
        
    
    return (timestamp,hitout)