# -*- mode: python -*-

block_cipher = None

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

def get_plt_path():
    import matplotlib
    plt_path = matplotlib.__path__[0]
    return plt_path

a = Analysis(['test_fileope_190428.py'],
             pathex=['E:\\Nan\\PycharmProjects\\team_development\\testcode'],
             binaries=[],
             datas=[('E:\\Nan\\Anaconda3\\Library\\bin\\mkl_avx2.dll','.'),
                        ('E:\\Nan\\Anaconda3\\Library\\bin\\mkl_def.dll','.')],

             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

dict_tree = Tree(get_plt_path(), prefix='matplotlib', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'matplotlib' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='test_fileope_190428',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
