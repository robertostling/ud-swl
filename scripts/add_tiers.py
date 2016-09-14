"""Script for adding empty UD annotation tiers to ELAN files from SSLC.

Requires pympi: https://github.com/dopefishh/pympi/
"""

import sys
import os

from pympi import Elan

def add_tiers(filename):
    # Names of the controlled vocabulary / linguistic type specifications.
    # Arbitrary.
    cv = 'ud_dep'
    lang = 'und'
    lingtype = 'ud_lingtype'
    lingtype_cv = lingtype # 'ud_lingtype_cv'

    # This list will be inserted as a controlled vocabulary.
    ud_deps = ['amod', 'advmod', 'advcl', 'acl', 'case', 'auxpass', 'aux',
            'appos', 'ccomp', 'cc', 'remnant', 'punct', 'root', 'reparandum',
            'nsubjpass', 'nsubj', 'parataxis', 'nummod', 'xcomp', 'vocative',
            'dobj', 'dislocated', 'csubj', 'cop', 'conj', 'compound',
            'discourse', 'det', 'dep', 'csubjpass', 'goeswith', 'iobj',
            'expl', 'foreign', 'mwe', 'name', 'list', 'mark', 'neg', 'nmod',
            'acl:relcl']

    eaf = Elan.Eaf(filename)

    if 'swl' not in eaf.languages:
        eaf.add_language('swl', 'swl', 'Swedish Sign Language')

    # Add a controlled vocabulary for the UD labels.
    #eaf.add_controlled_vocabulary(cv)
    #eaf.add_cv_description(cv, lang, 'UD dependency labels')
    #for i,dep in enumerate(ud_deps):
    #    eaf.add_cv_entry(cv, 'cveid%d' % i, [(dep, lang, dep)])

    # Add a lingtype which ensures that the annotations are aligned with the
    # respective gloss tier.
    eaf.add_linguistic_type(
            lingtype,
            constraints='Symbolic_Association',
            timealignable=False)

    # Add another lingtype for the UD labels controlled vocabulary.
    #eaf.add_linguistic_type(lingtype_cv, param_dict={
    #    'LINGUISTIC_TYPE_ID': lingtype_cv,
    #    'TIME_ALIGNABLE': 'false',
    #    'GRAPHIC_REFERENCES': 'false',
    #    'CONTROLLED_VOCABULARY_REF': cv})

    for signer in (1, 2):
        def get_glosses(hand):
            return [(hand,) + t for t in eaf.get_annotation_data_for_tier(
                        'Glosa_%s S%d' % (hand, signer))]

        # Get a list of glosses for both hands of this signer.
        glosses = get_glosses('DH') + get_glosses('NonDH')
        glosses.sort(key=lambda t: t[1])

        # Add the necessary tiers for this signer.
        for ud_part in ('Index', 'UD', 'Link'):
            for hand in ('DH', 'NonDH'):
                tier = '%s_%s S%d' % (ud_part, hand, signer)
                ref_tier = 'Glosa_%s S%d' % (hand, signer)
                eaf.add_tier(
                        tier,
                        ling=lingtype_cv if ud_part == 'UD' else lingtype,
                        parent=ref_tier)

        # Enumerate each one of the merged DH+NonDH glosses and write the
        # index to the Index tier.
        for i, (hand, t1, t2, _) in enumerate(glosses):
            tier = 'Index_%s S%d' % (hand, signer)
            ref_tier = 'Glosa_%s S%d' % (hand, signer)
            eaf.add_ref_annotation(tier, ref_tier, (t1+t2)//2, value=str(i+1))

    return eaf

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: add_tiers.py output-directory source-directory/*.eaf'
        sys.exit(1)
    out = sys.argv[1]
    for filename in sys.argv[2:]:
        print 'Converting %s...' % filename
        eaf = add_tiers(filename)
        base = os.path.splitext(os.path.basename(filename))[0]
        target = os.path.join(out, base+'_UD.eaf')
        Elan.to_eaf(target, eaf)

