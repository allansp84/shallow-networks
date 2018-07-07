#!/bin/sh

# *** Face *** #

#make pre-processing database=databaseReplayAttack operation=resize size=100 channel=1
#make pre-processing database=databaseReplayAttack operation=resize size=100 channel=3
#make pre-processing database=databaseReplayAttack operation=crop size=200 channel=1
#make pre-processing database=databaseReplayAttack operation=crop size=200 channel=3

#make pre-processing database=database3DMAD operation=crop height=200 width=200 channel=1


# *** Fingerprint *** #

make pre-processing-fp database=fp.ld13.bio.372x312 operation=resize height=320 width=268 channel=1





