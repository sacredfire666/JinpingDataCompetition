# Dependency: JSAP, python3, scipy, h5py.
# ConvertTruth.py is for simulations.
# Convert.py is for real data.

.PHONY: first
mul=$(shell seq 0 9)

first: first-problem.h5 $(mul:%=ftraining-%.h5)

first.mac: first.mac.in
	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
$(mul:%=ftraining-%.mac): %: first.mac.in
	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@

%.root: %.mac
	JPSim -g 1t -m $^ -o ../$@ > $@.log 2>&1
%.h5: %.root
	python3 1tPrototype/ConvertTruth.py $^ $@ > $@.log 2>&1

%-problem.h5: %.h5
	cp $^ $@
	python3 -c 'import h5py; del h5py.File("$@")["GroundTruth"]'
%-submission.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@
%-submission-2.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@
%-submission-3.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@

# Delete partial files when the processes are killed.
.DELETE_ON_ERROR:
# Keep intermediate files around
.SECONDARY:
