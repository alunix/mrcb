#!/usr/bin/env python
#
# Multi Router Configuration Backup (MRCB)
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

import datetime, glob, json, os, sys
import error as e, routeros

# Default configuration file location
MRCB_CONFIG = "config.json"
# Default backup directory
DEF_BACKUPDIR = './backup'

def get_latest_export(bkp_dir, per_device, dev_name):
  "Get name of latest export file by modification time"
  if per_device:
    glob_pattern = "%s/%s/%s_*.rsc" % (bkp_dir, dev_name, dev_name)
  else:
    glob_pattern = "%s/%s_*.rsc" % (bkp_dir, dev_name)

  files = glob.glob(glob_pattern)

  if files:
    # TODO: What if old export was changed recently?
    return max(files, key=os.path.getmtime)
  else:
    return ''

def main():
  # Open configuration file
  try:
    cfg_file = open(MRCB_CONFIG, "r")
  except Exception as err:
    e.perror("Cannot open configuration file '%s': %s" % (MRCB_CONFIG, str(err)))
    return 1

  # Load configuration
  try:
    cfg = json.load(cfg_file)
  except Exception as err:
    e.perror("Cannot read configuration: %s" % str(err))
    return 2

  cfg_file.close()

  if not cfg.get('backup_dir'):
    e.pwarn("Using default backup directory '%s'. Please, check your configuration." % DEF_BACKUPDIR)
    cfg['backup_dir'] = DEF_BACKUPDIR

  # Check if backup directory exist and try to create it
  if not os.path.exists(cfg['backup_dir']):
    try:
      e.pinfo("Creating directory '%s'." % cfg['backup_dir'])
      os.mkdir(cfg['backup_dir'])
    except Exception as err:
      e.perror("Cannot create backup directory '%s': %s" % (cfg['backup_dir'], str(err)))
      return 3
  elif not os.path.isdir(cfg['backup_dir']):
    e.perror("Path '%s' set as 'backup_dir' is not a directory!" % cfg['backup_dir'])
    return 4

  if not cfg.get('routers'):
    e.perror("No routers configured! Please, fix your configuration.")
    return 5

  # Loop routers
  for rtr in cfg['routers']:
    e.pinfos("Backing up configuration of '%s'... " % rtr['name'])

    # export configuration
    try:
      ros = routeros.SecureTransport(rtr['hostname'], rtr['port'])
      ros.login(rtr['username'], rtr['password'])
      ros.make_export()
      today = datetime.datetime.now()
      today_str = today.strftime("%Y%m%d-%H%M%S")

      if cfg['backup_dir_per_device']:
        dev_bkp_dir = "%s/%s" % (cfg['backup_dir'], rtr['name'])
        if not os.path.exists(dev_bkp_dir):
          try:
            os.mkdir(dev_bkp_dir)
          except Exception as err:
            e.perror("Cannot create device backup directory '%s': %s" % (dev_bkp_dir, str(err)))
        local_exp_file = "%s/%s/%s_%s.rsc" % (cfg['backup_dir'], rtr['name'], rtr['name'], today_str)
      else:
        local_exp_file = "%s/%s_%s.rsc" % (cfg['backup_dir'], rtr['name'], today_str)

      # get last export before new one is downloaded
      last_exp_file = get_latest_export(cfg['backup_dir'],
                                        cfg['backup_dir_per_device'],
                                        rtr['name'])
      # TODO: Get remote file datetime?
      ros.get_export(local_exp_file)
      ros.close()
    except Exception as err:
      e.pinfoe("Fail.")
      e.perror("Cannot get configuration: %s" % str(err))
      continue

    # compare with last configuration export if any
    if last_exp_file:
      ros_exp = routeros.Export()
      if ros_exp.same(last_exp_file, local_exp_file):
        e.pinfoe("Kept (%s)." % last_exp_file)
        os.remove(local_exp_file)
        continue

    e.pinfoe("Done (%s)." % local_exp_file)

exit(main())

