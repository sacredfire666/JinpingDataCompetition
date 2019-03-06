## 提交格式

选手提交HDF5格式的文件，在文件中写入一个与数据集中GroundTruth表结构相同的表，并命名为为Answer

<table cellspacing="0" border="0">	<colgroup width="180"></colgroup>	<colgroup width="200"></colgroup>	<colgroup width="180"></colgroup>	<tr>		<td style="border-bottom: 2px solid #000000" colspan=3 height="19" align="center" valign=middle><b><i><font color="#000000">Answer</font></i></b></td>		</tr>	<tr>		<td height="18" align="center" valign=middle><b><font color="#000000">EventID</font></b> (int64)</td>		<td align="center" valign=middle><b><font color="#000000">ChannelID</font></b> (int16)</td>		<td align="center" valign=middle><b><font color="#000000">PETime</font></b> (int16)</td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="0" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">269</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">284</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle sdval="1" sdnum="1033;"><font color="#000000">1</font></td>		<td align="center" valign=middle sdval="2" sdnum="1033;"><font color="#000000">0</font></td>		<td align="center" valign=middle><font color="#000000">287</font></td>	</tr>	<tr>		<td height="18" align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>		<td align="center" valign=middle><font color="#000000">…</font></td>	</tr></table>

## 写入文件的示例

在下面的示例中，我们向文件中写入上表中的三条示例数据。

### Python
```python
# An example of writing a file.
import tables

# Define the database columns
class AnswerData(tables.IsDescription):
    EventID    = tables.Int64Col(pos=0)
    ChannelID  = tables.Int16Col(pos=1)
    PETime     = tables.Int16Col(pos=2)

# Create the output file and the group
h5file = tables.open_file("MyAnswer.h5", mode="w", title="OneTonDetector")

# Create tables
AnswerTable = h5file.create_table("/", "Answer", AnswerData, "Answer")
answer = AnswerTable.row

# Write data 
answer['EventID'] =  1
answer['ChannelID'] = 0
answer['PETime'] = 269 
answer.append()
answer['EventID'] =  1
answer['ChannelID'] = 0
answer['PETime'] = 284 
answer.append()
answer['EventID'] =  1
answer['ChannelID'] = 0
answer['PETime'] = 287 
answer.append()

# Flush into the output file
AnswerTable.flush()

h5file.close()
```

### C++
```
g++ -std=c++11 -o submit -I/usr/local/hdf5/include/ Submit.cpp -lhdf5 -lhdf5_hl
```

```cpp
#include "hdf5.h"
#include "hdf5_hl.h"
#include <stdlib.h>
#include <iostream>
using namespace std;

constexpr size_t nFields = 3;
constexpr size_t nRecord = 3;

struct AnswerData
{
    long long EventID;
    short   ChannelID;
    short   PETime;
};

int main( void )
{

    AnswerData dst_buf;

    // Calculate the size and the offsets of our struct members in memory
    size_t dst_size =  sizeof( AnswerData );
    size_t dst_offset[nFields] = { HOFFSET( AnswerData, EventID ),
        HOFFSET( AnswerData, ChannelID ),
        HOFFSET( AnswerData, PETime )
    };

    size_t dst_sizes[nFields] = { sizeof( dst_buf.EventID),
        sizeof( dst_buf.ChannelID),
        sizeof( dst_buf.PETime)
    };

    // Define an array of data
    AnswerData p_data[nRecord] = {
        {1,0, 269},
        {1,0, 284},
        {1,0, 287}
    };

    // Define field information
    const char *field_names[nFields]  =
    { "EventID","ChannelID", "PETime"};
    hid_t      field_type[nFields];
    hid_t      file_id;
    hsize_t    chunk_size = 10;
    int        *fill_data = NULL;
    int        compress  = 0;
    int        i;

    // Initialize field_type
    field_type[0] = H5T_NATIVE_LLONG;
    field_type[1] = H5T_NATIVE_SHORT;
    field_type[2] = H5T_NATIVE_SHORT;

    // Create a new file using default properties.
    file_id = H5Fcreate( "MyAnswer_cpp.h5", H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT );


    // Make the table.
    H5TBmake_table( "Table Title", file_id, "Answer", nFields, nRecord,
                dst_size,field_names, dst_offset, field_type,
                chunk_size, fill_data, compress, p_data  );

    // Close the file.
    H5Fclose( file_id );

    return 0;
}
```