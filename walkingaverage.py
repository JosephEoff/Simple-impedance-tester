"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import scipy.signal


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""
    
    def __init__(self, blocksize=4096, averaging=1.0, medianrank=51):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Walking average',   # will show up in GRC
            in_sig=[(np.float32, blocksize)],
            out_sig=[(np.float32, blocksize)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.averaging = averaging
        self.blocksize = blocksize
        self.lastblock = np.zeros(shape=(self.blocksize))
        self.medianrank = medianrank

    def work(self, input_items, output_items):
        newblock = scipy.signal.medfilt(input_items[0].flatten(order='C'),self.medianrank)
        self.lastblock = (newblock - self.lastblock ) * self.averaging + self.lastblock
        output_items[0][:] = self.lastblock        
        return len(output_items)
