#!/bin/bash

ANY_FAIL=0

for F in ./shell/*.sh
do
    echo "Running test '$F'..." >&2
    socket=$(mktemp --suffix="-lpytest")
    bash $F $socket
    if [[ "$(cat $socket)" != "OK" ]]
    then
        echo -e "\tTest failed!" >&2
        ANY_FAIL=1
    fi
    rm $socket
done

if [[ $ANY_FAIL -ne 0 ]]
then
    echo "Some tests failed." >&2
    exit 1
fi
exit 0
