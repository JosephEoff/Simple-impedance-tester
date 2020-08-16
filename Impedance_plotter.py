#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Impedance Plotter
# Author: Joseph Eoff
# Generated: Sun Aug 16 16:01:09 2020
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
import walkingaverage
from gnuradio import qtgui


class Impedance_plotter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Impedance Plotter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Impedance Plotter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Impedance_plotter")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.smoothing = smoothing = 0.03
        self.series_resistor = series_resistor = 20
        self.samp_rate = samp_rate = 44100
        self.block_size = block_size = 8192

        ##################################################
        # Blocks
        ##################################################
        self._series_resistor_range = Range(0, 1000000, 1, 20, 50)
        self._series_resistor_win = RangeWidget(self._series_resistor_range, self.set_series_resistor, 'Series Resistor (ohms)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._series_resistor_win)
        self.walkingaverage = walkingaverage.blk(blocksize=block_size/2, averaging=smoothing, medianrank=101)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            block_size/2,
            0,
            (samp_rate/2)/(block_size/2),
            "Frequency (Hz)",
            "Impedance (ohms)",
            '',
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.01)
        self.qtgui_vector_sink_f_0.set_y_axis(0, series_resistor*2)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("Hz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("Ohms")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["black", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.fft_vxx_0_0 = fft.fft_vfc(block_size, True, (window.blackmanharris(block_size)), 1)
        self.fft_vxx_0 = fft.fft_vfc(block_size, True, (window.blackmanharris(block_size)), 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, block_size)
        self.blocks_sub_xx_0 = blocks.sub_ff(block_size)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, block_size/2)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, block_size)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, block_size)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(series_resistor)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_float, block_size/2, block_size, 0)
        self.blocks_divide_xx_0 = blocks.divide_ff(block_size)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(block_size)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(block_size)
        self.audio_source_0 = audio.source(samp_rate, 'sysdefault', False)
        self.audio_sink_0 = audio.sink(samp_rate, 'sysdefault', True)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.audio_sink_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.audio_source_0, 1), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.walkingaverage, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.walkingaverage, 0), (self.qtgui_vector_sink_f_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Impedance_plotter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_smoothing(self):
        return self.smoothing

    def set_smoothing(self, smoothing):
        self.smoothing = smoothing
        self.walkingaverage.averaging = self.smoothing

    def get_series_resistor(self):
        return self.series_resistor

    def set_series_resistor(self, series_resistor):
        self.series_resistor = series_resistor
        self.qtgui_vector_sink_f_0.set_y_axis(0, self.series_resistor*2)
        self.blocks_multiply_const_xx_0.set_k(self.series_resistor)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_vector_sink_f_0.set_x_axis(0, (self.samp_rate/2)/(self.block_size/2))

    def get_block_size(self):
        return self.block_size

    def set_block_size(self, block_size):
        self.block_size = block_size
        self.walkingaverage.blocksize = self.block_size/2
        self.qtgui_vector_sink_f_0.set_x_axis(0, (self.samp_rate/2)/(self.block_size/2))
        self.blocks_keep_m_in_n_0.set_m(self.block_size/2)
        self.blocks_keep_m_in_n_0.set_n(self.block_size)


def main(top_block_cls=Impedance_plotter, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
