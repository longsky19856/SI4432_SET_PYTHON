# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['E:\\mywork\\python\\\xb2\xc9\xbc\xaf\xb5\xa5\xd4\xaa\xb2\xce\xca\xfd\xc9\xe8\xd6\xc3'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='main')
