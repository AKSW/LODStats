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
import bitarray
from hashlib import md5
from LimitedSizeDict import LimitedSizeDict

# FIXME: does it help to build some small "md5-cache" for the last 1, 2, 3 strings?!

# subjects
distinct_subjects = LimitedSizeDict(size_limit=300000) # FIXME: make limit configurable
# 0: entities, 1: typed subjects, 2: labeled subjects

def query_distinct_subject(s, num_id):
    if len(s) > 16:
        s_hash = md5(s).digest()
    else:
        s_hash = s
    if distinct_subjects.has_key(s_hash):
        return distinct_subjects[s_hash][num_id]
    else:
        return False
        
def set_distinct_subject(s, num_id):
    if len(s) > 16:
        s_hash = md5(s).digest()
    else:
        s_hash = s
    if distinct_subjects.has_key(s_hash):
        distinct_subjects[s_hash][num_id] = True
    else:
        b_array = bitarray.bitarray(8)
        b_array[num_id] = True
        distinct_subjects[s_hash] = b_array

# subjects+predicate+object
distinct_spo = LimitedSizeDict(size_limit=300000) # FIXME: make limit configurable
# 0: properties, 1: classes, 2: classes defined

def query_distinct_spo(spo, num_id):
    if len(spo) > 16:
        spo_hash = md5(spo).digest()
    else:
        spo_hash = spo
    if distinct_spo.has_key(spo_hash):
        return distinct_spo[spo_hash][num_id]
    else:
        return False
        
def set_distinct_spo(spo, num_id):
    if len(spo) > 16:
        spo_hash = md5(spo).digest()
    else:
        spo_hash = spo
    if distinct_spo.has_key(spo_hash):
        distinct_spo[spo_hash][num_id] = True
    else:
        b_array = bitarray.bitarray(8)
        b_array[num_id] = True
        distinct_spo[spo_hash] = b_array
