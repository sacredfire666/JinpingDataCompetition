# Dependency: JSAP, python3, scipy, h5py.
# ConvertTruth.py is for simulations.
# Convert.py is for real data.

%.root: %.mac
	JPSim -g 1t -m $^ -o ../$@ > $@.log 2>&1
%.h5: %.root
	python3 1tPrototype/ConvertTruth.py $^ $@ > $@.log 2>&1

# Delete partial files when the processes are killed.
.DELETE_ON_ERROR:
# Keep intermediate files around
.SECONDARY:
