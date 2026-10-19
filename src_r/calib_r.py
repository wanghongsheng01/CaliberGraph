"""Add the annotation-drift check (calibration items) to a second-freeze summary file."""
import json
import sys

summ, key_p, a_p, b_p, c_p, a4, b4, c4 = sys.argv[1:9]
key = {k['idx']: k for k in json.load(open(key_p))}


def final(a, b, c):
    A = {x['idx']: x['verdict'] for x in json.load(open(a))}
    B = {x['idx']: x['verdict'] for x in json.load(open(b))}
    C = {x['idx']: x['verdict'] for x in json.load(open(c))}
    return {i: (A[i] if A[i] == B[i] else C[i]) for i in A}


f, f4 = final(a_p, b_p, c_p), final(a4, b4, c4)
cal = [i for i in key if key[i]['source'].startswith('calib')]
S = json.load(open(summ))
S['calibration'] = dict(n=len(cal), same=sum(f[i] == f4[key[i]['orig_idx']] for i in cal),
                        same_implausible=sum((f[i] == 'implausible_data') == (f4[key[i]['orig_idx']] == 'implausible_data') for i in cal))
json.dump(S, open(summ, 'w'), indent=1)
print(S['calibration'])
