# -*- mode: python ; coding: utf-8 -*-

import os
import importlib

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Kort\\Documents\\GitHub\\ocm\\app'],
             binaries=[],
             datas=[
                 (os.path.join(os.path.dirname(importlib.import_module('tensorflow').__file__),"lite/experimental/microfrontend/python/ops/_audio_microfrontend_op.so"),"tensorflow/lite/experimental/microfrontend/python/ops/"),
                 ('rede/checkpoint','rede'),
                 ('rede/Teste 38.data-00000-of-00001','rede'),
                 ('rede/Teste 38.index','rede')
                 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='OCM',
          icon = 'icons/app_icon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
