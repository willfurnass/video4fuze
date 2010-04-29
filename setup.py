#!/usr/bin/env python
# -*- coding: utf-8 -*-

import info
from distutils.core import setup

setup(name=info.NAME,
       version=info.VERSION,
       description=info.SHORT_DES,
       url=info.URL,
       author_email=info.AUTHORS.split()[-1][1:-1],
       author=info.AUTHORS,
       license='GPLv3',
       data_files=[('share/video4fuze',
                   ['fuze.py',
                    'info.py', 
                    'p2fuze.py',
                    'video4fuze.pyw',
                    'video4fuze_rc.py',
                    'vthumb.py']),
                   ('share/video4fuze/translations',
                   ['translations/v4f_ca.qm',
                    'translations/v4f_de.qm',
                    'translations/v4f_en.qm',
                    'translations/v4f_es.qm']),
                   ('share/video4fuze/GUI',
                   ['GUI/AboutDiag.py',
                    'GUI/MainWindow.py',
                    'GUI/Ui_AboutDiag.py',
                    'GUI/Ui_MainWindow.py',
                    'GUI/Ui_Preferences.py',
                    'GUI/__init__.py',
                    'GUI/v4fPreferences.py']),
                   ('share/applications',
                   ['video4fuze.desktop']),
                   ('share/pixmaps',
                   ['icons/blackfuze.png']),
                   ('bin/',
                   ['dist/video4fuze',
		    'dist/fuze'])
    ]
)
