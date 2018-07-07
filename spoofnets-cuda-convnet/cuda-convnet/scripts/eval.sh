#!/bin/sh

# *** Face *** #

#make evaluation_hter database=ra.crop.200x200.1.acc fusion=max target=ra_hter
#make evaluation_hter database=ra.crop.200x200.1.acc fusion=min target=ra_hter
#make evaluation_hter database=ra.crop.200x200.1.acc fusion=mean target=ra_hter

#make evaluation_hter database=3dmad.None.480x640.1.acc fusion=max target=3dmad_hter
#make evaluation_hter database=3dmad.None.480x640.1.acc fusion=min target=3dmad_hter
#make evaluation_hter database=3dmad.None.480x640.1.acc fusion=mean target=3dmad_hter

make evaluation_hter database=ra.None.240x320.1.acc fusion=max target=ra_hter
make evaluation_hter database=ra.None.240x320.1.acc fusion=min target=ra_hter
make evaluation_hter database=ra.None.240x320.1.acc fusion=mean target=ra_hter




