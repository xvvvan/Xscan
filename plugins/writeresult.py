# -*- coding: utf-8 -*-

import os,sys
sys.path.append("..")

def writer(result):
    with open(r'result.txt','a+') as f:
        f.write(result+'\n')
if __name__ == '__main__':
    writer('aaa')