# -*- mode: python -*-

from kivy.deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(['C:\\Users\\Kivy\\Desktop\\Audica Maker\\source\\main.py'],
             pathex=['C:\\Users\\Kivy\\Desktop\\Audica Maker'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
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
          name='AudicaMaker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('C:\\Users\\Kivy\\Desktop\\Audica Maker\\source\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='AudicaMaker')
