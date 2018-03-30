import Weigtscale
import logging
import socket
import logging.handlers



def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])

 

LOG_FILENAME = "WeightScale.log"
ID = "W10"
USB_ADDRESS ='/dev/ttyUSB0'
SERI_NUMBER =9600
WEB_SERVER = 'http://10.0.201.104/JetsWMS/WgtScale/updateWeight.aspx'


logger = logging.getLogger()
logformatter = logging.Formatter('%(asctime)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                               maxBytes = 1024*1024*100,
                                               backupCount =3)
logger.setLevel(logging.DEBUG)
handler.setFormatter(logformatter)
logger.addHandler(handler)
oneWgtscale = Weigtscale.Wgtscale(ID,USB_ADDRESS,SERI_NUMBER,WEB_SERVER)

logger.debug('Start the program')
logger.info('Run Weightscale')
oneWgtscale.run()
logger.info('finished the program')
