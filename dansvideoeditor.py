import itertools
import os
import subprocess

TMP_PATH = '.dansvideoeditor-tmp.txt'

def reset():
    _Element._elements = {}

# elements
def _element(name):
    return _Element._elements[name]

def _vlink(name):
    if name == None: return ''
    if name in _Element._links: return f'[{name}]'
    return _element(name).vlink()

def _alink(name):
    if name == None: return ''
    if name in _Element._links: return f'[{name}]'
    return _element(name).alink()

class _Element:
    def __init__(self, name):
        self.name = name
        if name in _Element._elements:
            raise Exception(f'name {name} already taken')
        _Element._elements[name] = self

    _elements = {}
    _links = set()

class _VElement(_Element):
    def vlink(self):
        return f'[{self.name}]'

class _VAElement(_Element):
    def vlink(self):
        return f'[{self.name}__v]'

    def alink(self):
        return f'[{self.name}__a]'

# input file
class Ifile(_Element):
    def __init__(self, name, path, start=None, end=None):
        _Element.__init__(self, name)
        self.path = path
        self.start = start
        self.end = end

    def set_index(self, index):
        self._index = index

    def index(self):
        return self._index

    def vlink(self):
        return f'[{self.index()}:v:0]'

    def alink(self):
        return f'[{self.index()}:a:0]'

    def get_dims(self):
        w, h = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                self.path,
            ],
            check=True,
            capture_output=True,
        ).stdout.decode('utf-8').strip().split(',')
        return (int(w), int(h))

# filters
class _Filter: pass

class Concat(_VAElement, _Filter):
    def __init__(self, name, ivnames, ianames=None):
        _Element.__init__(self, name)
        self.ivnames = ivnames
        if ianames == None:
            self.ianames = ivnames
        else:
            self.ianames = ianames

    def _filter(self):
        return ''.join([
            *[
                f'{_vlink(vname)}{_alink(aname)}'
                for vname, aname
                in itertools.zip_longest(self.ivnames, self.ianames)
            ],
            f'concat={len(self.ivnames)}:1:{1 if self.ianames else 0}',
            self.vlink(),
            self.alink() if self.ianames else '',
        ])

class Scale(_VElement, _Filter):
    def __init__(self, name, iname, x, y):
        _Element.__init__(self, name)
        self.iname = iname
        self.x = x
        self.y = y

    def _filter(self):
        return (
            f'{_vlink(self.iname)}'
            f'scale={self.x}:{self.y}'
            f'{self.vlink()}'
        )

class Pad(_VElement, _Filter):
    def __init__(self, name, iname, w='iw', h='ih', x=0, y=0):
        _Element.__init__(self, name)
        self.iname = iname
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def _filter(self):
        return (
            f'{_vlink(self.iname)}'
            f'pad={self.w}:{self.h}:{self.x}:{self.y}'
            f'{self.vlink()}'
        )

class Crop(_VElement, _Filter):
    def __init__(self, name, iname, w, h, x=None, y=None):
        _Element.__init__(self, name)
        self.iname = iname
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def _filter(self):
        x = f':x={self.x}' if self.x != None else ''
        y = f':y={self.y}' if self.y != None else ''
        return ''.join([
            f'{_vlink(self.iname)}',
            f'crop=w={self.w}:h={self.h}{x}{y}',
            f'{self.vlink()}',
        ])

class SetSar(_VElement, _Filter):
    def __init__(self, name, iname, sar):
        _Element.__init__(self, name)
        self.iname = iname
        self.sar = sar

    def _filter(self):
        return (
            f'{_vlink(self.iname)}'
            f'setsar={self.sar}'
            f'{self.vlink()}'
        )

class Split(_VElement, _Filter):
    def __init__(self, iname, n, names=None):
        _Element.__init__(self, f'{iname}_split')
        self.iname = iname
        self.n = n
        self.names = names or [f'{iname}_{i}' for i in range(n)]
        for name in self.names: _Element._links.add(name)

    def _filter(self):
        return ''.join([
            _vlink(self.iname),
            f'split={self.n}',
            *[_vlink(name) for name in self.names],
        ])

class Hstack(_VElement, _Filter):
    def __init__(self, name, inames, shortest=False):
        _Element.__init__(self, name)
        self.inames = inames
        self.shortest = 1 if shortest else 0

    def _filter(self):
        return ''.join([
            *[f'{_vlink(name)}' for name in self.inames],
            f'hstack={len(self.inames)}:{self.shortest}',
            self.vlink(),
        ])

class Vstack(_VElement, _Filter):
    def __init__(self, name, inames, shortest=False):
        _Element.__init__(self, name)
        self.inames = inames
        self.shortest = 1 if shortest else 0

    def _filter(self):
        return ''.join([
            *[f'{_vlink(name)}' for name in self.inames],
            f'vstack={len(self.inames)}:{self.shortest}',
            self.vlink(),
        ])

# invocations
def concat_copy(ifile_names, opath='output.mov'):
    with open(TMP_PATH, 'w') as file:
        for name in ifile_names:
            ifile = _element(name)
            file.write(f'file {ifile.path}\n')
            if ifile.start != None:
                file.write(f'inpoint {ifile.start}\n')
            if ifile.end != None:
                file.write(f'outpoint {ifile.end}\n')
    subprocess.run(
        [
            'ffmpeg',
            '-f', 'concat',  # use the concat demuxer
            '-safe', '0',  # allow absolute file paths
            '-i', TMP_PATH,
            '-codec', 'copy',
            opath,
        ],
        check=True,
    )

def render(opath, vname, aname):
    ifile_options = []
    index = 0
    for element in _Element._elements.values():
        if isinstance(element, Ifile):
            if element.start != None:
                ifile_options.extend(['-ss', str(element.start)])
            if element.end != None:
                ifile_options.extend(['-t', str(element.end - (element.start or 0))])
            ifile_options.extend(['-i', element.path])
            element.set_index(index)
            index += 1
    filters = []
    for element in _Element._elements.values():
        if isinstance(element, _Filter):
            filters.append(element._filter())
    print('----- filter graph -----')
    for filter in filters: print(filter)
    print('\n----- ffmpeg -----')
    subprocess.run(
        [
            'ffmpeg',
            *ifile_options,
            '-filter_complex', ';'.join(filters),
            '-map', _vlink(vname),
            '-map', _alink(aname),
            opath,
        ],
        check=True,
    )

def concat_center(ifile_names, width=None, height=None, opath='output.mov'):
    if width == None or height == None:
        width, height = _element(ifile_names[0]).get_dims()
    vnames = []
    anames = []
    m = rf'min({width}/iw\,{height}/ih)'  # so that reshaped is as big as possible without clipping
    for name in ifile_names:
        Scale(f'_s_{name}', name, f'iw*{m}', f'ih*{m}')  # scale by factor of m
        Pad(f'_p_{name}', f'_s_{name}', width, height, f'({width}-iw*{m})/2', f'({height}-ih*{m})/2')  # center
        SetSar(f'_ss_{name}', f'_p_{name}', 1)  # force SAR to 1 (is this gonna be an issue?)
        vnames.append(f'_ss_{name}')
        anames.append(name)
    Concat('_c', vnames, anames)
    render(opath, '_c', '_c')
