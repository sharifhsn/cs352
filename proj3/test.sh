#!/bin/bash
# basic: no username or password posted, no cookies (login)
curl -v http://localhost:32702
# correct username and password posted, no cookies (success)
curl -v -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:32702
# non-existent username posted with password, no cookies (bad credentials)
curl -v -d "username=some&password=none" http://localhost:32702
# existing username posted with bad password, no cookies (bad credentials)
curl -v -d "username=bezos&password=none" http://localhost:32702
# exactly one of username or password posted, other field missing, no cookies (bad credentials)
curl -v -d "username=bezos" http://localhost:32702
# no username or password posted, valid cookie (success)
curl -v -c cookies.txt -b cookies.txt http://localhost:32702
# non-existent username or bad password for existing username, valid cookie (success)
curl -v -d "username=some&password=none" -c cookies.txt -b cookies.txt http://localhost:32702
# correct username and password, valid cookie (success)
curl -v -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:32702
# correct username and password, invalid cookie (bad credentials)
sed 's/0/1' cookies.txt
curl -v -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:32702
# logout posted, valid cookie (logout)
curl -v -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:32702 > /dev/null
curl -v -d "action=logout" -c cookies.txt -b cookies.txt http://localhost:32702
# logout posted, invalid cookie (logout)
curl -v -d "username=bezos&password=amazon" -c cookies.txt -b cookies.txt http://localhost:32702 > /dev/null
sed 's/0/1' cookies.txt
curl -v -d "action=logout" -c cookies.txt -b cookies.txt http://localhost:32702