

@ECHO OFF

::path to python tool scripts
 SET MSC_PY_TOOLS=..\python\

:: get full path to python script
 SET CD_BCK=
 SET CD_BCK=%CD%
 
 cd %MSC_PY_TOOLS%
 SET MSC_PY_TOOLS=%cd%
 
 cd %CD_BCK%

@ECHO ***  MSC_PY_TOOLS: %MSC_PY_TOOLS%



:: Content of the Acc_Sensors_all.txt
:: 1st line: path to *.res file
:: 2nd line: flag header - 1=write header to the 1st line, 0=no header line
:: 3rd line: flag magnitude - 1=compute magnitude of vector (out of the last 3 components), 0=no magnitude
:: 4th line: path to ascii output file (nr1)
:: 5th line: components list (nr1)
:: 6th line: components ucf list (nr1)
:: 7th line: path to ascii output file (nr2)
:: 8th line: components list (nr2)
:: 9th line: components ucf list (nr2)


:: components list example
:: time.TIME Dyno_Measurements.Motor_Speed gear_force_cyl_Kinematics.pinion_TE_Angle gear_force_cyl_Kinematics.Wheel_TE_Angle

:: components ucf list example
:: Set Time unit consitency factor to go from model to desired units : model in millimeter, milliseconds -> millimeter, seconds: TIME_UCF=1.0E-3, Motor_Speed_UCF=1.0, ACC_UCF=1.0E+6
:: 1.0E-3 1.0 1.0E+6 1.0E+6 1.0E+6
:: Set Time unit consitency factor to go from model to desired units : model in millimeter,      seconds -> millimeter, seconds: TIME_UCF=1.0,    Motor_Speed_UCF=1.0, ACC_UCF=1.0
:: 1.0 1.0 1.0 1.0 1.0


@ECHO *
@ECHO *********************************************************************************
@ECHO ***  Current Working Directory: %CD%
@ECHO *********************************************************************************
@ECHO *
@ECHO *
@echo ***************************************************************************
@echo *********  Extracting Transmission Error results
@echo ***************************************************************************
@ECHO *
@ECHO *

call adams2023_3 python %MSC_PY_TOOLS%\xml_res_reader_ucf.py %CD%\ad002c_script.txt

 SET MSC_PY_TOOLS=

IF NOT DEFINED MASTER_BAT pause
