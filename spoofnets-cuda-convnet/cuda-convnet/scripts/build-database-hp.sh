#!/bin/sh

# *** Finger Print *** #
#make build_database_hp database=LivDet2013 subset=BiometrikaTrain image_type=png


# *** Face *** #
make build_database_hp_3dmad operation=None height=480 width=640 channel=1 image_type=png


