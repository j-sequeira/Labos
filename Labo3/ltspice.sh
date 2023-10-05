#!/bin/bash

LTSPICE_PATH='/home/seke/.wine/drive_c/users/seke/Local Settings/Application Data/Programs/ADI/LTspice/LTspice.exe'

LTSPICE_CIRCUIT='/home/seke/.wine/drive_c/users/seke/Local Settings/Application Data/LTspice/Draft1.asc'

OUTPUT_DIR='/home/seke/Labos/Labo3'

FREQUENCY='1kHz' 
TIME_INTERVAL="0.01s"
MAX_TIME_STEP="0.1us"

wine "$LTSPICE_PATH" -b -Run -a -o "$OUTPUT_DIR/$FREQUENCY.txt" -tf "$TIME_INTERVAL" -maxstep "$MAX_TIME_STEP" "$LTSPICE_CIRCUIT"

grep -E "^V\(in\)" "$OUTPUT_DIR/$FREQUENCY.txt" | awk '{print $2, $3}' > "$OUTPUT_DIR/V_in_$FREQUENCY.txt"
grep -E "^V\(out\)" "$OUTPUT_DIR/$FREQUENCY.txt" | awk '{print $2, $3}' > "$OUTPUT_DIR/V_out_$FREQUENCY.txt"