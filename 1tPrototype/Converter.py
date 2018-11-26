# Convert ROOT file to HDF5 file

import pandas as pd
import numpy as np
import ROOT
import sys
import h5py

if len(sys.argv)!=2:
    print("Wront arguments!")
    print("Usage: python converter.py RunNo")
    sys.exit(1)

RunNo = int(sys.argv[1])

FileNo = 0
windowSize = 1029

f = h5py.File("Run%d.h5"%(RunNo), "w")
g1 = f.create_group("TriggerInfo")
g2 = f.create_group("Waveform")

# Loop for ROOT files
while True:
    t = ROOT.TChain("Readout")
    if FileNo==0:
        filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d.root"%(RunNo,RunNo)
    else:
        filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d_%d.root"%(RunNo,RunNo,FileNo)
    if t.Add(filename) == 0:
        break
    print("Processing Run %d File %d "%(RunNo, FileNo)+" ...")

    # Allocate memery first, for efficiency
    nTrigger = t.GetEntries()
    evtid = np.zeros((nTrigger,), dtype="int64")
    sec = np.zeros((nTrigger,), dtype="int64")
    nanosec = np.zeros((nTrigger,), dtype="int64")
    ch_entry = t.Draw("ChannelId","","goff")
    ch_evtid = np.zeros((ch_entry,), dtype="int64")
    chlid = np.zeros((ch_entry,), dtype='int16')
    wav = np.zeros((ch_entry*windowSize,), dtype='int16')

    # Loop for event, fill the arrays
    ch_idx = 0
    wav_idx = 0
    trig_idx = 0
    for event in t:
        nChannel = event.ChannelId.size()
        wavSize = event.Waveform.size()

        evtid[trig_idx:trig_idx+1] = event.TriggerNo
        sec[trig_idx:trig_idx+1] = event.Sec
        nanosec[trig_idx:trig_idx+1] = event.NanoSec
        trig_idx = trig_idx+1

        ch_evtid[ch_idx:ch_idx+nChannel] = event.TriggerNo
        chlid[ch_idx:ch_idx+nChannel] = list(event.ChannelId)
        ch_idx = ch_idx+nChannel
        wav[wav_idx:wav_idx+wavSize] = list(event.Waveform)
        wav_idx = wav_idx+wavSize
    
    # Create dataset
    wav = wav.reshape(-1,windowSize)
    if FileNo==0:
        dset0 = g1.create_dataset("EventID", data=evtid, maxshape=(None,))
        dset1 = g1.create_dataset("Sec",     data=sec, maxshape=(None,))
        dset2 = g1.create_dataset("NanoSec", data=nanosec, maxshape=(None,))

        dset3 = g2.create_dataset("EventID", data=ch_evtid, maxshape=(None,))
        dset4 = g2.create_dataset("ChannelID", data = chlid, maxshape=(None,))
        dset5 = g2.create_dataset("Waveform", data = wav, maxshape=(None,windowSize), compression="gzip", compression_opts=4)
    else:
        dset0.resize(dset0.shape[0]+nTrigger, axis=0)
        dset1.resize(dset1.shape[0]+nTrigger, axis=0)
        dset2.resize(dset2.shape[0]+nTrigger, axis=0)
        dset0[-evtid.shape[0]:] = evtid
        dset1[-sec.shape[0]:] = sec
        dset2[-nanosec.shape[0]:] = nanosec
        dset3.resize(dset3.shape[0]+ch_entry, axis=0)
        dset4.resize(dset4.shape[0]+ch_entry, axis=0)
        dset5.resize(dset5.shape[0]+ch_entry, axis=0)
        dset3[-ch_evtid.shape[0]:] = ch_evtid
        dset4[-chlid.shape[0]:] = chlid
        dset5[-wav.shape[0]:] = wav
    FileNo = FileNo+1

f.close()
                
