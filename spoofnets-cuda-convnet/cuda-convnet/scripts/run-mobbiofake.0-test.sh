#outputnet=ConvNet__2014-11-04_16.14.16 # AO+FB
outputnet=ConvNet__2014-11-11_18.51.08 #128x128 color - 100%

python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.MobBIOfake.sq.128.3-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.3-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-mobbiofake.0.cfg --layer-params=./example-layers/layer-params-conv-local-mobbiofake.0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=3 --crop-border=8 --test-freq=13 --epochs=200

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.3-py/${outputnet} --train-range=1-4 --epochs=280

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.3-py/${outputnet} --epochs=300

## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.3-py/${outputnet} --epochs=320

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.3-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5
