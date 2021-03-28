import matplotlib.pyplot as plt
import matplotlib
import datetime
import numpy as np
import seaborn

PALETTE = 'husl'
COLOR = (0, 0, 0)
GRID_COLOR = (0.85, 0.85, 0.85)
SHADE_OPACITY = 0.2
TITLE_FONT_SIZE = 16
LABEL_FONT_SIZE = 12
ANNOTATE_FONT_SIZE = 10

ASPECT_RATIO = 'auto'
INTERPOLATION = 'none'
SCALE = 'linear'
INITIAL_Z_ORDER = 2
LINE_WIDTH = 1.0
MARKER_SIZE = 5
FIGURE_SIZE = (6, 4)
MARGINS = (0, 0.1)
DPI = 120
SAVE_DPI = 200


class Graph:
    def __init__(self, size=FIGURE_SIZE, titleFontSize=TITLE_FONT_SIZE, labelFontSize=LABEL_FONT_SIZE):
        self.figure = plt.figure(figsize=size, dpi=DPI, tight_layout=True)
        self.axes = plt.gca()
        self.titleFontSize = titleFontSize
        self.labelFontSize = labelFontSize
        self.zOrder = INITIAL_Z_ORDER

    def line(self, x, y, format_=None, width=LINE_WIDTH, color=None, markerSize=MARKER_SIZE, markerColor=None):
        format_ = '' if format_ is None else format_
        self.axes.plot(x, y, format_, color=color, linewidth=width, markersize=markerSize,
                       markeredgecolor=markerColor, markerfacecolor=markerColor,
                       zorder=self.zOrder)
        self.zOrder += 1
        return self

    def errorLine(self, x, y, yError, format_=None, width=LINE_WIDTH, color=None, markerSize=MARKER_SIZE,
                  markerColor=None):
        format_ = '' if format_ is None else format_
        self.axes.errorbar(x, y, yError, fmt=format_, color=color, linewidth=width, markersize=markerSize,
                           markeredgecolor=markerColor, markerfacecolor=markerColor, zorder=self.zOrder)
        self.zOrder += 1
        return self

    def bar(self, x, y, width=None, color=None):
        x = np.array(x)
        width = (1 if width is None else width) * np.average(x[1:] - x[:-1])
        self.axes.bar(x, y, width=width, color=color, zorder=self.zOrder)
        self.zOrder += 1
        return self

    def shade(self, x, yLower, yUpper, color=None):
        color = COLOR if color is None else matplotlib.colors.to_rgb(color)
        color = (*color, SHADE_OPACITY)
        self.axes.fill_between(x, yLower, yUpper, facecolor=color, zorder=self.zOrder)
        self.zOrder += 1
        return self

    def image(self, data, label=None, flip=False, extent=None, aspectRatio=ASPECT_RATIO, interpolation=INTERPOLATION):
        if flip:
            data = np.flip(data, axis=0)
        with seaborn.color_palette(PALETTE):
            image = self.axes.imshow(data, extent=extent, aspect=aspectRatio, interpolation=interpolation,
                                     zorder=self.zOrder)
        colorBar = self.figure.colorbar(image)
        colorBar.set_label(label, fontsize=self.labelFontSize)
        colorBar.ax.tick_params(labelsize=self.labelFontSize)
        self.zOrder += 1
        return self

    def annotate(self, labels, x, y, offset=(0, 0), color=None, rotation=0, fontSize=ANNOTATE_FONT_SIZE):
        for label, x_, y_ in zip(labels, x, y):
            self.axes.annotate(label, (x_, y_), xytext=offset, textcoords='offset points', ha='center', va='center',
                               color=color, rotation=rotation, size=fontSize, zorder=self.zOrder)
        self.zOrder += 1
        return self

    def xTicks(self, x, labels):
        self.axes.xticks(x, labels)
        return self

    def yTicks(self, y, labels):
        self.axes.yticks(y, labels)
        return self

    def show(self, legend=None, xLabel=None, yLabel=None, xRange=None, yRange=None, xScale=SCALE, yScale=SCALE,
             title=None, margins=MARGINS, showGrid=False, gridColor=GRID_COLOR, windowName=None):
        legend = self._formatLegend(legend)
        if legend is not None:
            self.axes.legend(legend, fontsize=self.labelFontSize)
        if yRange is not None:
            self.axes.ylim(yRange)
        if xRange is not None:
            self.axes.xlim(xRange)
        if showGrid:
            self.axes.grid(color=gridColor, which='both')
        self.axes.set_xlabel(xLabel, fontsize=self.labelFontSize)
        self.axes.set_ylabel(yLabel, fontsize=self.labelFontSize)
        self.axes.tick_params(labelsize=self.labelFontSize)
        self.axes.set_xscale(xScale)
        self.axes.set_yscale(yScale)

        self.axes.set_title(title, fontsize=self.titleFontSize)
        self.figure.canvas.set_window_title(self._windowName() if windowName is None else windowName)
        self.axes.margins(*margins)
        plt.show()
        return self

    def save(self, filePath):
        self.figure.savefig(filePath, dpi=SAVE_DPI, bbox_inches='tight')
        return self

    @staticmethod
    def _formatLegend(legend):
        if (legend is None) or (type(legend) is str):
            return None
        return [('_nolegend_' if v is None else v) for v in legend]

    @staticmethod
    def _windowName():
        return f'Figure {datetime.datetime.now().strftime("%y-%m-%d %H%M%S")}'
