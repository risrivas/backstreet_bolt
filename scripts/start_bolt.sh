#!/bin/bash

export PROJECT_HOME="$( cd "$(dirname "$0")" ; cd .. ; pwd -P )"
source ${PROJECT_HOME}/scripts/config.sh

if [[ ! -d "${LOG_DIR}" ]]; then
  mkdir -p ${LOG_DIR}
fi

${PROJECT_HOME}/scripts/stop_bolt.sh

/usr/local/bin/docker container run -d --rm --name ${SERVICE_BOLT} -p 8802:8888 -v ${PROJECT_HOME}/backstreet/use_backtest_bolt:/home/backstreet/use_backtest_bolt ${IMAGE_BOLT}:${VERSION}

container_ids=`/usr/local/bin/docker ps -aqf "name=${SERVICE_BOLT}.*"`
for cid in ${container_ids}
do
 /usr/local/bin/docker logs -f ${cid} > ${PROJECT_HOME}/logs/${SERVICE_BOLT}_${cid}.log 2>&1 &
done

