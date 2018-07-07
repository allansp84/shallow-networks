#!/bin/sh

# *** Iris *** #

#make iris_printed_MobBIOfake operation=resize height=256 width=320 channel=1 eval_measure=acc subset=train
#make iris_printed_MobBIOfake operation=resize height=256 width=320 channel=1 eval_measure=acc subset=test

#make iris_printed_Warsaw_200_250_1 target=iris_printed_Warsaw_train_200_250_1
#make iris_printed_Warsaw_200_250_1 target=iris_printed_Warsaw_test_200_250_1

#make iris_printed_Biosec target=iris_printed_Biosec_train
#make iris_printed_Biosec target=iris_printed_Biosec_test


# *** Face *** #

#make representation operation=crop height=200 width=200 channel=1 eval_measure=acc subset=train target=ra_representation
#make representation operation=crop height=200 width=200 channel=1 eval_measure=acc subset=devel target=ra_representation
#make representation operation=crop height=200 width=200 channel=1 eval_measure=acc subset=test target=ra_representation
#make representation operation=crop height=200 width=200 channel=1 eval_measure=acc subset=competition_icb2013 target=ra_representation

#make representation operation=None height=480 width=640 channel=1 eval_measure=acc subset=train target=3dmad_representation
#make representation operation=None height=480 width=640 channel=1 eval_measure=acc subset=devel target=3dmad_representation
#make representation operation=None height=480 width=640 channel=1 eval_measure=acc subset=test target=3dmad_representation


# *** Fingerprint *** #

make representation operation=resize height=320 width=268 channel=1 eval_measure=acc subset=train target=ld13bio_representation
make representation operation=resize height=320 width=268 channel=1 eval_measure=acc subset=test target=ld13bio_representation


