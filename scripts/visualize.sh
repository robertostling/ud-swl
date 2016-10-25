#!/bin/sh

SCRIPTDIR=`dirname $0`
SCRIPTDIR=`realpath $SCRIPTDIR`
OUTDIR=`pwd`
FDPDIR="$SCRIPTDIR"/../../Finnish-dep-parser
CONLLDIR="$SCRIPTDIR"/../../UD_Swedish_Sign_Language

cd "$FDPDIR"
python visualize.py "$CONLLDIR/swl-ud-train.conllu" >"$OUTDIR"/train.html
python visualize.py "$CONLLDIR/swl-ud-dev.conllu" >"$OUTDIR"/dev.html
python visualize.py "$CONLLDIR/swl-ud-test.conllu" >"$OUTDIR"/test.html

