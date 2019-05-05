## Ambari Service for Kylin

## Version
   + Kylin 2.6.1 (With Hadoop 3.x version)
   + Ambari 2.7+
   + HDP 3.1.0

## Setup

#### Prepare spark package 
Configure ***spark-2.3.2-bin-hadoop2.7.tgz*** download url. Kylin must used special spark package to RUNNING successful.

#### Deploy Kylin on existing cluster

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

## Configure

#### Create HBase Namespace
Namespace MUST BE UPPER CASE!!!
```
hbase shell
> create_namespace 'NS_KYLIN'
``` 

#### Kerberos TGT Init
```
[root@cdh-node-2 security]# cat init_kt.sh
#!/bin/bash
kinit -kt ./kylin.keytab kylin@HWINFO.COM
```
Use crontab every 1:00 AM init TGT
```
0 1 * * * kylin /home/kylin/init_kt.sh  > /tmp/kylin-ktinit.log 2>&1
```

#### Apache Ranger configure
Generate all privileges on HDFS to kylin.    
Generate all privileges on Hive to kylin.  
Generate all privileges on HBase to kylin.  

## !!!IMPORTANT!!!
Every YARN node must had kylin user.
```
sudo groupadd kylin && sudo useradd kylin -g kylin && sudo gpasswd -a kylin hadoop
```