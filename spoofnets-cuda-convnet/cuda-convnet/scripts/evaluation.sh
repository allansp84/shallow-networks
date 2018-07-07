#!/bin/sh

#make iris_printed_Warsaw_200_250_1 target=iris_printed_Warsaw_train_200_250_1
#make iris_printed_Warsaw_200_250_1 target=iris_printed_Warsaw_test_200_250_1

make classification_iris_printed_MobBIOfake operation=resize height=256 width=320 channel=1 eval_measure=acc

#make iris_printed_Biosec target=iris_printed_Biosec_train
#make iris_printed_Biosec target=iris_printed_Biosec_test

#make repla_attack operation=None height=240 width=320 channel=1 eval_measure=acc subset=train
#make repla_attack operation=None height=240 width=320 channel=1 eval_measure=acc subset=devel
#make repla_attack operation=None height=240 width=320 channel=1 eval_measure=acc subset=test
#make repla_attack operation=None height=240 width=320 channel=1 eval_measure=acc subset=competition_icb2013
