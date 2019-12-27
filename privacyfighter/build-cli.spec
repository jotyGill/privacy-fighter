
a = Analysis(['pf.py'],
             pathex=[''],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             )
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          name='privacy-fighter-linux',
          debug=False,
          strip=None,
          upx=True,
          console=False)
