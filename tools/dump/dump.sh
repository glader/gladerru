#!/bin/sh

FILE="`date +%%Y%%m%%d_%%H%%M`"
ARCHIVE="/tmp/mysqldump_$FILE.sql.gz"
CURRENT_DIR="./gladerru/current"

echo "Dumps $FILE"
mysqldump -u%(DATABASE_USER)s -p%(DATABASE_PASSWORD)s %(DATABASE_DB)s | gzip > $ARCHIVE

echo "make dir"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "mkdir -p ./gladerru/current"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "mkdir -p ./gladerru/intermediate"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "mkdir -p ./gladerru/old"

echo "upload $FILE"
scp $ARCHIVE %(DUMP_USER)s@%(DUMP_HOST)s:$CURRENT_DIR

echo "move old files"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "find ./gladerru/current -mtime +3 | grep _0000 | xargs -i mv {} ./gladerru/intermediate"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "find ./gladerru/current -mtime +3 -delete"

ssh %(DUMP_USER)s@%(DUMP_HOST)s "find ./gladerru/intermediate -mtime +10 | grep 01_0000 | xargs -i mv {} ./gladerru/old"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "find ./gladerru/intermediate -mtime +10 -delete"

