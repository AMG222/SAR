#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Info

import pickle
import re
import sys
from SAR_p3_monkey_lib import Monkey


if __name__ == "__main__":
    
    if len(sys.argv) <2:
        print("python %s indexfile" % sys.argv[0])
        sys.exit(-1)

    index_filename = sys.argv[1]
    if len(sys.argv) is 2:
        tri = False
    else:
        tri = True
    i = index_filename.rfind('.')
    info_filename = (index_filename[:i] if i > 0 else index_filename)
    if tri:
        info_filename = info_filename + "_tri"
    info_filename = info_filename + ".info"

    m = Monkey()
    m.load_index(index_filename)
    m.save_info(info_filename)