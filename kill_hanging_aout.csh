kill -9 `ps -e | grep a.out | grep -v grep | awk '{print $1}'`
