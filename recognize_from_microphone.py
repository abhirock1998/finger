import os
import sys
import libs
import libs.fingerprint as fingerprint
import argparse


from argparse import RawTextHelpFormatter
from itertools import izip_longest
from termcolor import colored
from libs.config import get_config
from libs.reader_microphone import MicrophoneReader
# from libs.visualiser_console import VisualiserConsole as visual_peak
# from libs.visualiser_plot import VisualiserPlot as visual_plot
from libs.db_sqlite import Database as SqliteDatabase



if __name__ == '__main__':
    config = get_config()

    db = SqliteDatabase()

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--seconds', nargs='?')
    args = parser.parse_args()

    if not args.seconds:
        parser.print_help()
        sys.exit(0)

    seconds = int(args.seconds)

    chunksize = 2**12  # 4096
    channels = 2#int(config['channels']) # 1=mono, 2=stereo

    record_forever = False
    visualise_console = bool(config['mic.visualise_console'])
    visualise_plot = bool(config['mic.visualise_plot'])

    reader = MicrophoneReader(None)


    reader.start_recording(seconds=seconds,
      chunksize=chunksize,
      channels=channels)
  
    msg = ' * started recording..'

    print(colored(msg, attrs=['dark']))

    while True:
        bufferSize = int(reader.rate / reader.chunksize * seconds)

        for i in range(0, bufferSize):
            nums = reader.process_recording()

            if visualise_console:
                msg = colored('   %05d', attrs=['dark']) + colored(' %s', 'green')
        # print (msg  % visual_peak.calc(nums))
            else:
                msg = '   processing %d of %d..' % (i, bufferSize)
                print (colored(msg, attrs=['dark']))

        if not record_forever: break

    if visualise_plot:
        data = reader.get_recorded_data()[0]
        visual_plot.show(data)   

        reader.stop_recording()

        msg = ' * recording has been stopped'

        print( colored(msg, attrs=['dark']) )
