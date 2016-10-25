import re
import sys
import os
from collections import defaultdict

from pympi import Elan

with open(os.path.join(os.path.dirname(sys.argv[0]), 'gestures_pos.txt'),
          'r', encoding='utf-8') as f:
    GESTURES_POS = dict(line.split() for line in f if len(line.split()) == 2)

RE_GLOSS = re.compile(r'(.+)\[([^\]]+)\]$')

POS_TABLE = {
        'AB':       'ADV',
        'INTERJ':   'INTJ',
        'NN':       'NOUN',
        'NNKL':     'NOUN',
        'PN':       'PRON',
        'JJ':       'ADJ',
        'PP':       'ADP',
        'KN':       'CONJ',
        'RG':       'NUM',
        'VB':       'VERB',
        'VBS':      'VERB',
        'VBPP':     'VERB',
        'VBCA':     'VERB',
        'VBAV':     'VERB',
        'G':        'X',
        'PEK':      'X',
        'BOJ':      'X',
        }

def parse_gloss(s):
    m = RE_GLOSS.match(s)
    assert m is not None, s
    return m.group(1), m.group(2)

def convert(filename):
    eaf = Elan.Eaf(filename)

    utts = []

    def translate_pos(pos, dep, gloss):
        if '?' in pos:
            print('Warning: removing ? from "%s"' % pos, file=sys.stderr)
            pos = pos.replace('?', '')
        elif pos not in POS_TABLE:
            print('Warning: unknown PoS tag "%s"' % pos, file=sys.stderr)
        if pos[:2] == 'VB': return 'VERB'
        if pos == 'G':
            return GESTURES_POS.get(gloss+'[G]', 'X')
        if pos == 'PEK':
            return 'DET' if dep == 'det' else 'PRON'
        return POS_TABLE.get(pos, 'X')

    def utt_to_conllu(utt):
        base = utt[0]['index']

        def process_sign(sign):
            return [str(sign['index']-base+1),
                    sign['gloss'],
                    '_',
                    translate_pos(sign['pos'], sign['dep'], sign['gloss']),
                    sign['pos'],
                    '_',
                    str(0 if sign['head'] == 0 else sign['head']-base+1),
                    sign['dep'],
                    '_',
                    '_']

        return list(map(process_sign, utt))

    for signer in (1, 2):
        def get_annotation_from_hand(tier, hand):
            return [(hand,) + t for t in eaf.get_annotation_data_for_tier(
                        '%s_%s S%d' % (tier, hand, signer))]

        def get_annotation(tier):
            return get_annotation_from_hand(tier, 'DH') + \
                   get_annotation_from_hand(tier, 'NonDH')

        #ann_glosses = get_annotation('Glosa')
        ann_index = get_annotation('Index')
        ann_dep = get_annotation('UD')
        ann_head = get_annotation('Link')

        slots = defaultdict(dict)

        for hand, t0, t1, i, gloss_pos in ann_index:
            try:
                slots[(t0, t1)]['index'] = int(i)
            except ValueError:
                print('Warning: invalid index "%s"' % i, file=sys.stderr)
            gloss, pos = parse_gloss(gloss_pos)
            slots[(t0, t1)]['gloss'] = gloss
            slots[(t0, t1)]['pos'] = pos
            slots[(t0, t1)]['t0'] = t0

        for hand, t0, t1, i, gloss in ann_head:
            try:
                slots[(t0, t1)]['head'] = int(i)
            except ValueError:
                print('Warning: invalid head "%s" at index %d' % (
                    i, slots[(t0, t1)]['index']), file=sys.stderr)

        for hand, t0, t1, dep, gloss in ann_dep:
            if dep:
                # hack to fix typo
                if dep == 'reparandium': dep = 'reparandum'
                slots[(t0, t1)]['dep'] = dep

        children = defaultdict(list)
        signs = {}
        roots = []

        for (t0, t1), sign in slots.items():
            try:
                index = sign['index']
                dep = sign['dep']
                head = sign['head']
                gloss = sign['gloss']
                pos = sign['pos']
                children[head].append(index)
                signs[index] = sign
                if head == 0:
                    roots.append(sign)
            except KeyError:
                pass

        roots.sort(key=lambda sign: sign['index'])

        def get_flat_tree(index):
            return [signs[index]] + sum(
                    [get_flat_tree(child) for child in children[index]], [])

        for root in roots:
            utt = get_flat_tree(root['index'])
            utt.sort(key=lambda sign: sign['index'])
            indexes = [sign['index'] for sign in utt]
            expected = set(range(min(indexes), max(indexes)+1))
            missing = expected - set(indexes)
            if not missing:
                utts.append(utt)
            else:
                print('Warning: signs %d and %d are connected to each other'
                      ' but not to the following signs between them: %s' % (
                          min(indexes), max(indexes),
                          ', '.join(map(str, sorted(missing)))),
                      file=sys.stderr)


    print('%d trees, %d signs' % (len(roots), len(signs)), file=sys.stderr)

    return [utt_to_conllu(utt) for utt in utts]


def main():
    for filename in sys.argv[1:]:
        print('Converting %s...' % filename, file=sys.stderr)
        sents = convert(filename)
        for sent in sents:
            for sign in sent:
                print('\t'.join(sign))
            print()


if __name__ == '__main__': main()

