#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Impedance Plotter
# Author: Joseph Eoff
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import epy_block_0
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

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.smoothing = smoothing = 0.03
        self.series_resistor = series_resistor = 20
        self.samp_rate = samp_rate = 44100
        self.calculation_type = calculation_type = 'Impedance (ohms)'
        self.block_size = block_size = 8192

        ##################################################
        # Blocks
        ##################################################
        self._series_resistor_range = Range(0, 100000, 0.01, 20, 50)
        self._series_resistor_win = RangeWidget(self._series_resistor_range, self.set_series_resistor, 'Series Resistor (ohms)', "counter", float)
        self.top_grid_layout.addWidget(self._series_resistor_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._calculation_type_options = ('Impedance (ohms)', 'Capacitance (microfarads)', 'Inductance (microhenries)', )
        # Create the labels list
        self._calculation_type_labels = ('Impedance (ohms)', 'Capacitance (microfarads)', 'Inductance (microhenries)', )
        # Create the combo box
        self._calculation_type_tool_bar = Qt.QToolBar(self)
        self._calculation_type_tool_bar.addWidget(Qt.QLabel('Type' + ": "))
        self._calculation_type_combo_box = Qt.QComboBox()
        self._calculation_type_tool_bar.addWidget(self._calculation_type_combo_box)
        for _label in self._calculation_type_labels: self._calculation_type_combo_box.addItem(_label)
        self._calculation_type_callback = lambda i: Qt.QMetaObject.invokeMethod(self._calculation_type_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._calculation_type_options.index(i)))
        self._calculation_type_callback(self.calculation_type)
        self._calculation_type_combo_box.currentIndexChanged.connect(
            lambda i: self.set_calculation_type(self._calculation_type_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._calculation_type_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.walkingaverage = walkingaverage.blk(block_size=int(block_size/2), averaging=smoothing, medianrank=101)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            int(block_size/2),
            0,
            (samp_rate/2)/(block_size/2),
            "Frequency (Hz)",
            calculation_type,
            '',
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.01)
        self.qtgui_vector_sink_f_0.set_y_axis(0, series_resistor*2)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("Hz")
        self.qtgui_vector_sink_f_0.set_y_axis_units(calculation_type)
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["black", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 1, 0, 4, 5)
        for r in range(1, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_vxx_0_0 = fft.fft_vfc(block_size, True, window.blackmanharris(block_size), 1)
        self.fft_vxx_0 = fft.fft_vfc(block_size, True, window.blackmanharris(block_size), 1)
        self.epy_block_0 = epy_block_0.ImpedanceConverter(block_size=int(block_size/2), samp_rate=samp_rate, outputType=calculation_type)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, block_size)
        self.blocks_sub_xx_0 = blocks.sub_ff(block_size)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, int(block_size/2))
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, block_size)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, block_size)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(series_resistor, 1)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_float, int(block_size/2), block_size, 0)
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
        self.connect((self.epy_block_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.walkingaverage, 0), (self.epy_block_0, 0))


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
        self.blocks_multiply_const_xx_0.set_k(self.series_resistor)
        self.qtgui_vector_sink_f_0.set_y_axis(0, self.series_resistor*2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.epy_block_0.samp_rate = self.samp_rate
        self.qtgui_vector_sink_f_0.set_x_axis(0, (self.samp_rate/2)/(self.block_size/2))

    def get_calculation_type(self):
        return self.calculation_type

    def set_calculation_type(self, calculation_type):
        self.calculation_type = calculation_type
        self._calculation_type_callback(self.calculation_type)
        self.epy_block_0.outputType = self.calculation_type
        self.qtgui_vector_sink_f_0.set_y_axis_units(self.calculation_type)

    def get_block_size(self):
        return self.block_size

    def set_block_size(self, block_size):
        self.block_size = block_size
        self.blocks_keep_m_in_n_0.set_m(int(self.block_size/2))
        self.blocks_keep_m_in_n_0.set_n(self.block_size)
        self.epy_block_0.block_size = int(self.block_size/2)
        self.qtgui_vector_sink_f_0.set_x_axis(0, (self.samp_rate/2)/(self.block_size/2))
        self.walkingaverage.block_size = int(self.block_size/2)





def main(top_block_cls=Impedance_plotter, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
