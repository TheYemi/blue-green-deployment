#!/bin/sh
envsubst '$ACTIVE_POOL $RELEASE_ID $BLUE_BACKUP $GREEN_BACKUP' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf
nginx -s reload

