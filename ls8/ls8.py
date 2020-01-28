#!/usr/bin/env python

"""Main."""

import sys
from cpu import *

file_name = sys.argv[1]

cpu = CPU()

cpu.load()(file_name)
cpu.run()