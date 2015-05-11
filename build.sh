#!/usr/bin/env bash

# A script to build the exporter. A virtualenv environment is created for
# dependencies. After the build a standalone executable will be produced.
#
# If any program arguments are specified (i.e. anything preceding the final --)
# then the output binary is executed within a virtualenv environment with those
# arguments.

source third_party/shflags.sh

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

# Builds the output binary.
function build() {
  TMP_FILE=$(mktemp -u --suffix=.zip)
  zip ${TMP_FILE} __main__.py sportszone.py
  echo "#!/usr/bin/env python" | cat - ${TMP_FILE} > ${FLAGS_out}
  chmod +x ${FLAGS_out}
  rm ${TMP_FILE}
}

# Creates a virtualenv environment and runs the output binary in it.
function run() {
  [ ! -d ${FLAGS_envname} ] && virtualenv ${FLAGS_envname}
  source ${FLAGS_envname}/bin/activate
  pip install lxml python-gflags pytz requests
  ./${FLAGS_out} $@
  deactivate
}

if [ ${FLAGS_clean} -eq ${FLAGS_TRUE} ]; then
  clean
  exit
fi

build
[ ${#@} -gt 0 ] && run $@
