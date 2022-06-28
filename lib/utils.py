# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os
import re


def __make_dir(apath):
    if not os.path.exists(apath):
        os.makedirs(apath)


def FilterListByMask(amask, alist):
    reslist = []
    pattern = re.compile(amask)

    for item in alist:
        match = bool(pattern.match(item))
        if match:
            reslist.append(item)
    return reslist


def create_dir(apath):
    if os.path.isdir(apath):
        __make_dir(apath)
    else:
        res = os.path.split(apath)
        for d in res:
            if d != ".":
                __make_dir(d)


def splitpath(apath):
    delimeters = {"/", "\\\\", '\\'}
    for delim in delimeters:
        if delim in apath:
            res = apath.split(delim)
            if not res[0]:
                res[0] = delim
            return res
