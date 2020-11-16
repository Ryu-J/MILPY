from __future__ import print_function

import mil as MIL
import os
import sys
import serial

def MGrab(ScannerID, nImage):
    ## Directory Check
    rootdir = "Scanner/{}".format(ScannerID)
    try:
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
    except OSError:
        print('Error: Creating directory. ' + rootdir)

    # Allocate defaults.
    MilApplication = MIL.MappAlloc(MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    ID = int(ScannerID)
    MilSystem = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_SOLIOS, ID, MIL.M_DEFAULT, None)
 #   MilSystem_1 = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_SOLIOS, MIL.M_DEV0, MIL.M_DEFAULT, None)
 #   MilSystem_2 = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_SOLIOS, MIL.M_DEV0, MIL.M_DEFAULT, None)
    MilDisplay_0 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDisplay_1 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_0 = MIL.MdigAlloc(MilSystem, MIL.M_DEV0, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_1 = MIL.MdigAlloc(MilSystem, MIL.M_DEV1, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)

    SizeX_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    SizeX_1 = MIL.MdigInquire(MilDigitizer_1, MIL.M_SIZE_X, None)
    SizeY_1 = MIL.MdigInquire(MilDigitizer_1, MIL.M_SIZE_Y, None)

    SizeBand_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_BAND, None)
    SizeX_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    MilImageParent = MIL.MbufAllocColor(MilSystem, 
                                        SizeBand_Par, 
                                        SizeX_Par*2, 
                                        SizeY_Par, 
                                        8 + MIL.M_UNSIGNED, 
                                        MIL.M_IMAGE + MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB, 
                                        None)

    MIL.MbufClear(MilImageParent, MIL.M_COLOR_BLACK)

    MilImageDisp_0 = MIL.MbufChildColor2d(MilImageParent,
                                      MIL.M_ALL_BANDS,
                                      0,0,
                                      SizeX_0,
                                      SizeY_0,
                                      None)

    MIL.MbufClear(MilImageDisp_0, MIL.M_COLOR_BLACK)

    MilImageDisp_1 = MIL.MbufChildColor2d(MilImageParent,
                                      MIL.M_ALL_BANDS,
                                      SizeX_0,0,
                                      SizeX_1,
                                      SizeY_1,
                                      None)

    MIL.MbufClear(MilImageDisp_1, MIL.M_COLOR_BLACK)
    MIL.MdispSelect(MilDisplay_0, MilImageDisp_0)
    MIL.MdispSelect(MilDisplay_1, MilImageDisp_1)

    # Print a message.
    print("-----------------------------\n")

    for i in range(nImage):
        MIL.MdigGrabContinuous(MilDigitizer_0, MilImageDisp_0)
        MIL.MdigGrabContinuous(MilDigitizer_1, MilImageDisp_1)

        # Halt continuous grab.
        MIL.MdigHalt(MilDigitizer_0)
        MIL.MdigHalt(MilDigitizer_1)
        MIL.MbufExport(MIL.MIL_TEXT("{}/F_FileName{i}.tif".format(rootdir, i=i)), MIL.M_TIFF, MilImageParent)

    MIL.MbufFree(MilImageDisp_0)
    MIL.MbufFree(MilImageDisp_1)
    MIL.MbufFree(MilImageParent)
    MIL.MdispFree(MilDisplay_0)
    MIL.MdispFree(MilDisplay_1)
    MIL.MdigFree(MilDigitizer_0)
    MIL.MdigFree(MilDigitizer_1)
    MIL.MsysFree(MilSystem)
    MIL.MappFree(MilApplication)

    return

def ScanIDtoPort(scanID):
    portarray = { "0":[7, 5], "1":[8, 3], "2":[6, 4]}
    return portarray[scanID]

def TurnOn(scanID):
    print("Scanner {} Turn on ".format(scanID))
    Ports = ScanIDtoPort(scanID)
    for port in Ports:
        sendsignal(port, 'vp')
    return

def TurnOff(scanID):
    print("Scanner {} Turn on ".format(scanID))
    Ports = ScanIDtoPort(scanID)
    for port in Ports:
        sendsignal(port, 'sp')
    return

def sendsignal(port, command):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM{}'.format(port)  # counter for port name starts at 0

    # check to see if port is open or closed
    if (ser.isOpen() == False):
        print('The Port COM{} is Open '.format(port))
        # timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print('The Port %d is closed' % COMPORT)
    ser.write(b'{}\r\n'.format(command))
    print('Send Signal:{} {}'.format(COMPORT, command))
    ser.close()


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) >= 3 :
        command = sys.argv[1]
        print("Command: {}".format(command))
        scanID = sys.argv[2]
        if ( command == "scan") :
            MGrab(scanID, 100)
        if ( command == "turnon") :
            TurnOn(scanID)
        if ( command == "turnoff"):
            TurnOff(scanID)

