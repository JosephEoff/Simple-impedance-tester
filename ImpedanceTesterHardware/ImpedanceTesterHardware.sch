EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text GLabel 2850 2950 0    50   Input ~ 0
Lineout_Left
Text GLabel 2850 3250 0    50   Input ~ 0
LineIn_Left
Text GLabel 2850 3750 0    50   Input ~ 0
LineIn_Right
Text GLabel 2850 4250 0    50   Input ~ 0
Ground
$Comp
L Device:R_US R_series
U 1 1 5F394605
P 3700 3500
F 0 "R_series" H 3768 3546 50  0000 L CNN
F 1 "20" H 3768 3455 50  0000 L CNN
F 2 "" V 3740 3490 50  0001 C CNN
F 3 "~" H 3700 3500 50  0001 C CNN
	1    3700 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:R DUT
U 1 1 5F394F82
P 3700 4000
F 0 "DUT" H 3770 4046 50  0000 L CNN
F 1 "Z?" H 3770 3955 50  0000 L CNN
F 2 "" V 3630 4000 50  0001 C CNN
F 3 "~" H 3700 4000 50  0001 C CNN
	1    3700 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 3750 3700 3750
Wire Wire Line
	3700 3750 3700 3850
Wire Wire Line
	3700 4150 3700 4250
Wire Wire Line
	3700 4250 2850 4250
Wire Wire Line
	2850 3250 3700 3250
Wire Wire Line
	3700 3250 3700 3350
Wire Wire Line
	3700 3650 3700 3750
Connection ~ 3700 3750
Wire Wire Line
	2850 2950 3700 2950
Wire Wire Line
	3700 2950 3700 3250
Connection ~ 3700 3250
$EndSCHEMATC
