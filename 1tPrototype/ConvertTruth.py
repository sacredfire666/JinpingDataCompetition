# Convert ROOT file to HDF5 file

import numpy as np
import ROOT
import sys
import h5py
import os

if len(sys.argv)!=3:
    print("Wront arguments!")
    print("Usage: python ConvertTruth.py MCFileName outputFileName")
    sys.exit(1)

baseFileName = sys.argv[1]
outputFileName = sys.argv[2]

FileNo = 0
windowSize = 1029

f = h5py.File(outputFileName, "w")
g1 = f.create_group("Waveform")
g2 = f.create_group("GroundTruth")

# Loop for ROOT files
while True:
    t = ROOT.TChain("Readout")
    tTruth = ROOT.TChain("SimTriggerInfo")
    if FileNo==0:
        filename = baseFileName
    else:
        filename = baseFileName[0:-5]+"_%d.root"%(FileNo)
    if  not os.path.exists(filename):
        break
    t.Add(filename)
    tTruth.Add(filename)
    print("Processing File %d "%(FileNo)+" ...")

    # Allocate memery first, for efficiency
    nTrigger = t.GetEntries()
    ch_entry = t.Draw("ChannelId","","goff")
    ch_evtid = np.zeros((ch_entry,), dtype="int64")
    ch_sec   = np.zeros((ch_entry,), dtype='int64')
    ch_nsec  = np.zeros((ch_entry,), dtype='int64')
    ch_id    = np.zeros((ch_entry,), dtype='int16')
    ch_wav   = np.zeros((ch_entry*windowSize,), dtype='int16')


    # Loop for event, fill the arrays
    ch_idx = 0
    wav_idx = 0
    #trig_idx = 0
    for event in t:
        nChannel = event.ChannelId.size()
        wavSize = event.Waveform.size()

        ch_evtid[ch_idx:ch_idx+nChannel] = event.TriggerNo
        ch_sec[ch_idx:ch_idx+nChannel] = event.Sec
        ch_nsec[ch_idx:ch_idx+nChannel] = event.NanoSec
        ch_id[ch_idx:ch_idx+nChannel] = list(event.ChannelId)
        ch_idx = ch_idx+nChannel
        ch_wav[wav_idx:wav_idx+wavSize] = list(event.Waveform)
        wav_idx = wav_idx+wavSize
    
    nTriggerTruth = tTruth.GetEntries()
    pe_entry_truth = tTruth.Draw("PEList.PMTId","","goff")
    pe_evtid_truth = np.zeros((pe_entry_truth,), dtype="int64")
    pe_pmtid_truth = np.zeros((pe_entry_truth,), dtype="int64")
    pe_time_truth  = np.zeros((pe_entry_truth,), dtype="int64")
    pe_idx = 0
    for event in tTruth:
        trigger_id = event.TriggerNo
        for PE in event.PEList:
            pe_evtid_truth[pe_idx] = trigger_id
            pe_pmtid_truth[pe_idx] = PE.PMTId
            pe_time_truth[pe_idx] = PE.HitPosInWindow
            pe_idx = pe_idx+1

    # Create dataset
    ch_wav = ch_wav.reshape(-1,windowSize)
    if FileNo==0:   # Create new data set

        dset0 = g1.create_dataset("EventID", data=ch_evtid, maxshape=(None,))
        dset1 = g1.create_dataset("ChannelID", data = ch_id, maxshape=(None,))
        dset2 = g1.create_dataset("Sec", data = ch_sec, maxshape=(None,))
        dset3 = g1.create_dataset("NanoSec", data = ch_nsec, maxshape=(None,))
        dset4 = g1.create_dataset("Waveform", data = ch_wav, maxshape=(None,windowSize), compression="gzip", compression_opts=4)

        dset5 = g2.create_dataset("EventID", data=pe_evtid_truth, maxshape=(None,))
        dset6 = g2.create_dataset("ChannelID", data=pe_pmtid_truth, maxshape=(None,))
        dset7 = g2.create_dataset("PETime", data=pe_time_truth, maxshape=(None,))

    else:   # Insert new data to the data set
        
        dset0.resize(dset0.shape[0]+ch_entry, axis=0)
        dset1.resize(dset1.shape[0]+ch_entry, axis=0)
        dset2.resize(dset2.shape[0]+ch_entry, axis=0)
        dset3.resize(dset3.shape[0]+ch_entry, axis=0)
        dset0[-ch_evtid.shape[0]:] = ch_evtid
        dset1[-ch_id.shape[0]:] = ch_id
        dset2[-ch_sec.shape[0]:] = ch_sec
        dset3[-ch_nsec.shape[0]:] = ch_nsec
        dset4[-ch_wav.shape[0]:] = ch_wav

        dset5.resize(dset6.shape[0]+nTriggerTruth, axis=0)
        dset6.resize(dset7.shape[0]+nTriggerTruth, axis=0)
        dset7.resize(dset8.shape[0]+nTriggerTruth, axis=0)
        dset5[-pe_evtid_truth.shape[0]:] = pe_evtid_truth
        dset6[-pe_pmtid_truth.shape[0]:] = pe_pmtid_truth
        dset7[-pe_time_truth.shape[0]:] = pe_time_truth
    
    FileNo = FileNo+1

f.close()
