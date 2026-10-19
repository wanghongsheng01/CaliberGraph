"""Build the public artifact repository for the PVLDB submission from the tracked files of this
(development) repository. Internal working notes are excluded; the pre-registrations, freeze
records, code, data, raw outputs, annotations and paper sources are included.

Usage: python tools/build_release.py OUT_DIR
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INCLUDE_PREFIXES = [
    'src/', 'src_r/', 'src_v5/', 'src_s3/', 'data/', 'results/', 'paper_pvldb/', 'tools/', 'REPRODUCE_DERIVED.md',
    'docs/en/', 'docs/FREEZE.md', 'docs/FREEZE_R.md', 'docs/FREEZE_SHA256.txt', 'docs/FREEZE_R_SHA256.txt',
    'docs/FREEZE_S3.md', 'docs/FREEZE_S3_SHA256.txt', 'docs/02_', 'docs/02a_', 'docs/07_',
    'spider/data/', 'spider/results/', 'spider/aborted_', 'minidev/data/', 'minidev/results/', 'spider_smoke/data/', 'spider_smoke/results/',
]
EXCLUDE_SUFFIXES = ('.aux', '.log', '.out', '.blg', '.spl', '.synctex.gz')
EXCLUDE_EXACT = {'paper_pvldb/main.pdf',
                 # withheld until all round-3 sheets are returned (docs/en/17c; SHA-256 in docs/en/17c_key_sha256.txt)
                 'results/audit/human_validation_r3/key_DO_NOT_OPEN_BEFORE_ANNOTATING.json'}  # rebuilt from sources; the submitted PDF goes to CMT


def tracked():
    out = subprocess.run(['git', '-C', ROOT, 'ls-files', '-z'], capture_output=True, check=True).stdout
    return [p for p in out.decode().split('\0') if p]


def keep(p):
    if p in EXCLUDE_EXACT or p.endswith(EXCLUDE_SUFFIXES) and p.startswith('paper_pvldb/'):
        return False
    return any(p.startswith(x) for x in INCLUDE_PREFIXES)


def main(out):
    if os.path.exists(out) and os.listdir(out):
        sys.exit(f'{out} exists and is not empty')
    files = [p for p in tracked() if keep(p)]
    total = 0
    for p in files:
        src = os.path.join(ROOT, p)
        dst = os.path.join(out, p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        total += os.path.getsize(src)
    for name, dst in (('release/README.md', 'README.md'), ('release/THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_NOTICES.md'), ('release/requirements.txt', 'requirements.txt'),
                      ('release/LICENSE', 'LICENSE'), ('release/AI_USE.md', 'AI_USE.md')):
        src = os.path.join(ROOT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(out, dst))
    head = subprocess.run(['git', '-C', ROOT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(out, 'RELEASE_INFO.txt'), 'w') as f:
        f.write(f'Snapshot of development repository commit {head}\n{len(files)} files, {total / 1e6:.1f} MB\n')
    print(len(files), 'files', f'{total / 1e6:.1f} MB ->', out)


if __name__ == '__main__':
    main(sys.argv[1])
