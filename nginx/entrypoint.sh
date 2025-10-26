#!/bin/sh

if [ "$ACTIVE_POOL" = "blue" ]; then
    export BLUE_BACKUP=""
    export GREEN_BACKUP="backup"
elif [ "$ACTIVE_POOL" = "green" ]; then
    export BLUE_BACKUP="backup"
    export GREEN_BACKUP=""
else
    echo "ERROR: ACTIVE_POOL must be 'blue' or 'green', got: $ACTIVE_POOL"
    exit 1
fi

envsubst '${BLUE_BACKUP} ${GREEN_BACKUP}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

chmod 644 /etc/nginx/conf.d/default.conf

echo "Nginx configuration generated with ACTIVE_POOL=${ACTIVE_POOL}"
