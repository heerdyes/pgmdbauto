@ECHO OFF
IF "%1"=="" GOTO continue
ECHO "filtering records from %1"
python xlfilter\xlfilter.py "%1" 5 300 400 > RSNs.txt
ECHO "beginning retrieval of time series records from PEERNGA database"
python pgmdbfind\pgmdbfind.py RSNs.txt 300 400
:continue
ECHO "**** DONE ****"

