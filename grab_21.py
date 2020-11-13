  
from __future__ import print_function

import mil as MIL


def MGrab():
    # Allocate defaults.
    MilApplication = MIL.MappAlloc(MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilSystem = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_HOST, MIL.M_DEV0, MIL.M_DEFAULT, None)
    MilDisplay_0 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDisplay_1 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_0 = MIL.MdigAlloc(MilSystem, MIL.M_DEV0, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_1 = MIL.MdigAlloc(MilSystem, MIL.M_DEV1, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)

    SizeBand_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_BAND, None)
    SizeX_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    SizeBand_1 = MIL.MdigInquire(MilDigitizer_1, MIL.M_SIZE_BAND, None)
    SizeX_1 = MIL.MdigInquire(MilDigitizer_1, MIL.M_SIZE_X, None)
    SizeY_1 = MIL.MdigInquire(MilDigitizer_1, MIL.M_SIZE_Y, None)

    SizeBand_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_BAND, None)
    SizeX_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_Par = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    MilImageParent = MIL.MbufAllocColor(MilSystem, SizeBand_Par, SizeX_0 + SizeX_1, SizeY_Par, 8 + MIL.M_UNSIGNED, MIL.M_IMAGE + MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB, None)



    # MilImageDisp_0 = MIL.MbufAllocColor(MilSystem,
    #                                   SizeBand_0,
    #                                   SizeX_0,
    #                                   SizeY_0,
    #                                   8 + MIL.M_UNSIGNED,
    #                                   MIL.M_IMAGE +
    #                                   MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB,
    #                                   None)

    MilImageDisp_0 = MIL.MbufChildColor2d(MilImageParent,
                                      SizeBand_0,
                                      0,0,
                                      SizeX_0,
                                      SizeY_0,
                                      None)

    MIL.MbufClear(MilImageDisp_0, MIL.M_COLOR_BLACK)

    # MilImageDisp_1 = MIL.MbufAllocColor(MilSystem,
    #                                     SizeBand_1,
    #                                     SizeX_1,
    #                                     SizeY_1,
    #                                     8 + MIL.M_UNSIGNED,
    #                                     MIL.M_IMAGE +
    #                                     MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB,
    #                                     None)

    MilImageDisp_1 = MIL.MbufChildColor2d(MilImageParent,
                                      SizeBand_0,
                                      2592,0,
                                      SizeX_0,
                                      SizeY_0,
                                      None)

    MIL.MbufClear(MilImageDisp_1, MIL.M_COLOR_BLACK)
    MIL.MdispSelect(MilDisplay_0, MilImageDisp_0)
    MIL.MdispSelect(MilDisplay_1, MilImageDisp_1)

    # Print a message.
    print("-----------------------------\n")

    for i in range(100):
        MIL.MdigGrabContinuous(MilDigitizer_0, MilImageDisp_0)
        MIL.MdigGrabContinuous(MilDigitizer_1, MilImageDisp_1)

        # Halt continuous grab.
        MIL.MdigHalt(MilDigitizer_0)
        MIL.MdigHalt(MilDigitizer_1)
        # MIL.MbufExport(MIL.MIL_TEXT("0_FileName{i}.tif".format(i=i)), MIL.M_TIFF, MilImageDisp_0)
        # MIL.MbufExport(MIL.MIL_TEXT("1_FileName{i}.tif".format(i=i)), MIL.M_TIFF, MilImageDisp_1)
        MIL.MbufExport(MIL.MIL_TEXT("F_FileName{i}.tif".format(i=i)), MIL.M_TIFF, MilImageParent)

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


if __name__ == "__main__":
    MGrab()