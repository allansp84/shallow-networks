#outputnet=ConvNet__2014-11-11_17.50.23
#outputnet=ConvNet__2015-01-17_16.08.58
outputnet=ConvNet__2015-01-19_15.07.53



#python convnet.py --data-path=/home/LIV/axf/shared/datasets/fg.ld13.swipe.crop.ns440-py/ --save-path=/home/LIV/axf/shared/results/fg.ld13.swipe.crop.ns440-py --test-range=4 --train-range=1-3 --layer-def=./example-layers/layers-conv-local-swipe.0.cfg --layer-params=./example-layers/layer-params-conv-local-swipe.0.cfg --data-provider=biometrika-cropped --img-size=128 --num-colors=1 --crop-border=8 --test-freq=13 --epochs=1000

#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.swipe.crop.ns440-py/${outputnet} --train-range=1-4 --epochs=1400

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.swipe.crop.ns440-py/${outputnet} --epochs=1500

# Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.swipe.crop.ns440-py/${outputnet} --epochs=1600

python convnet.py -f /home/LIV/axf/shared/results/fg.ld13.swipe.crop.ns440-py/${outputnet} --multiview-test=1 --test-only=1 --logreg-name=logprob --test-range=5

