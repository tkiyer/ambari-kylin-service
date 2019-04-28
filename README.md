## Ambari Service for Kylin

## Version
   + Kylin 2.6.1 (With Hadoop 3.x version)
   + Ambari 2.7+
   + HDP 3.1.0

## Setup

#### Deploy Hue on existing cluster

- To download the kylin service folder, run below
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo rm -rf /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/KYLIN  
sudo git clone https://github.com/tkiyer/ambari-kylin-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/KYLIN
```

- Restart Ambari

```
sudo ambari-server restart
```
