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

RESULT=$(echo "$INPUT" | python3 -m pysln -t csv "${SCRIPT}" | tr -d '\r')

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
