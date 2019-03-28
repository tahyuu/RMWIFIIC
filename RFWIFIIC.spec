# -*- mode: python -*-

block_cipher = None


a = Analysis(['RFWIFIIC.py',
              'Comm232.py',
              'Log.py',
              'Configure.py',
              'Color.py'],
             pathex=['D:\\WorkSpace\\RFWIFIIC'],
             binaries=[],
             datas=[],
             hiddenimports=['pyserial'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='RFWIFIIC',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='RFWIFIIC')
