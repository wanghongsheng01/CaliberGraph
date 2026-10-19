"""S3-D attribution adapter (amendment E8): write spider/data/raw/bird_dev_20240627.json, the question file the
frozen src_r/audit_build.py reads, from Spider dev.json (index = qid; Spider has no evidence, so evidence = '').
Usage: python src_s3/spider_devjson.py /home/claude/ext/spider_full/spider/dev.json spider"""
import json, os, sys
dev = json.load(open(sys.argv[1]))
out = [dict(question_id=i, db_id=d['db_id'], question=d['question'], evidence='', SQL=d['query'], difficulty=None)
       for i, d in enumerate(dev)]
json.dump(out, open(os.path.join(sys.argv[2], 'data', 'raw', 'bird_dev_20240627.json'), 'w'), indent=0)
print(len(out))
