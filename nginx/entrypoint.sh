#!/bin/sh

# Set backups based on ACTIVE_POOL
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

# Substitute all variables in template and create final config
envsubst '${ACTIVE_POOL} ${RELEASE_ID} ${BLUE_BACKUP} ${GREEN_BACKUP}' \
    < /etc/nginx/templates/default.conf.template \
    > /etc/nginx/conf.d/default.conf

chmod 644 /etc/nginx/conf.d/default.conf

echo "Nginx configuration generated with ACTIVE_POOL=${ACTIVE_POOL}, RELEASE_ID=${RELEASE_ID}"

# Start nginx in foreground
nginx -g 'daemon off;'

