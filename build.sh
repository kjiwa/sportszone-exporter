#!/usr/bin/env bash

# A script to build the exporter. A virtualenv environment is created for
# dependencies. After the build a standalone executable will be produced.

source shflags.sh

DEFINE_boolean clean false "Clean the directory of build artifacts."
DEFINE_string envname env "The virtualenv environment to create."
DEFINE_string out exporter "The name of the output binary"

FLAGS $@ || exit $?
eval set -- ${FLAGS_ARGV}

set -e

[ ${FLAGS_help} -eq ${FLAGS_TRUE} ] && exit 0

# Cleans the directory of build artifacts.
function clean() {
  rm -rf ${FLAGS_envname} ${FLAGS_out}
}

# Creates a virtualenv environment and installs dependencies.
function setup() {
  [ ! -d ${FLAGS_envname} ] && virtualenv ${FLAGS_envname}
  source ${FLAGS_envname}/bin/activate
  pip install lxml python-gflags pytz requests
}

# Exits the build/run environment.
function teardown() {
  deactivate
}

# Builds the output binary.
function build() {
  TMP_FILE=$(mktemp -u --suffix=.zip exporterXXX)
  zip ${TMP_FILE} __main__.py sportszone.py translator.py
  echo "#!/usr/bin/env python" | cat - ${TMP_FILE} > ${FLAGS_out}
  chmod +x ${FLAGS_out}
  rm ${TMP_FILE}
}

# Runs the output binary.
function run() {
  ./exporter $@
}

if [ ${FLAGS_clean} -eq ${FLAGS_TRUE} ]; then
  clean
  exit
fi

setup
build
run $@
teardown
