## 256x2568
outputnet=ConvNet__2014-11-03_13.07.36 # AO+FB

## alex networks
#python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.join.sq.256-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.join.sq.256-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-joiniris.256.cfg --layer-params=./example-layers/layer-params-conv-local-joiniris.256.cfg --data-provider=biometrika-cropped --img-size=256 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=100

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.join.sq.256-py/${outputnet} --train-range=1-4 --epochs=140

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --epochs=150

# Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.MobBIOfake.sq.256-py/${outputnet} --epochs=160

python convnet.py -f /home/LIV/axf/shared/results/iris.printed.join.sq.256-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5
python convnet.py -f /home/LIV/axf/shared/results/iris.printed.join.sq.256-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=6
python convnet.py -f /home/LIV/axf/shared/results/iris.printed.join.sq.256-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=7
python convnet.py -f /home/LIV/axf/shared/results/iris.printed.join.sq.256-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=8
