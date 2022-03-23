#!/bin/bash
# basic: no username or password posted, no cookies (login)
curl http://localhost:"$1"
# correct username and password posted, no cookies (success)
curl -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:"$1"
# non-existent username posted with password, no cookies (bad credentials)
curl -d "username=some&password=none" http://localhost:"$1"
# existing username posted with bad password, no cookies (bad credentials)
curl -d "username=bezos&password=none" http://localhost:"$1"
# exactly one of username or password posted, other field missing, no cookies (bad credentials)
curl -d "username=bezos" http://localhost:"$1"
# no username or password posted, valid cookie (success)
curl -c cookies.txt -b cookies.txt http://localhost:"$1"
# non-existent username or bad password for existing username, valid cookie (success)
curl -d "username=some&password=none" -c cookies.txt -b cookies.txt http://localhost:"$1"
# correct username and password, valid cookie (success)
curl -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:"$1"
# correct username and password, invalid cookie (bad credentials)
sed -i 's/0/1/g' cookies.txt
curl -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:"$1"
# logout posted, valid cookie (logout)
curl -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:"$1" > /dev/null # regenerate cookie
curl -d "action=logout" -c cookies.txt -b cookies.txt http://localhost:"$1"
# logout posted, invalid cookie (logout)
curl -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:"$1" > /dev/null # regenerate cookie
sed -i 's/0/1/g' cookies.txt
curl -d "action=logout" -c cookies.txt -b cookies.txt http://localhost:"$1"