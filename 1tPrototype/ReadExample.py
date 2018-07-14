import pandas as pd
import numpy as np
import h5py
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Read hdf5 file
filename = "data/Run669.h5"
f = h5py.File(filename,"r")
evtid = f["Waveform/EventID"][:]
chlid = f["Waveform/ChannelID"][:]
wav = f["Waveform/Waveform"][:]
wav = np.column_stack((chlid,wav))

column_name = ["ChannelID"]
for i in range(1029):
    column_name.append("Tick%d"%i)

# Create a DataFrame. EventID is the index.
wavdf = pd.DataFrame(wav, columns=column_name, index=evtid)

# Print the fired PMTs in the EventID=1 event
eid = 1
print(wavdf.loc[eid]["ChannelID"])

# Plot the waveform of #2 PMT
wav_e1p2 = wavdf.loc[eid].query("ChannelID==2")
wav_e1p2 = wav_e1p2.iloc[0].values[1:]
plt.plot(wav_e1p2)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [ADC]')
plt.savefig("example.png")

# Calculate the pedestal
ped = np.mean(wavdf.iloc[:,1:150], axis=1)
peddf = pd.DataFrame({'ChannelID': chlid, 'Pedestal': ped})
print(peddf)

f.close()