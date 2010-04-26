#!/usr/bin/env python

import video4fuze
from distutils.core import setup

setup (name=video4fuze.NAME,
       version=video4fuze.VERSION,
       description=video4fuze.SHORT_DES,
       url=video4fuze.URL,
       author_email=video4fuze.AUTHORS.split()[-1][1:-1],
       author=video4fuze.AUTHORS,
       license=['GPLv3'],
       data_files=[('share/video4fuze',
                   ['fuze.py',
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
		   ['dist/video4fuze'])
		   ]
	)
