#!/bin/bash
#usage: ./ConvertCToPython.sh test
#arg1: file name, need test.c and test.i exisit
#set -x
export PYTHON_INC=/usr/include/python2.7
if [ -z $1 ];then
    echo 'need module name'
    exit -1
elif [ $1 = '-c' ];then
    set -x
    rm -rf *.o *.so *_wrap.c
    set +x
    exit 0
fi
module_name=$1
set -x
swig -python ${module_name}.i

gcc -fPIC -c ${module_name}.c
gcc -I$PYTHON_INC -fPIC -c ${module_name}_wrap.c
gcc -shared -fPIC -o _${module_name}.so ${module_name}_wrap.o ${module_name}.o
set +x
