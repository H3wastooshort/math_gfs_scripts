#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import matplotlib

# ``bundle_files`` option explained:
# ===================================================
#
# The py2exe runtime *can* use extension module by directly importing
# the from a zip-archive - without the need to unpack them to the file
# system.  The bundle_files option specifies where the extension modules,
# the python dll itself, and other needed dlls are put.
#
# bundle_files == 3:
#     Extension modules, the Python dll and other needed dlls are
#     copied into the directory where the zipfile or the exe/dll files
#     are created, and loaded in the normal way.
#
# bundle_files == 2:
#     Extension modules are put into the library ziparchive and loaded
#     from it directly.
#     The Python dll and any other needed dlls are copied into the
#     directory where the zipfile or the exe/dll files are created,
#     and loaded in the normal way.
#
# bundle_files == 1:
#     Extension modules and the Python dll are put into the zipfile or
#     the exe/dll files, and everything is loaded without unpacking to
#     the file system.  This does not work for some dlls, so use with
#     caution.
#
# bundle_files == 0:
#     Extension modules, the Python dll, and other needed dlls are put
#     into the zipfile or the exe/dll files, and everything is loaded
#     without unpacking to the file system.  This does not work for
#     some dlls, so use with caution.


py2exe.freeze(
    console=["binom_graph.py","shrinking_rects.py","dice_server.py"],
    #data_files=matplotlib.get_py2exe_datafiles(),
    zipfile='pkg.zip',
    options={"py2exe": dict(
    packages = ['matplotlib','six','scipy','asyncio'],
    optimize=0,
    compressed=True,
    bundle_files=3,
    dist_dir='dist'
    )}
)
