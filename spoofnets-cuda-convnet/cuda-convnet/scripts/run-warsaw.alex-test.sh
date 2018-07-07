#outputnet=ConvNet__2014-11-05_10.03.03 #- AO+FB 128x128
outputnet=ConvNet__2014-11-10_23.55.32 #- AO+FB 32x32


#python convnet.py --data-path=/home/LIV/axf/shared/datasets/iris.printed.Warsaw.sq.32-py/ --save-path=/home/LIV/axf/shared/results/iris.printed.Warsaw.sq.32-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-warsaw.alex.cfg --layer-params=./example-layers/layer-params-conv-local-warsaw.alex.cfg --data-provider=biometrika-cropped --img-size=32 --num-colors=1 --crop-border=4 --test-freq=13 --epochs=100

#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.Warsaw.sq.32-py/${outputnet} --train-range=1-4 --epochs=140

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/iris.printed.Warsaw.sq.32-py/${outputnet} --epochs=150

# Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
python convnet.py -f /home/LIV/axf/shared/results/iris.printed.Warsaw.sq.32-py/${outputnet} --epochs=160

python convnet.py -f /home/LIV/axf/shared/results/iris.printed.Warsaw.sq.32-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5
