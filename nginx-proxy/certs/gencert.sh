#!/bin/sh
NAME=default
openssl genrsa -out $NAME.key 4096
openssl req -new -key $NAME.key -out $NAME.csr -subj "/OU=IAI/CN=localhost/O=Universitaet Bremen/C=DE" -config openssl.cnf
openssl x509 -req -days 365 -in $NAME.csr -signkey $NAME.key -out $NAME.crt -extensions v3_req -extfile openssl.cnf
rm $NAME.csr
