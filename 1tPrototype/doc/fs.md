## 文件格式

我们将数据储存在[HDF5](https://www.hdfgroup.org/)文件中，文件中有一个名为OneTonDetector的group，其中有三个表：TriggerInfo保存触发的时间戳信息；Waveform保存波形信息；GroundTruth保存每个光子的击中时间，即标签信息。每个表都有对应的事例编号或通道编号，如下所示。
<center>
<table cellspacing="0" border="0"><colgroup width="180"></colgroup><colgroup width="180"></colgroup><colgroup width="180"></colgroup><tr><td style="border-bottom: 2px solid #000000" colspan=3 height="19" align="center" valign=middle><b><i><font color="#000000">OneTonDetector/TriggerInfo</font></i></b></td></tr><tr><td style="border-top: 2px solid #000000" height="18" align="center" valign=middle><b><font color="#000000">EventID</font></b> (int64)</td><td style="border-top: 2px solid #000000" align="center" valign=middle><b><font color="#000000">Sec</font></b> (int32)</td><td style="border-top: 2px solid #000000" align="center" valign=middle><b><font color="#000000">NanoSec</font></b> (int32)</td></tr><tr><td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td><td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td><td align="center" valign=middle sdval="89692193" sdnum="1033;"><font color="#000000">89692193</font></td></tr><tr><td height="18" align="center" valign=middle sdval="2" sdnum="1033;"><font color="#000000">2</font></td><td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td><td align="center" valign=middle sdval="109000153" sdnum="1033;"><font color="#000000">109000153</font></td></tr><tr><td height="18" align="center" valign=middle sdval="3" sdnum="1033;"><font color="#000000">3</font></td><td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td><td align="center" valign=middle sdval="201205243" sdnum="1033;"><font color="#000000">201205243</font></td></tr><tr><td height="18" align="center" valign=middle><font color="#000000">…</font></td><td align="center" valign=middle><font color="#000000">…</font></td><td align="center" valign=middle><font color="#000000">…</font></td></tr></table>

<table cellspacing="0" border="0">	<colgroup width="180"></colgroup>	<colgroup width="200"></colgroup>	<colgroup width="250"></colgroup>	<tr>		<td style="border-bottom: 2px solid #000000" colspan=3 height="19" align="center" valign=middle><b><i><font color="#000000">OneTonDetector/Waveform</font></i></b></td>		</tr>	<tr>		<td height="18" align="center" valign=middle><b><font color="#000000">EventID</font></b> (int64)</td>		<td align="center" valign=middle><b><font color="#000000">ChannelID</font></b> (int16)</td>		<td align="center" valign=middle><b><font color="#000000">Waveform</font></b> (int16 [1029])</td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">974, 973, …, 972</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle><font color="#000000">973, 974, …, 975</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="2" sdnum="1033;"><font color="#000000">2</font></td>		<td align="center" valign=middle><font color="#000000">973, 973, …, 974</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>	</tr></table>

<table cellspacing="0" border="0">	<colgroup width="180"></colgroup>	<colgroup width="200"></colgroup>	<colgroup width="180"></colgroup>	<tr>		<td style="border-bottom: 2px solid #000000" colspan=3 height="19" align="center" valign=middle><b><i><font color="#000000">OneTonDetector/GroundTruth</font></i></b></td>		</tr>	<tr>		<td height="18" align="center" valign=middle><b><font color="#000000">EventID</font></b> (int64)</td>		<td align="center" valign=middle><b><font color="#000000">ChannelID</font></b> (int16)</td>		<td align="center" valign=middle><b><font color="#000000">PETime</font></b> (int16)</td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">269</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">284</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="2" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">287</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>	</tr></table>

</center>

使用[HDFView](https://www.hdfgroup.org/downloads/hdfview/)打开数据文件，可以查看文件的大致结构

<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/hdfview.png" width = "100%" alt="数据文件的结构"/><br/>
数据文件的结构
</div>

## 读取文件的示例

### Python

利用Python的`pytables`模块，我们可以方便地读取hdf5文件。

```python
import tables
import matplotlib
import matplotlib.pyplot as plt

# Read hdf5 file
filename = "test.h5"
h5file = tables.open_file(filename, "r")

WaveformTable = h5file.root.OneTonDetector.Waveform
entry = 0
EventId = WaveformTable[entry]['EventID']
ChannelId = WaveformTable[entry]['ChannelID']
Waveform = WaveformTable[entry]['Waveform']
minpoint = min(Waveform)
maxpoint = max(Waveform)

GroundTruthTable = h5file.root.OneTonDetector.GroundTruth
PETime = [x['PETime'] for x in GroundTruthTable.iterrows() if x['EventID'] == EventId and x['ChannelID']==ChannelId]
print(PETime)

plt.plot(Waveform)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [ADC]')
for time in PETime:
    plt.vlines(time, minpoint, maxpoint, 'r')

plt.title("Entry %d, Event %d, Channel %d" % (entry, EventId, ChannelId))
plt.show()

h5file.close()
```
这段程序将Waveform表中的第一个记录读取，并在GroundTruth表中取出对应的光电子到达时间，将其画出。得到的图像为

<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/Figure_1.png" width = "60%" alt="读出波形"/><br/>
波形和击中时间的示例图
</div>

<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/Figure_2.png" width = "60%" alt="读出波形"/><br/>
波形局部放大
</div>

可以看出该PMT上有3次击中，其中后两次离得较近，两个波形叠加得到一个较大、较宽的波形。

### C++
HDF5原生库提供了C/C++的支持。安装后指定头文件目录和库即可编译下面的示例代码
```
g++ -std=c++11 -o test -I/usr/local/hdf5/include/ ReadExample.cpp -lhdf5 -lhdf5_hl
```
```cpp
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
```
这段程序读取了Waveform表中的第一条记录，并把波形数值打印了出来。