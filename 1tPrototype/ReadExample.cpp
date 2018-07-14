#include <iostream>
#include <string>
#include <vector>
#include <highfive/H5File.hpp>
#include <highfive/H5DataSet.hpp>
#include <highfive/H5DataSpace.hpp>
using namespace HighFive;

void read_dataset() {
    // Open the existing hdf5 file
    File file("data/Run669.h5", File::ReadOnly);

    std::vector<int> evtid;
    std::vector<int> channelid;
    std::vector<std::vector<int> > waveform;

    // Get the dataset
    DataSet evtid_dset = file.getDataSet("Waveform/EventID");
    DataSet channelid_dset = file.getDataSet("Waveform/ChannelID");
    DataSet waveform_dset = file.getDataSet("Waveform/Waveform");

    // Convert the waveform data to containers
    evtid_dset.read(evtid);
    channelid_dset.read(channelid);
    waveform_dset.read(waveform);

    // Print the waveform of Event#1 PMT#2
    for(size_t i=0; i<evtid.size(); i++)
    {
        if(evtid[i]==1 && channelid[i]==2)
        {
            for(auto&& v : waveform[i])
                std::cout<<v<<std::endl;
            break;
        }
    }
}

int main(void) {
    try {
        read_dataset();
    } catch (Exception& err) {
        // catch and print any HDF5 error
        std::cerr << err.what() << std::endl;
    }
    return 0; // successfully terminated
}