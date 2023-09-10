from CrazyDG import CrazyDragon
from CrazyDG import Navigation
from CrazyDG import Controller
from CrazyDG import Recorder
from CrazyDG import utils

from cflib                         import crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils                   import uri_helper

from numpy import array, zeros
from numpy import frombuffer
from numpy import ndarray
from numpy import float32



nav_config = {
    'body_name': 'cf1',
    'header'   : array([20,23]),
    'pckt_size': 9
}

ctr_config = {
    'dt'       : 0.1,
    'n'        : 5,
    'header'   : array([23,20]),
    'pckt_size': 9
}

packet = zeros(nav_config['pckt_size'])


def transmit( _cf: CrazyDragon ):

    packet[0:3] = _cf.pos
    packet[3:6] = _cf.vel
    packet[6:9] = _cf.att

    return packet


def parser( recv_buff: list, recv_data: ndarray ):

    buff = recv_buff.pop(0)

    recv_data[:] = frombuffer( buff, dtype=float32 )


uri = uri_helper.uri_from_env( default='radio://0/80/2M/E7E7E7E702' )


if __name__ == "__main__":

    crtp.init_drivers()
    
    _cf = CrazyDragon()

    with SyncCrazyflie( uri, cf=_cf ) as scf:

        NAV = Navigation( _cf, nav_config )
        CTR = Controller( _cf, ctr_config )
        RCD = Recorder( _cf, CTR )

        NAV.connect( nav_config['header'], nav_config['pckt_size'] )
        NAV.transmit = transmit

        CTR.connect( ctr_config['header'], ctr_config['pckt_size'] )
        CTR.parser = parser

        NAV.start()
        CTR.start()
        RCD.start()

        ## your guidance function ##
        CTR.init_send_setpoint()
        ##       from here        ##

        input( "You can immediatly stop process with any key" )

        ############################

        CTR.stop_send_setpoint()

        NAV.join()
        CTR.join()
        RCD.join()

    NAV.qtm.close()