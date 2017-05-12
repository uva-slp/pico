#!/bin/bash
if [ -d "/init-db/" ]; then
    sleep 5
    cat /init-db/000-db-init.sql | mysql
    cat /init-db/schema.sql | mysql pico
    /bin/rm /init-db/*
    rmdir /init-db
fi
