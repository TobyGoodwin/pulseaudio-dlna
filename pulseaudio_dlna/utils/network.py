#!/usr/bin/python

# This file is part of pulseaudio-dlna.

# pulseaudio-dlna is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pulseaudio-dlna is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pulseaudio-dlna.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import commands
import re
import netifaces


def default_ipv4():
    return _default_ipv4_cmd_ip() or _default_ipv4_cmd_networkctl()


def _default_ipv4_cmd_ip():
    status_code, result = commands.getstatusoutput(
        'ip route get 255.255.255.255')
    if status_code == 0:
        match = re.findall(
            r"(?<=src )(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})", result)
        if match:
            return match[0]
    return None


def _default_ipv4_cmd_networkctl():
    status_code, result = commands.getstatusoutput('networkctl status')
    if status_code == 0:
        match = re.findall(
            r"Address: (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) on", result)
        if match:
            return match[0]
    return None


def ipv4_addresses():
    ips = []
    for iface in netifaces.interfaces():
        for link in netifaces.ifaddresses(iface).get(netifaces.AF_INET, []):
            ip = link.get('addr', None)
            if ip:
                ips.append(ip)
    return ips
