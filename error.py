# Multi Router Configuration Backup (MRCB)
# Functions to print error messages
# Copyright (c) 2020 Georgi D. Sotirov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import print_function # requires python 2.6 or later
import sys

# TODO: Use termcolor or colorama
class TermColors:
  RED     = '\033[91m'
  CYAN    = '\033[36m'
  ORANGE  = '\033[33m'
  NORMAL  = '\033[0m'

def perror(*objects):
  "Print error message to stderr"
  sys.stderr.write(TermColors.RED + "Error" + TermColors.NORMAL + ": ")
  sys.stdout.flush()
  print(*objects, file=sys.stderr)

def pwarn(*objects):
  "Print warning message to stderr"
  sys.stderr.write(TermColors.ORANGE + "Warning" + TermColors.NORMAL + ": ")
  sys.stdout.flush()
  print(*objects, file=sys.stderr)

def pinfo(*objects):
  "Print info message to stdout"
  sys.stdout.write(TermColors.CYAN + "Info" + TermColors.NORMAL + ": ")
  sys.stdout.flush()
  print(*objects, file=sys.stdout)

def pinfos(*objects):
  "Start info message without newline to stdout, so it could be continued"
  sys.stdout.write(TermColors.CYAN + "Info" + TermColors.NORMAL + ": ")
  sys.stdout.write(*objects)
  sys.stdout.flush()

def pinfoe(*objects):
  "End info message"
  print(*objects, file=sys.stdout)

