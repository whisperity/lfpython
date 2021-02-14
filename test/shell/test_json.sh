#!/bin/bash
SOCKET="$1"

INPUT=$(cat <<-EOM
[{"Timezone": "Europe/London"}, {"Timezone": "America/New York"}]
EOM
)

EXPECTED=$(cat <<-EOM
[{"Country": "Europe", "City": "London"}, {"Country": "America", "City": "New York"}]
EOM
)

EXPECTED_PRETTY=$(cat <<-EOM
[
    {
        "City": "London",
        "Country": "Europe"
    },
    {
        "City": "New York",
        "Country": "America"
    }
]
EOM
)

SCRIPT='for rec in DATA: for k, v in dict(rec).items(): if k == "Timezone": split = v.split("/"); rec["Country"] = split[0]; rec["City"] = split[1]; del rec["Timezone"]; endif; endfor; endfor;'

RESULT=$(echo $INPUT | python3 -m lpython -t json "${SCRIPT}")

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


RESULT_PRETTY=$(echo "$INPUT" | python3 -m lpython -t json "${SCRIPT}; PRETTY();")

if [[ "$EXPECTED_PRETTY" != "$RESULT_PRETTY" ]]
then
    echo "[ERROR] Received output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$RESULT_PRETTY" >&2
    echo "----------------------------------------" >&2
    echo "Does NOT match expected output:" >&2
    echo "----------------------------------------" >&2
    echo -e "$EXPECTED_PRETTY" >&2
    echo "----------------------------------------" >&2

    echo "FAIL" >> $SOCKET
fi

echo "OK" >> $SOCKET
