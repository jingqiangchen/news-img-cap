#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import threading

import common

class Meteor(object):

    def __init__(self):
        self.meteor_cmd = ['java', '-jar', '-Xmx2G', common.path_meteor, \
                '-', '-', '-stdio', '-l', 'en', '-norm']
        self.meteor_p = subprocess.Popen(self.meteor_cmd, \
                cwd=common.path_lib, \
                stdin=subprocess.PIPE, \
                stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        self.lock = threading.Lock() # Used to guarantee thread safety

    def _score(self, hypothesis_str, reference_list):
        self.lock.acquire()
        # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
        hypothesis_str = hypothesis_str.replace('|||','').replace('  ',' ')
        score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str))
        w = '{}\n'.format(score_line)
        self.meteor_p.stdin.write(w)
        stats = self.meteor_p.stdout.readline().strip()
        
        eval_line = 'EVAL ||| {}'.format(stats)
        w = '{}\n'.format(eval_line)
        self.meteor_p.stdin.write(w)
        r = self.meteor_p.stdout.readline().strip()
        score = float(r)
        # I don't know why we were reading out twice? That doesn't work
        # r = self.meteor_p.stdout.readline().strip()
        # print 'got second line of EVAL results:'
        # score = float(r) # have to read out twice
        # print r, score
        self.lock.release()
        return score
 
    def __exit__(self):
        self.lock.acquire()
        self.meteor_p.stdin.close()
        self.meteor_p.wait()
        self.lock.release()

if __name__ == "__main__":
    '''
        assert os.path.isfile(common.path_meteor), 'you must have meteor-1.5.jar! Check README.md instructions in eval/ folder.'
    
        jobid = sys.argv[1] if len(sys.argv) >= 2 else ''
        INPUT_FILE = os.path.join(ABSPATH, 'input%s.json' % (jobid, ))
        OUTPUT_FILE = os.path.join(ABSPATH, 'output%s.json' % (jobid, ))    
    
        m = Meteor()
        import json
        records = json.load(open(INPUT_FILE, 'r'))
    '''
    scores = []
    m = Meteor()
    candidate="you must have meteor"
    references="you must have meteor"
    score = m._score(candidate, references)
    scores.append(score)

    out = {}
    out['scores'] = scores
    out['average_score'] = sum(scores) / len(scores)
    
    print(score)










