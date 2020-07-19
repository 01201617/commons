# -*- mode: python -*-

block_cipher = None


a = Analysis(['accountabilitychart_v0_5.py'],
             pathex=['E:\\Nan\\PycharmProjects\\team_development\\mainthread_package\\tkinter_accountability','E:\\Nan\\PycharmProjects\\team_development'],
             binaries=[],
             datas=[],
             hiddenimports = ["pandas._libs.tslibs.timedeltas"],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='accountabilitychart_v0_5',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
