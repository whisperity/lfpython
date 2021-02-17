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
