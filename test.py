import somlib as sl
import parlib as pl
import numpy as np
import os
import natsort


pcapname = "test.pcap"
directory = "asd/"
filename = "csv"
somsize = 20
ksize = 6

pl.csv5(directory+filename,pcapname)
tmparr=[]
for filename in os.listdir(directory):
	if filename.endswith(".csv"):
		tmparr.append(filename)
	else:
		continue
visual_list = natsort.natsorted(tmparr)

kmap = np.load("kmap.npy")
weights = np.load("weights.npy")

for x in visual_list:
	temp = directory+x
	csv = sl.opencsv(temp)
	norm = sl.normalized(csv)
	hits = sl.som_hits(weights, norm)
	name = ("img/" + x + ".png")
	sl.disp(kmap,name,hits)
