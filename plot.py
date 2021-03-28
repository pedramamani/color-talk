from graph import Graph
import os
import pathlib
import numpy as np
import regex
import matplotlib.pyplot as plt

DIR = pathlib.Path(os.path.dirname(__file__))
NAME = os.path.basename(DIR)
ASSETS_DIR = DIR / 'assets'

floatGroup = lambda name: f'(?P<{name}>[0-9.E-]*)'
FORMAT_2 = f"({floatGroup('w')} {floatGroup('x')}\n)+$"
FORMAT_4 = f"({floatGroup('w')} {floatGroup('x')} {floatGroup('y')}( {floatGroup('z')})?\n)+$"


def extractData(filePath, format_):
    filePath = str(filePath)
    with open(filePath, 'r') as file:
        content = file.read()
    match = regex.match(format_, content)
    assert match is not None, f'File "{filePath}" contents do not match given format.'
    return (np.array([float(v) for v in match.captures(n)]) for n in match.groupdict().keys())


if __name__ == '__main__':
    plt.style.use('dark_background')

    g = Graph()
    w2, x2 = extractData(ASSETS_DIR / '2deg-luminous-efficiency.csv', FORMAT_2)
    w10, x10 = extractData(ASSETS_DIR / '10deg-luminous-efficiency.csv', FORMAT_2)
    g.line(w2, x2, width=1.5)
    g.line(w10, x10, width=1.5, format_='--')
    g.show(xLabel='Wavelength (nm)', yLabel='Sensitivity', showGrid=True, gridColor=(0.3, 0.3, 0.3),
           legend=['2$^\circ$', '10$^\circ$'])

    g = Graph()
    w, x, y, z = extractData(ASSETS_DIR / '2deg-lms-fundamentals.csv', FORMAT_4)
    g.line(w, x, width=1.5, color='r')
    g.line(w, y, width=1.5, color='g')
    g.line(w[:len(z)], z, width=1.5, color='b')
    g.show(xLabel='Wavelength (nm)', yLabel='Sensitivity', showGrid=True, gridColor=(0.3, 0.3, 0.3),
           legend=['L', 'M', 'S'])
