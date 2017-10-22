#!/bin/bash
# Initially request the SSL cert from Let's Encrypt (executed by the ansible
# script `ghu.yml')
exec certbot certonly --expand --agree-tos --email contact@globalhumanitariansunite.org \
             --non-interactive --webroot -w /var/www/certbot-overlay \
             -d globalhumanitariansunite.org \
             -d www.globalhumanitariansunite.org \
             -d globalhumanitariansunite.info \
             -d www.globalhumanitariansunite.info \
             -d globalhumanitariansunite.net \
             -d www.globalhumanitariansunite.net \
             -d globalhumanitariansunite.com \
             -d www.globalhumanitariansunite.com \
             -d jenkins.globalhumanitariansunite.org \
             -d master.globalhumanitariansunite.org \
             -d develop.globalhumanitariansunite.org \
             -d mail.globalhumanitariansunite.org \
             -d email.globalhumanitariansunite.org
