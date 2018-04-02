#!/usr/bin/env bash


[ "${KAMATERA_ENVIRONMENT_NAME}" == "" ] && echo missing KAMATERA_ENVIRONMENT_NAME && exit 1
! [ -e /kamatera-k8s ] && echo missing kamatera-k8s directory && exit 1
! [ -e /kamatera-k8s/switch_environment.sh ] && echo missing kamatera-k8s code && exit 1
! [ -e /kamatera-k8s/environments/$KAMATERA_ENVIRONMENT_NAME/.env ] && echo $KAMATERA_ENVIRONMENT_NAME environment is not initialized && exit 1


cd /kamatera-k8s
source switch_environment.sh $KAMATERA_ENVIRONMENT_NAME
export DPPCTL_CONF_PATH=/kamatera-k8s/environments/$KAMATERA_ENVIRONMENT_NAME/.dppctl
dppctl "$@"
