import   GLOBALS                                              as     GB
import   pandas                                               as     pd
from     IPython.display                                      import display
import   time, os, sys, signal, threading, importlib
from     common_utils                                         import IDFromURI
from     colorama              import Fore, Back, Style
from     datetime                                             import datetime
from     dotenv                                               import load_dotenv
load_dotenv()

############    CFLIB_PATH è assoluto e va specificato nel file .env su ogni macchina
CFLIB_PATH         = os.environ.get('CFLIB_PATH')
# print(CFLIB_PATH)
sys.path = [CFLIB_PATH, *sys.path]                  ### Mette CFLIB_PATH all'inizio dele variabili d'ambiente

import cflib
import cflib.crtp

import   wakeUppatore, stenBaiatore, DataDrogno

oggieora   = str(datetime.now())                                              ### Crea stringa in formato yyyymmddhhmmss per creazione nome json
oggieora   = oggieora.replace('-', '')
oggieora   = oggieora.replace(' ', '')
oggieora   = oggieora.replace(':', '')
oggieora   = oggieora[:-7]

is_test_completed = False

def istanziaClassi():
    # cancellami = DataDrogno.dataDrone(IDFromURI('E7E7E7E7E1'),'E7E7E7E7E1')

    for uro in GB.available:
        iddio = IDFromURI(uro)
        GB.data_d[iddio] = DataDrogno.dataDrone(iddio, uro)
        GB.data_d[iddio].connect()

def scan_for_crazyflies():
    GB.available
    print(Fore.WHITE + "Scanning for available radios...")
    for i in GB.paginegialle:
        GB.available.extend(cflib.crtp.scan_interfaces(address=int(i, 16)))
    GB.available = list(filter(None, GB.available))
    GB.available = [x[0] for x in GB.available]
    print("\nTrovate %s radio!" %(len(GB.available)))
    for i in GB.available:
        print(i)
    print("\n")
    return GB.available

def check_if_test_is_completed():
    dati_mech = []                              ### Dati "elettromeccanici" dei droni
    dati_rev  = []                              ### Dati sulla "revisione del firmware"

   

    while not (all (GB.data_d[datadrogno].is_testing_over != False for datadrogno in GB.data_d)):
        time.sleep(1)
    is_test_completed = True
        

    for drogno in GB.data_d:
        i = 0
        data_mech = pd.DataFrame({'Indirizzo'              : [GB.data_d[drogno].link_uri], 
                                  'Battery Sag'            : [GB.data_d[drogno].battery_sag],
                                  'Battery Voltage'        : [GB.data_d[drogno].battery_voltage],
                                  'Battery Test Pass'      : [GB.data_d[drogno].battery_test_passed],
                                  'Propeller Test'         : [GB.data_d[drogno].propeller_test_result],
                                  'Propeller Test Pass'    : [GB.data_d[drogno].propeller_test_passed],
                                  'RSSI'                   : [GB.data_d[drogno].RSSI],
                                  'Bandwidth'              : ['%s pkg/s %s kB/s' %(float("{:.2f}".format(GB.data_d[drogno].bandwidth[0])), float("{:.2f}".format(GB.data_d[drogno].bandwidth[1])))],
                                  'Latency'                : ['%s ms' %float("{:.2f}".format(GB.data_d[drogno].latency))]},
                                  index                    = ['Drone ' + str(drogno)])
        dati_mech.append(data_mech)
        data_rev = pd.DataFrame({'Revisione Firmware (1)' : [GB.data_d[drogno].firmware_revision0],
                                 'Revisione Firmware (2)' : [GB.data_d[drogno].firmware_revision1]},
                                  index                   = ['Drone ' + str(drogno)])
        dati_rev.append(data_rev)
        i += 1
    try:
        df1 = pd.concat([drogno for drogno in dati_mech])
        df2 = pd.concat([drogno for drogno in dati_rev])
        display(df1)
        print()
        display(df2)
        df1.to_json(sys.path[3] + '/Test_Resultsss/Risultati_mech_' + oggieora + '.json', orient='index', indent=4)         ### Scrive un file json con i risultati
        df2.to_json(sys.path[3] + '/Test_resultsss/Risultati_rev_'  + oggieora + '.json', orient='index', indent=4)
        # df = df.align()
        print()
        print('tutti i test sono stati completati')
        time.sleep(2)
        print('sto per mettere a ninna tutti...')

        ### Aspetta finché il LED di ogni drone non ha finito di "lampeggiare"
        while not (all(GB.data_d[drogno].lampeggio_finito for drogno in GB.data_d)):
            time.sleep(0.5)
        print('addormento tutti... ')
        for drogno in GB.data_d:
            stenBaiatore.standBySingle(GB.data_d[drogno].link_uri)
    except ValueError:
        print('mi sa che \'sto test è ito buco')
        # sys.exit(0)
        os._exit(0)
        return