# outputnet=ConvNet__2014-10-29_00.15.53 # AA+FB
outputnet=ConvNet__2014-10-30_18.16.17 # AO+FB


## without normalization
#python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.MobBIOfake.sq.128-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-biometrika0.cfg --layer-params=./example-layers/layer-params-conv-local-biometrika0.cfg --data-provider=biometrika-cropped --crop-border=16 --test-freq=13 --epochs=100

### with normalization
#python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.MobBIOfake.sq.128-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.128-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-mobbiofake0.cfg --layer-params=./example-layers/layer-params-conv-local-mobbiofake0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=3 --crop-border=8 --test-freq=13 --epochs=200

## optimal architecture
#python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.MobBIOfake.sq.256-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-mobbiofake.opt.cfg --layer-params=./example-layers/layer-params-conv-local-mobbiofake.opt.cfg --data-provider=biometrika-cropped --img-size=256 --num-colors=3 --crop-border=16 --test-freq=13 --epochs=100


#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --train-range=1-4 --epochs=140

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --epochs=150

# Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --epochs=160

python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5
