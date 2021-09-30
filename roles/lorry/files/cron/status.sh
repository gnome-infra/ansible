set -x
while true; do
    curl -o /dev/null http://lorry-controller-webapp:12765/1.0/status
    sleep 10
done
