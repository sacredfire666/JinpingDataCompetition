#include "hdf5.h"
#include "hdf5_hl.h"
#include <stdlib.h>
#include <iostream>
using namespace std;

constexpr size_t nWindowSize = 1029;
constexpr size_t nFields = 3;

struct WaveformData
{
    long long EventID;
    short   ChannelID;
    short   Waveform[nWindowSize];
};

int main()
{
    WaveformData wf_buf;

    /* Calculate the size and the offsets of our struct members in memory */
    size_t dst_size =  sizeof(WaveformData);
    size_t dst_offset[nFields] = { HOFFSET( WaveformData, EventID ),
        HOFFSET( WaveformData, ChannelID ),
        HOFFSET( WaveformData, Waveform )
    };
    size_t dst_sizes[nFields] = { sizeof(wf_buf.EventID), 
        sizeof(wf_buf.ChannelID), 
        sizeof(wf_buf.Waveform)
    };
    
    hid_t file_id = H5Fopen( "test.h5", H5F_ACC_RDONLY,  H5P_DEFAULT);
    hid_t group_id = H5Gopen(file_id, "OneTonDetector", H5P_DEFAULT);
    H5TBread_records( group_id, "Waveform", 0, 1, dst_size, dst_offset, dst_sizes, &wf_buf);
    for(int i=0; i<nWindowSize; i++)
        cout<<wf_buf.Waveform[i]<<", ";
    cout<<endl;

    H5Fclose( file_id );
    return 0;
}

