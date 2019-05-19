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


f = h5py.File(args.opt, "w")
g1 = f.create_group("TriggerInfo")

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
    evtid = np.zeros((nTrigger,), dtype="int64")
    sec = np.zeros((nTrigger,), dtype="int64")
    nanosec = np.zeros((nTrigger,), dtype="int64")

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
        dset0 = g1.create_dataset("EventID", data=evtid, maxshape=(None,))
        dset1 = g1.create_dataset("Sec",     data=sec, maxshape=(None,))
        dset2 = g1.create_dataset("NanoSec", data=nanosec, maxshape=(None,))

        dwf = f.create_dataset("Waveform", data=wf, maxshape=(None,), compression="gzip", compression_opts=9)
    else:
        dset0.resize(dset0.shape[0]+nTrigger, axis=0)
        dset1.resize(dset1.shape[0]+nTrigger, axis=0)
        dset2.resize(dset2.shape[0]+nTrigger, axis=0)
        dset0[-evtid.shape[0]:] = evtid
        dset1[-sec.shape[0]:] = sec
        dset2[-nanosec.shape[0]:] = nanosec
        
        dwf.resize(dwf.shape[0]+ch_entry, axis=0)
        dwf[-wf.shape[0]:] = wf
    FileNo = FileNo+1

f.close()
