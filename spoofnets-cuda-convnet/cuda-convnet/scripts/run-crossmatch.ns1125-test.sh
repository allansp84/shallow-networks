#outputnet=ConvNet__2014-11-05_00.04.35 # 128x128
#outputnet=ConvNet__2014-11-11_01.48.33 # 32x32
#outputnet=ConvNet__2014-11-11_17.16.29 # 128x128 - 98.32
#outputnet=ConvNet__2015-01-16_17.33.44 # 128x128 - 98.32
outputnet=ConvNet__2015-01-19_15.31.42 # 128x128 - 98.32



#python convnet.py --data-path=/home/LIV/axf/shared/datasets/fg.ld13.crossmatch.ns1125-py/ --save-path=/home/LIV/axf/shared/results/fg.ld13.crossmatch.ns1125-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-crossmatch.0.cfg --layer-params=./example-layers/layer-params-conv-local-crossmatch.0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=400

#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns1125-py/${outputnet} --train-range=1-4 --epochs=560

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns1125-py/${outputnet} --epochs=600

## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns1125-py/${outputnet} --epochs=640

#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.crossmatch.ns1125-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5

