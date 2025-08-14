#!/bin/sh

host="$1"
shift

if [ "$1" = "--" ]; then
  shift
fi

cmd="$@"
max_attempts=30
attempt=1

until curl -s --connect-timeout 1 "http://$host" > /dev/null; do
  echo "Waiting fro $host..."
  sleep 1
  if [ $attempt -eq $max_attempts ]; then
    echo "Timeout waiting for $host"
    exit 1
  fi
  attempt=$((attempt +1))
done

echo "$host is available, resolving consul IP"
CONSUL_IP=$(dig +short + consul)
if [ -z "$CONSUL_IP" ]; then
  echo "Failed to resolve consul ip"
  exit 1
fi
sed -i "s/address: consul/address: $CONSUL_IP/g" /etc/envoy/envoy.yaml
echo "envoy.yaml updated"
exec $cmd
