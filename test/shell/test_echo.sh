#!/bin/bash
SOCKET="$1"

if [[ $(hostname) != $(hostname | python3 -m lpython -t lines 'OUT(LINE);') ]]
then
    echo $(hostname)" echo failed." >&2
    echo "FAIL" >> $SOCKET
fi

if [[ $(id) != $(id | python3 -m lpython -t lines 'OUT(LINE);') ]]
then
    echo $(id)" echo failed." >&2
    echo "FAIL" >> $SOCKET
fi


if [[ $(ls -l) != $(ls -l | python3 -m lpython -t lines 'OUT(LINE);') ]]
then
    echo $(ls -l)" echo failed." >&2
    echo "FAIL" >> $SOCKET
fi

echo "OK" >> $SOCKET
