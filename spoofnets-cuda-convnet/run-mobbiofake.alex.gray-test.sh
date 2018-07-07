outputnet=ConvNet__2014-11-07_23.14.04 # 91.25 - 100/140/150/160
outputnet=ConvNet__2014-11-07_23.14.04 # 300/420/450/480

python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.MobBIOfake.sq.128.1-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.1-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-mobbiofake.alex.cfg --layer-params=./example-layers/layer-params-conv-local-mobbiofake.alex.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=300

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.1-py/${outputnet} --train-range=1-4 --epochs=420

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.1-py/${outputnet} --epochs=450

## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.1-py/${outputnet} --epochs=480

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128.1-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5
