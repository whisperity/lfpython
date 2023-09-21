#!/bin/bash
# Copyright (C) 2020 Whisperity
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
RESULT=$(seq 1 15 | python3 -m pysln -t lines \
    'if int(LINE) % 15 == 0: print("Fizzbuzz"); elif int(LINE) % 3 == 0: print("Fizz");' \
    'elif int(LINE) % 5 == 0: print("Buzz"); else: print(LINE); endif')

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
