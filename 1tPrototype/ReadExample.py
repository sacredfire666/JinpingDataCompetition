import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Read hdf5 file
filename = 'data/Run669.h5'
chdf = pd.read_hdf(filename, 'ChannelID')
wavdf = pd.read_hdf(filename, 'Waveform')

# Print the fired PMTs in the EventID=1 event
evtid = 1
print(chdf.loc[evtid])

# Plot the waveform of #2 PMT
pmtid = 2
rowFinder = chdf.loc[evtid].isin([pmtid])
row = np.flatnonzero(rowFinder)
waveform = wavdf.loc[evtid].iloc[row[0]]
plt.plot(waveform)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [ADC]')
plt.savefig("example.png")

# Calculate pedestal
ped = np.mean(wavdf.iloc[:,0:150], axis=1)
peddf = pd.DataFrame({'ChannelID': chdf, 'Pedestal': ped})
print(peddf)