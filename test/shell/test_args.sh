#!/bin/bash
SOCKET="$1"

EXPECTED=$(cat <<-EOM
Foo
$(bash --version)
EOM
)

RESULT=$(python3 -m lpython -t bare -X "Foo" -X "$(bash --version)" \
    'print(ARGS[1]); print(ARGS[2])')

if [[ $EXPECTED != $RESULT ]]
then
    echo "[ERROR] Received output:" >&2
    echo "----------------------------------------" >&2
    echo -e $RESULT >&2
    echo "----------------------------------------" >&2
    echo "Does NOT match expected output:" >&2
    echo "----------------------------------------" >&2
    echo -e $EXPECTED >&2
    echo "----------------------------------------" >&2

    echo "FAIL" >> $SOCKET
fi

echo "OK" >> $SOCKET
