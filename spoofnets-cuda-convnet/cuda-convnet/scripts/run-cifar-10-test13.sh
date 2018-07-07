python convnet.py --data-path=/home/menotti/datasets/cifar-10-py-colmajor/ --save-path=/home/menotti/results/cifar-10-py --test-range=5 --train-range=1-4 --layer-def=./example-layers/layers-conv-local-13pct.cfg --layer-params=./example-layers/layer-params-conv-local-13pct.cfg --data-provider=cifar-cropped --crop-border=4 --test-freq=13 --epochs=100

#python convnet.py -f /home/menotti/results/cifar-10-py/ConvNet__2014-10-15_18.13.52 --train-range=1-5 --epochs=140

## Now we reduce all learning rates (the epsW parameters) in the layer parameter file by a factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/menotti/results/cifar-10-py/ConvNet__2014-10-15_18.13.52 --epochs=150
## Reduce all learning rates in the layer parameter file by another factor of 10, and train for another 10 epochs:
#python convnet.py -f /home/menotti/results/cifar-10-py/ConvNet__2014-10-15_18.13.52 --epochs=160

