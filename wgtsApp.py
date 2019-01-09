import Weightscale
import logging
import sys
import getopt
import logging.handlers
import logging
import serial

  



def main():
    LOG_FILENAME = "WeightScale.log"
    ID = "WS1"
    USB_ADDRESSES =['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyUSB4','/dev/ttyUSB5','/dev/ttyUSB6','/dev/ttyUSB7','/dev/ttyUSB8','/dev/ttyUSB9','/dev/ttyUSB10','end']
    SERI_NUMBER =9600
    WEB_ADDRESS ='10.0.201.104'
    logger = logging.getLogger()
    logformatter = logging.Formatter('%(asctime)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                   maxBytes = 1024*1024*100,
                                                   backupCount =3)
    logger.setLevel(logging.DEBUG)
    handler.setFormatter(logformatter)
    logger.addHandler(handler)
    #Get command line arguments
    argv = sys.argv[1:]

    try:
        opts,args = getopt.getopt(argv,"i:w:")
    except getopt.getoptError as err:
        print(err)
        logger.info(err)  
        opts =[]

    for opt,arg in opts:
        if opt in ['-i']:
             ID = arg
        elif opt in ['-w']:
             WEB_ADDRESS = arg
    logger.info('Respberry ID = {0}'.format(ID))  
    logger.info('Web Servers = {0}'.format(WEB_ADDRESS))
    logger.debug('Start the program')
    WEB_SERVER = 'http://' + WEB_ADDRESS + '/JetsWMS/WgtScale/updateWeight.aspx'
    print(WEB_SERVER)                    
    oneWgtscale = Weightscale.Wgtscale(ID,USB_ADDRESSES,SERI_NUMBER,WEB_SERVER)
    logger.info('Run Weightscale')
    oneWgtscale.run()
    logger.info('finished the program')
    

main()
