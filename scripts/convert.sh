#!/bin/sh

SCRIPTDIR=`dirname $0`
DATADIR="$SCRIPTDIR"/../data
DESTDIR="$SCRIPTDIR"/../../UD_Swedish_Sign_Language

echo "Converting train set..."

echo -n >"$DESTDIR"/swl-ud-train.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC02_409_UD_CB_proofed.eaf \
    >>"$DESTDIR"/swl-ud-train.conllu

echo "----------------------------------------------------------------"

echo "Converting dev set..."

echo -n >"$DESTDIR"/swl-ud-dev.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC02_332_UD_MG_161025.eaf \
    >>"$DESTDIR"/swl-ud-dev.conllu

echo "----------------------------------------------------------------"

echo "Converting test set..."

echo -n >"$DESTDIR"/swl-ud-test.conllu

python3 $SCRIPTDIR/elan_to_conllu.py \
    "$DATADIR"/SSLC02_331_UD_MG_161024_CB_proofed.eaf \
    >>"$DESTDIR"/swl-ud-test.conllu

echo "----------------------------------------------------------------"

