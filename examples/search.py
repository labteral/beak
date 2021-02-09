#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beak import Beak


for i, result in enumerate(Beak().search("query")):
    print(i, result)
