#锦屏中微子实验一吨原型机介绍

## 探测器

为了研究大型中微子实验所用到的液体闪烁体技术和低本底技术，我们在锦屏地下实验室中建造了一个小型原型机。其的核心部件包括1吨液体闪烁体和30个光电倍增管（PMT）。粒子在液体闪烁体中沉积能量，光电倍增管会将闪烁体发出的光信号转化为电信号读出，通过分析这30个光电倍增管上的电压波形，我们就可以得到原初粒子的能量、位置等信息，进而进行相关的物理分析。

![detector.png](.\detector.png)
<center>锦屏中微子实验一吨原型机结构示意图</center>

探测器每次运行被称为一个Run，每个Run中都包含了很多个触发事例，被称为Event。我们记录下来的主要信息就是每个事例的触发时间戳，以及30个PMT（编号从0到29）上的波形。值得注意的是，并不是每个事例都会触发全部30个PMT，我们将触发阈值设为25个PMT，即大于或等于25个PMT同时接收到光信号时才将事例记录下来，也只记录有触发的PMT上的波形。记录波形的长度（即时间窗）为1029ns，时间分辨为1ns，因此每个PMT上的波形被记录为一个长度为1029的数组。波形在每个时间点上的电压由10位ADC转化成数字信号，取值为0到1023。

数据分析的基本任务就是从这些波形的数组中挖掘出相关的物理目标。

## 数据格式

目前我们将数据记录为pandas的DataFrame对象（其中ChannelID字段是Series对象）并存储在HDf5文件中进行数据的分享。数据的格式如下表所示，

| EventID | Sec | NanoSec | ChannelID | Waveform|
|--------|--------|--------|--------|--------|
|   1     |    1507012212    |   763742685     |     [0,<br />2,<br />...,<br />29]   |  [[968, 967, ..., 967],<br />[957, 969, ..., 967],<br />...,<br />[967, 969, ..., 968]]      |
|   2     |    1507012212    |   778829336     |     [0,<br />1,<br />...,<br />28]   |  [[965, 964, ..., 961],<br />[958, 969, ..., 967],<br />...,<br />[967, 954, ..., 962]]      |
|   ...     |    ...    |   ...     |     ...   | ...      |

其中EventID、Sec、NanoSec字段放在名为TriggerInfo的group中，ChannelID字段和Waveform字段各自成group。ChannelID是一个长度为n的向量，记录了该事例中触发的n个PMT的编号；Waveform是一个n×m大小的矩阵，记录这n个PMT的波形，其中m为时间窗的大小。例如从上表的数据可以读出，EventID为1的这个事例中，2号PMT被触发，其波形是[957, 969, ..., 967]。

为了检索方便，我们把这些DataFrame的index都设为EventID。

一些读取文件的示例代码如下
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
![example.png](.\example.png)

