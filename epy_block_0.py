"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import numpy 

class ImpedanceConverter(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Calculates capacitance or inductance from impedances. """
    Impedance = "Impedance (ohms)"
    Capacitance = "Capacitance (microfarads)"
    Inductance = "Inductance (microhenries)"
    def __init__(self, block_size=4096, samp_rate= 44100,  outputType=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Impedance to inductance or capacitance converter',   # will show up in GRC
            in_sig=[(np.float32, block_size)],
            out_sig=[(np.float32, block_size)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.block_size = block_size
        self.outputType = outputType
        self.samp_rate = samp_rate
        self.frequencies = numpy.arange(0,  self.block_size) * ((self.samp_rate/2)/self.block_size) * 2 * numpy.pi
        self.frequencies[0]=1

    def work(self, input_items, output_items):
        block = input_items[0].flatten(order='C')
        output_items[0][:] = self.calculateByOutputType(block)
        return len(output_items)

    def calculateByOutputType(self,  block):
        if self.outputType == self.Capacitance:
            return self.calculateCapacitanceFromImpedance(block)
        if self.outputType == self.Inductance:
            return self.calculateInductanceFromImpedance(block)
            
        #No idea what we got, return the data unmodified
        return block
    
    def calculateInductanceFromImpedance(self,  impedances):
        impedances[0] = 0
        inductance = 1000000 * impedances/self.frequencies
        return inductance
        
    def calculateCapacitanceFromImpedance(self,  impedances):
        impedances[0] = 1
        capacitance = 1000000/(self.frequencies*impedances)
        return capacitance
