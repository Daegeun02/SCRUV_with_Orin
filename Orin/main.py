from CrazyDG import CrazyDragon
from CrazyDG import Guidance
from CrazyDG import utils

from numpy import array, zeros



config = {

}

def transmit():
    pass


def parser():
    pass


if __name__ == "__main__":

    _cf = CrazyDragon()

    GUD = Guidance( config )

    GUD.transmit = transmit
    GUD.parser   = parser

    GUD.start()

    ###      Guidance Loop    ###
    ## _cf.command = somethine ##
    ### ###