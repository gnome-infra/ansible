sleep 10
set -x
while true; do
    curl -o /dev/null -X POST --data "" http://lorry-controller-webapp:12765/1.0/read-configuration
    sleep 120
done
