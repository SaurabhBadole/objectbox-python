# Copyright 2019-2023 ObjectBox Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from objectbox.box import Box
from objectbox.builder import Builder
from objectbox.model import Model
from objectbox.store import Store
from objectbox.objectbox import ObjectBox
from objectbox.c import NotFoundException, version_core
from objectbox.version import Version

__all__ = [
    'Box',
    'Builder',
    'Model',
    'Store',
    'ObjectBox',
    'NotFoundException',
    'version',
    'version_info',
]

# Python binding version
version = Version(0, 7, 0, alpha=9)


def version_info():
    return "ObjectBox Python version " + str(version) + " using dynamic library version " + str(version_core)
