#!/bin/sh

SCRIPTDIR=`dirname $0`
DATADIR="$SCRIPTDIR"/../data
DESTDIR="$SCRIPTDIR"/../../UD_Swedish_Sign_Language

echo "Converting train set..."

echo -n >"$DESTDIR"/swl-ud-train.conllu

# TODO: this was in the old version, make sure to re-include it in the test
#       set once it is ready for UDv2
#python3 $SCRIPTDIR/elan_to_conllu.py \
#    "$DATADIR"/SSLC02_409_UD_CB_proofed.eaf \
#    >>"$DESTDIR"/swl-ud-train.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC01_104_UD.eaf \
    "$DESTDIR"/swl-ud-train.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC01_391_UD.eaf \
    "$DESTDIR"/swl-ud-train.conllu

echo "----------------------------------------------------------------"

echo "Converting dev set..."

echo -n >"$DESTDIR"/swl-ud-dev.conllu

# TODO: add to dev set once ready for UDv2
#python3 $SCRIPTDIR/elan_to_conllu.py \
#    "$DATADIR"/SSLC02_332_UD_MG_161025.eaf \
#    >>"$DESTDIR"/swl-ud-dev.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC01_320_UD.eaf \
    "$DESTDIR"/swl-ud-dev.conllu

echo "----------------------------------------------------------------"

echo "Converting test set..."

echo -n >"$DESTDIR"/swl-ud-test.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC02_331_UD.eaf \
    "$DESTDIR"/swl-ud-test.conllu

echo "----------------------------------------------------------------"

