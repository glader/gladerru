#!/bin/sh

DIR="`date +%%Y_%%m`"
FILE="`date +%%Y%%m%%d_%%H%%M`"
FULL_DIR="/backup/%(DUMP_USER)s/gladerru/$DIR"
ARCHIVE="/tmp/mysqldump_$FILE.sql.gz"

echo "Dumps $FILE"
mysqldump -u%(DATABASE_USER)s -p%(DATABASE_PASSWORD)s %(DATABASE_DB)s | gzip > $ARCHIVE

echo "make dir $DIR"
ssh %(DUMP_USER)s@%(DUMP_HOST)s "mkdir -p $FULL_DIR"

echo "upload $FILE"
scp $ARCHIVE %(DUMP_USER)s@%(DUMP_HOST)s:$FULL_DIR
