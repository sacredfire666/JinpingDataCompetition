#锦屏中微子实验一吨原型机介绍

## 探测器

为了研究大型中微子实验所用到的液体闪烁体技术和低本底技术，我们在锦屏地下实验室中建造了一个小型原型机。其的核心部件包括1吨液体闪烁体和30个光电倍增管（PMT）。粒子在液体闪烁体中沉积能量，光电倍增管会将闪烁体发出的光信号转化为电信号读出，通过分析这30个光电倍增管上的电压波形，我们就可以得到原初粒子的能量、位置等信息，进而进行相关的物理分析。

<center>
![detector.png](.\detector.png)
锦屏中微子实验一吨原型机结构示意图
</center>

探测器每次运行被称为一个run，每个run中都包含了很多个触发事例，被称为event。我们记录下来的主要信息就是每个事例的触发时间戳，以及30个PMT（编号从0到29）上的波形。值得注意的是，并不是每个事例都会触发全部30个PMT，我们将触发阈值设为25个PMT，即大于或等于25个PMT同时接收到光信号时才将事例记录下来，也只记录有触发的PMT上的波形。记录波形的长度（即时间窗）为1029ns，时间分辨为1ns，因此每个PMT上的波形被记录为一个长度为1029的数组。波形在每个时间点上的电压由10位ADC转化成数字信号，取值为0到1023。

数据分析的基本任务就是从这些波形的数组中挖掘出相关的物理目标。

## 数据格式

目前我们将数据储存在HDF5文件中，其中有两个group：
- TriggerInfo，有三个dataset：EventID、Sec和NanoSec组保存了该事例的编号和时间戳，未来还会加上蒙特卡洛模拟的truth信息作为数据的label。
- Waveform，有三个dataset：EventID、ChannelID和Wavform。EventID可以和TriggerInfo组中的数据匹配，ChannelID记录了触发的PMT编号（不一定是30个），Waveform记录了该PMT上的波形，是一个长度为1029的数组。

数据的格式如下表所示，例如可以从表中的数据可以读出，EventID为1的这个事例的时间戳是(1507012212s, 763742685ns)，0号PMT被触发，其波形是[968, 967, ..., 967]。

<center>
<table cellspacing="0" border="0"><tr align="center" valign=middle><td style="border-right: 3px solid" colspan=3><b><i>TriggerInfo</i></b></td><td colspan=3><b><i>Waveform</i></b></td></tr><tr align="center" valign=middle><td style="border-bottom: 2px solid"><b>EventID</b></td><td style="border-bottom: 2px solid"><b>Sec</b></td><td style="border-right: 3px solid;border-bottom: 2px solid"><b>NanoSec</b></td><td style="border-bottom: 2px solid"><b>EventID</b></td><td style="border-bottom: 2px solid"><b>ChannelID</b></td><td style="border-bottom: 2px solid"><b>Waveform</b></td></tr><tr align="center" valign=middle><td rowspan=4 style="border-bottom: 1px solid">1</td><td rowspan=4 style="border-bottom: 1px solid">1507012212</td><td style="border-right: 3px solid; border-bottom: 1px solid" rowspan=4>763742685</td><td>1</td><td>0</td><td>[968, 967, …, 967]</td></tr><tr align="center" valign=middle><td>1</td><td>1</td><td>[957, 969, …, 967]</td></tr><tr align="center" valign=middle><td>…</td><td>…</td><td>…</td></tr><tr align="center" valign=middle><td style="border-bottom: 1px solid">1</td><td style="border-bottom: 1px solid">29</td><td style="border-bottom: 1px solid">[967, 969, …, 968]</td></tr><tr align="center" valign=middle><td rowspan=4 style="border-bottom: 1px solid">2</td><td rowspan=4 style="border-bottom: 1px solid">1507012212</td><td style="border-right: 3px solid; border-bottom: 1px solid" rowspan=4>778829336</td><td>2</td><td>1</td><td>[968, 967, …, 967]</td></tr><tr align="center" valign=middle><td>2</td><td>3</td><td>[957, 969, …, 967]</td>	</tr><tr align="center" valign=middle><td>…</td><td>…</td><td>…</td></tr><tr align="center" valign=middle><td style="border-bottom: 1px solid">2</td><td style="border-bottom: 1px solid">28</td><td style="border-bottom: 1px solid">[967, 969, …, 968]</td></tr><tr align="center" valign=middle><td>…</td><td>…</td><td style="border-right: 3px solid">…</td><td>…</td><td>…</td><td>…</td></tr></table>
</center>

利用python的pandas来读取数据的示例如下
```
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

filename = 'data/Run669.h5'
chdf = pd.read_hdf(filename, 'ChannelID')
wavdf = pd.read_hdf(filename, 'Waveform')

# 查看第1个事例中有哪些PMT被击中
evtid = 1
print(chdf.loc[evtid])

# 查看这个事例中2号PMT的波形
pmtid = 2
rowFinder = chdf.loc[evtid].isin([pmtid])
row = np.flatnonzero(rowFinder)
waveform = wavdf.loc[evtid].iloc[row[0]]
plt.plot(waveform)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [ADC]')
plt.savefig("example.png")

# 计算该Run中所有波形的基线
ped = np.mean(wavdf.iloc[:,0:150], axis=1)
peddf = pd.DataFrame({'ChannelID': chdf, 'Pedestal': ped})
print(peddf)
```
生成的example.png如下图所示
<center>
![example.png](.\example.png)
</center>

利用C++读取数据的示例如下。这里使用了HighFive库（ https://github.com/BlueBrain/HighFive ）作为读取HDF5文件的interface，大家也可以使用其他自己熟悉的库。
```
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

```
