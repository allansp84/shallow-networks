#!/bin/sh

# *** Iris *** #

#make classification_iris_printed_Warsaw_250_200_1 target=iris_printed_Warsaw_250_200_1
#make classification_iris_printed_MobBIO target=iris_printed_MobBIO
#make classification_iris_printed_Biosec target=iris_printed_Biosec


# *** Face *** #

#make classification operation=crop height=200 width=200 channel=1 eval_measure=acc subset=devel target=ra_representation
#make classification operation=crop height=200 width=200 channel=1 eval_measure=acc subset=test target=ra_representation
#make classification operation=crop height=200 width=200 channel=1 eval_measure=acc subset=competition_icb2013 target=ra_representation

#make classification operation=None height=480 width=640 channel=1 eval_measure=acc subset=devel target=3dmad_representation
#make classification operation=None height=480 width=640 channel=1 eval_measure=acc subset=test target=3dmad_representation

make classification operation=resize height=320 width=268 channel=1 eval_measure=acc subset=test target=ld13bio_representation

