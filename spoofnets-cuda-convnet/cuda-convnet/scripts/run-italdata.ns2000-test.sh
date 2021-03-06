#outputnet=ConvNet__2014-11-05_00.39.25 #    99.95% - AA+FB
outputnet=ConvNet__2015-01-15_19.06.00 #    99.95% - AA+FB


#python convnet.py --data-path=/home/LIV/axf/shared/datasets/fg.ld13.italdata.ns2000-py/ --save-path=/home/LIV/axf/shared/results/fg.ld13.italdata.ns2000-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-italdata.0.cfg --layer-params=./example-layers/layer-params-conv-local-italdata.0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=200

python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.italdata.ns2000-py/${outputnet} --train-range=1-4 --epochs=280

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.italdata.ns2000-py/${outputnet} --epochs=300

## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.italdata.ns2000-py/${outputnet} --epochs=320

python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.italdata.ns2000-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5

