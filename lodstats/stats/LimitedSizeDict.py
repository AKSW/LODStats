"""
Copyright 2012 Jan Demter <jan@demter.de>

This file is part of LODStats.

LODStats is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LODStats is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LODStats.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
if sys.hexversion >= 0x02070000:
    from collections import OrderedDict
else:
    from .OrderedDict import OrderedDict


class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", 300000)
        self.size_grace = kwds.pop("size_grace", 100000)
        self.overflow_callback = kwds.pop("overflow_callback", None)
        self.overflow = False
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()
        
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None and len(self) > self.size_limit + self.size_grace:
            if not self.overflow and self.overflow_callback is not None:
                self.overflow_callback()
                self.overflow = True
            while len(self) > self.size_limit:
                self.popitem(last=False)
