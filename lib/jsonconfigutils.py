# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8



def getConfigValue(vconfig, value_path, defval=None, raise_on_error=False):
    try:
        first = True
        pathlist = value_path.split("/")
        for p in pathlist:
            if not p:
                continue

            if first:
                res = vconfig[p]
                first = False
            else:
                res = res[p]
        return res
    except:
        if not raise_on_error:
            return defval
        else:
            raise ValueError(f"can't read value at path: {value_path}, error access to {p}")
