## 问题背景

### 锦屏中微子实验

中国锦屏地下实验室（China Jinping Underground Laboratory， CJPL）位于四川省雅砻江锦屏山的深处，是中国首个用于开展暗物质探测等国际前沿基础研究课题的极深地下实验室，于2010年12月12日正式投入使用。目前，[CDEX](https://en.wikipedia.org/wiki/China_Dark_Matter_Experiment)、[PandaX](https://en.wikipedia.org/wiki/PandaX)等暗物质实验在这里进行，这些实验的研究水平已达到国际第一阵营。不仅仅是暗物质实验，未来的[锦屏中微子实验](http://jinping.hep.tsinghua.edu.cn/)也会在中国锦屏地下实验室开展，在太阳中微子、地球中微子、超新星遗迹中微子等学科前沿方面进行研究。

为了研究锦屏中微子实验所用到的液体闪烁体和低本底技术，我们在锦屏地下实验室中建造了一个小型原型机。其核心部件包括1吨液体闪烁体和30个光电倍增管（PMT）。高速运动的微观粒子在液体闪烁体中沉积能量，闪烁体会发出荧光，光电倍增管会将这些光信号转化为电信号输出。通过分析这30个光电倍增管上的电压波形，我们就可以得到原初粒子的能量、位置等信息，进而进行相关的物理分析。

更多的物理背景可以查看补充材料[幽灵粒子的前世今生](https://ghost-hunter-contest.github.io/)。

<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/detector.png" width = "80%" alt="锦屏中微子实验一吨原型机结构示意图"/><br/>
锦屏中微子实验一吨原型机结构示意图
</div>

探测器每次运行被称为一个run，每个run中都包含了很多个触发事例（event）。我们记录下来的主要信息就是每个事例的触发时间戳，以及30个PMT（编号从通道0到通道29）上的波形。

### 光电倍增管与输出
光电倍增管（PMT）是一种特殊的真空管仪器，它利用光电效应将微弱的光信号转化为电子信号（被称为光电子photoelectron, PE），并将其放大10<sup>7</sup>到10<sup>8</sup>倍，使光信号能被测量。

<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/PMT.png" width = "30%" alt="日本滨松于20世纪80年代开发出的直径为20英寸的光电倍增管"/><br/>
日本滨松于20世纪80年代开发出的直径为20英寸的光电倍增管。这项发明在2014年被认定为[IEEE里程碑](http://ieeemilestones.ethw.org/Main_Page)之一。
</div>

光电倍增管被光子击中并产生光电子后，经过多级倍增，会产生一个近似对数高斯形状的脉冲输出。一个典型的波形如图所示，
<div align=center>
<img src="https://raw.githubusercontent.com/sacredfire666/JinpingDataCompetition/master/1tPrototype/doc/waveform.png" width = "50%" alt="单光电子波形"/><br/>
一个典型的单光电子脉冲波形。这个波形中没有加入噪声。
</div>

不同光电子产生的波形形状相似，但幅度大小有涨落。光电倍增管输出的波形是一个模拟信号，我们通过[flash ADC](https://en.wikipedia.org/wiki/Flash_ADC)将这个模拟信号转化为数字信号。该flash ADC的时间精度为1ns，ADC为10位，动态范围为1V，因此电压精度约为1mV。记录数据的时间窗口大小为1029ns，最终每个PMT的波形数据是一个长度为1029，元素取值为0~1023的数组。本次数据竞赛的目的是通过波形数据找到单光电子击中的时间。

### 蒙特卡罗方法

本次竞赛的数据集来自[蒙特卡罗方法](https://en.wikipedia.org/wiki/Monte_Carlo_method)的模拟数据。我们可以通过计算机模拟粒子在探测器内的运动行为，以及探测器的电子学输出，得到与实际数据格式相同的模拟数据。与实际数据相比，模拟数据中包含了初始粒子以及PMT接收到的光电子的详细信息，并可以将其作为数据的标签，用于研究探测器的响应和分析算法的表现。