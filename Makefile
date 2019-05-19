# Dependency: JSAP, python3, scipy, h5py.
# ConvertTruth.py is for simulations.
# Convert.py is for real data.

.PHONY: first zinc
mul=$(shell seq 0 9)

zinc: zinc-ans.h5 zinc-problem.h5 $(mul:%=ztraining-%.h5)
first: first-problem.h5 $(mul:%=ftraining-%.h5)

$(mul:%=ftraining-%.mac): %: first.mac.in
	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
$(mul:%=ztraining-%.mac): %: zinc.mac.in
	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
%.mac: %.mac.in
	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@

%.root: %.mac
	JPSim -g 1t -m $^ -o ../$@ > $@.log 2>&1
%.h5: %.root
	sem --fg python3 1tPrototype/ConvertTruth.py $^ $@ > $@.log 2>&1

zreal.h5: /home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run00000893/Jinping_1ton_Phy_20180722_00000893.root
	python3 1tPrototype/Converter.py 893 --limit 2 -o $@

zexample.h5: /home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run00000896/Jinping_1ton_Phy_20180723_00000896.root
	python3 1tPrototype/Converter.py 896 --limit 4 -o $@
zincm-problem.h5: zinc-problem zreal.h5
	mix.py

%-problem.h5: %.h5
	cp $^ $@
	python3 -c 'import h5py; del h5py.File("$@")["GroundTruth"]'
	h5repack -i $@ -o $@-tmp
	mv -f $@-tmp $@
%-ans.h5: %.h5
	cp $^ $@
	python3 -c 'import h5py; del h5py.File("$@")["Waveform"]'
	h5repack -i $@ -o $@-tmp
	mv -f $@-tmp $@
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
