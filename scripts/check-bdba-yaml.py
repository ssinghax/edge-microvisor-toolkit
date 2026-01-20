#!/usr/bin/python

import os
import sys
from yaml import load, Loader
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, force=True)

edge_specs = os.environ.get('EDGE_MT_SPECS', '')
check_pass = ' PASS'
check_fail = 'FAIL'
check_warn = ' WARN'

if edge_specs == '':
    logging.error("EDGE_MT_SPECS environment variable is not set.")
    sys.exit(1)
else:
    for spec in edge_specs.split(' '):
        if os.path.isfile(spec):
            spec_name = spec.split('/')[1]
            bdba_yaml = spec.split('/')[-1]
            bdba_yaml_ext = bdba_yaml.split('.')[-1]

            # Check file extension
            if bdba_yaml_ext != 'yaml':
                logging.error(f"{check_fail}: File extension check for {spec_name}.")
                logging.error(f"{check_fail}: Expected '.yaml' extension but found '.{bdba_yaml_ext}'.")
                sys.exit(1)
            else:
                logging.info(f"{check_pass}: File extension check for {spec_name}.")

            # Check specVersion in YAML content
            stream = open(spec, 'r')
            bdba_data = load(stream, Loader=Loader)
            if bdba_data is None:
                logging.warning(f"{check_warn}: Content is empty for {spec_name}.")
            else:
                if 'specVersion' in bdba_data:
                    logging.info(f"{check_pass}: specVersion check for {spec_name}.")

                    if bdba_data['specVersion'] == 3:
                        logging.info(f"{check_pass}: specVersion is '3' for {spec_name}.")
                    else:
                        logging.error(f"{check_fail}: specVersion is '{bdba_data['specVersion']}' for {spec_name}, expected '3'.")
                else:
                    logging.error(f"{check_fail}: specVersion check for {spec_name}.")
    
