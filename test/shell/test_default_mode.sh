#!/bin/bash
SOCKET="$1"

EXPECTED=$(cat <<-EOM
Foo
EOM
)

RESULT_NOTPIPE=$(python3 -m lpython 'print(LINE);' 2>&1)

EXPECTED_ERROR="NameError: name 'LINE' is not defined"
TEST_NOTPIPE=$(echo "$RESULT_NOTPIPE" | grep "$EXPECTED_ERROR")
if [[ $? -ne 0 ]]
then
    echo "[ERROR] Received output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$RESULT" >&2
    echo "----------------------------------------" >&2
    echo "Does NOT contain:" >&2
    echo "----------------------------------------" >&2
    echo -e "$EXPECTED_ERROR" >&2
    echo "----------------------------------------" >&2

    echo "FAIL" >> $SOCKET
fi

RESULT_PIPE=$(echo "Foo" | python3 -m lpython 'print(LINE);')

if [[ "$EXPECTED" != "$RESULT_PIPE" ]]
then
    echo "[ERROR] Received output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$RESULT_PIPE" >&2
    echo "----------------------------------------" >&2
    echo "Does NOT match expected output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$EXPECTED" >&2
    echo "----------------------------------------" >&2

    echo "FAIL" >> $SOCKET
fi

echo "OK" >> $SOCKET
