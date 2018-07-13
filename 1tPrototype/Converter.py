# Convert ROOT file to HDF5 file

import pandas as pd
import numpy as np
import ROOT
import sys

if len(sys.argv)!=2:
	print("Wront arguments!")
	print("Usage: python converter.py RunNo")
	sys.exit(1)

RunNo = int(sys.argv[1])

t = ROOT.TChain("Readout")
i = 0
while True:
	if i==0:
		filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d.root"%(RunNo,RunNo)
	else:
		filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d_%d.root"%(RunNo,RunNo,i)
	if t.Add(filename) == 0:
		print("Add %d files."%(i))
		break
	i = i+1

columnName = ["EventID", "Sec", "NanoSec"]
store = pd.HDFStore("data/Run%d.h5"%(RunNo), "w", complevel=9)

for event in t:
	nChannel = event.ChannelId.size()
	windowSize = event.Waveform.size()//nChannel

	TriggerInfo = pd.DataFrame([[event.TriggerNo, event.Sec, event.NanoSec]],  columns=columnName, index=[event.TriggerNo])

	channelArray = np.array(list(event.ChannelId), dtype='int16')
	ChannelID = pd.Series(channelArray, index=np.array([event.TriggerNo]*nChannel))

	waveformMatrix = np.array(list(event.Waveform), dtype='int16').reshape(event.ChannelId.size(), windowSize)
	Waveform = pd.DataFrame(waveformMatrix, index=np.array([event.TriggerNo]*nChannel))

	store.append('TriggerInfo', TriggerInfo, index=False)
	store.append('ChannelID', ChannelID, index=False)
	store.append('Waveform', Waveform, index=False)

store.close()
