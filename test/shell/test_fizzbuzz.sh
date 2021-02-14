#!/bin/bash
SOCKET="$1"

EXPECTED=$(cat <<-EOM
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
Fizzbuzz
EOM
)

# Note that the command-line for the Python script is only broken so *this*
# script is more easily readable.
RESULT=$(seq 1 15 | python3 -m lpython -t lines \
    'if int(LINE) % 15 == 0: print("Fizzbuzz"); elif int(LINE) % 3 == 0: print("Fizz");' \
    'elif int(LINE) % 5 == 0: print("Buzz"); else: OUT(LINE); endif')

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
