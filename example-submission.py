#!/usr/bin/env python3
# generate example submission
#

import h5py, numpy as np, argparse
from numpy.lib.recfunctions import append_fields

psr = argparse.ArgumentParser()
psr.add_argument("-o", dest='opt', help="output")
psr.add_argument('ipt', help="input")
args = psr.parse_args()

with h5py.File(args.ipt) as ipt:
    ans = ipt["GroundTruth"][:]
    N = len(ans["PETime"])
    ans["PETime"] += np.random.randint(-50, 50, N)
    ans = append_fields(ans, "Weight", np.ones(N, dtype=np.float32))
    ipt["Answer"] = ans
    del ipt["GroundTruth"], ipt["Waveform"], ipt["TriggerInfo"]

