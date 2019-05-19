# Convert ROOT file to HDF5 file

import pandas as pd
import numpy as np
import ROOT
import sys
import h5py, argparse

psr = argparse.ArgumentParser()
psr.add_argument("--limit", type=int, default=999, help="limit of number of files to process")
psr.add_argument('ipt', type=int, help="input run number")
psr.add_argument('-o', dest="opt", help="output")
args = psr.parse_args()

RunNo = args.ipt

FileNo = 0
windowSize = 1029

wf_t=[("EventID", np.int64), ("ChannelID", np.int16), ("Waveform", np.int16, 1029)]
ti_t=[("EventID", np.int64), ("Sec", np.int32), ("NanoSec", np.int32)]

f = h5py.File(args.opt, "w")

# Loop for ROOT files
while True:
    t = ROOT.TChain("Readout")
    if FileNo==0:
        filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d.root"%(RunNo,RunNo)
    else:
        filename = "/home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run%08d/*_%08d_%d.root"%(RunNo,RunNo,FileNo)
    if t.Add(filename) == 0 or FileNo >= args.limit:
        break
    print("Processing Run %d File %d "%(RunNo, FileNo)+" ...")

    # Allocate memery first, for efficiency
    nTrigger = t.GetEntries()

    ti = np.zeros(nTrigger, dtype=ti_t)
    evtid = ti["EventID"]
    sec = ti["Sec"]
    nanosec = ti["NanoSec"]

    ch_entry = t.Draw("ChannelId","","goff")

    
    wf = np.zeros(ch_entry, dtype=wf_t)
    
    ch_evtid = wf["EventID"]
    chlid = wf["ChannelID"]
    wav = wf["Waveform"]

    # Loop for event, fill the arrays
    ch_idx = 0
    wav_idx = 0
    trig_idx = 0
    for event in t:
        nChannel = event.ChannelId.size()
        wavSize = event.Waveform.size() // windowSize

        evtid[trig_idx:trig_idx+1] = event.TriggerNo
        sec[trig_idx:trig_idx+1] = event.Sec
        nanosec[trig_idx:trig_idx+1] = event.NanoSec
        trig_idx = trig_idx+1

        ch_evtid[ch_idx:ch_idx+nChannel] = event.TriggerNo
        chlid[ch_idx:ch_idx+nChannel] = list(event.ChannelId)
        ch_idx = ch_idx+nChannel
        
        wav[wav_idx:wav_idx+wavSize] = np.array(event.Waveform).reshape(-1, windowSize)
        wav_idx = wav_idx+wavSize
    
    # Create dataset
    wav = wav.reshape(-1,windowSize)
    if FileNo==0:
        dti = f.create_dataset("TriggerInfo", data=ti, maxshape=(None,), compression="gzip", compression_opts=9)
        dwf = f.create_dataset("Waveform", data=wf, maxshape=(None,), compression="gzip", compression_opts=9)
    else:
        
        dti.resize(dti.shape[0]+nTrigger, axis=0)
        dti[-ti.shape[0]:] = ti
        dwf.resize(dwf.shape[0]+ch_entry, axis=0)
        dwf[-wf.shape[0]:] = wf
    FileNo = FileNo+1

f.close()
