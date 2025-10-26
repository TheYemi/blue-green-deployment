#!/bin/sh

envsubst '${BLUE_BACKUP} ${GREEN_BACKUP}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

nginx -s reload

echo "Nginx reloaded with new configuration"
