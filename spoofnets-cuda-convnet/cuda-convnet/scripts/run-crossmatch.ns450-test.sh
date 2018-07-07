#outputnet=ConvNet__2014-11-05_00.04.35 # 128x128
#outputnet=ConvNet__2014-11-11_01.48.33 # 32x32
#outputnet=ConvNet__2014-11-11_17.16.29 # 128x128 - 98.32
#outputnet=ConvNet__2015-01-16_17.35.45 # 128x128 - 98.32
outputnet=ConvNet__2015-01-19_15.30.53 # 128x128 - 98.32



#python convnet.py --data-path=/home/LIV/axf/shared/datasets/fg.ld13.crossmatch.ns450-py/ --save-path=/home/LIV/axf/shared/results/fg.ld13.crossmatch.ns450-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-crossmatch.0.cfg --layer-params=./example-layers/layer-params-conv-local-crossmatch.0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=1000

#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns450-py/${outputnet} --train-range=1-4 --epochs=1400

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns450-py/${outputnet} --epochs=1500

## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns450-py/${outputnet} --epochs=1600

#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns450-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5

