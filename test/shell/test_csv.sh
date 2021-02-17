#!/bin/bash
SOCKET="$1"

INPUT=$(cat <<-EOM
Foo,Bar,Baz
1,2,3
4,5,6
EOM
)

EXPECTED=$(cat <<-EOM
Foo,Bar,Baz
10,20,30
40,50,60
EOM
)

SCRIPT='for idx, elem in enumerate(ROW): if not HEADER(): ROW[idx] = int(elem) * 10; endif; endfor'

RESULT=$(echo "$INPUT" | python3 -m lpython -t csv "${SCRIPT}" | tr -d '\r')

if [[ "$EXPECTED" != "$RESULT" ]]
then
    echo "[ERROR] Received output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$RESULT" >&2
    echo "----------------------------------------" >&2
    echo "Does NOT match expected output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$EXPECTED" >&2
    echo "----------------------------------------" >&2

    echo "FAIL" >> $SOCKET
fi

echo "OK" >> $SOCKET
