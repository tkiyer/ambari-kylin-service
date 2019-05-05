from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
import os

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
tmp_dir = Script.get_tmp_dir()

ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']
kylin_project_name = 'apache-kylin-2.6.1-bin-hadoop3'
kylin_download = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/kylin/apache-kylin-2.6.1-bin-hadoop3.tar.gz"}\''

kylin_install_dir = config['configurations']['kylin']['kylin_install_dir']
kylin_log_dir = config['configurations']['kylin']['kylin_log_dir']
kylin_pid_dir = config['configurations']['kylin']['kylin_pid_dir']
kylin_pid_file = format("{kylin_pid_dir}/kylin.pid")

kylin_web_port = config['configurations']['kylin']['kylin_web_port']

kylin_env_hdfs_working_dir = config['configurations']['kylin']['kylin_env_hdfs_working_dir']

kylin_engine_spark_conf_spark_eventLog_dir = config['configurations']['kylin']['kylin_engine_spark_conf_spark_eventLog_dir']

kylin_engine_spark_conf_spark_history_fs_logDirectory = config['configurations']['kylin']['kylin_engine_spark_conf_spark_history_fs_logDirectory']

kylin_properties = config['configurations']['kylin']['kylin_properties']

kylin_env_header = config['configurations']['kylin-env']['kylin_env_header']

kylin_check_env_sh = config['configurations']['kylin-check-env-shell']['kylin_check_env_sh']

kylin_tomcat_conf = config['configurations']['kylin-tomcat']['kylin_tomcat_conf']

kylin_tomcat_context_conf = config['configurations']['kylin-tomcat-context']['kylin_tomcat_context_conf']

kylin_spark_download_sh = config['configurations']['kylin-spark-download']['kylin_spark_download_sh']

# kylin web timezone
kylin_web_timezone = config['configurations']['kylin']['kylin_web_timezone']
# kylin_web_cross_domain_enabled
kylin_web_cross_domain_enabled = config['configurations']['kylin']['kylin_web_cross_domain_enabled']
if (kylin_web_cross_domain_enabled):
    kylin_web_cross_domain_enabled = 'true'
else:
    kylin_web_cross_domain_enabled = 'false'

current_host_name = config['agentLevelParams']['hostname']
server_mode = "query"
server_masters = config['clusterHostInfo']['kylin_master_hosts'][0]
server_clusters_arr = config['clusterHostInfo']['kylin_master_hosts'] + (
    config['clusterHostInfo'].has_key('kylin_query_hosts') and config['clusterHostInfo']['kylin_query_hosts'] or [])

server_clusters = ','.join(i + ":" + kylin_web_port for i in server_clusters_arr)
kylin_servers = ';'.join("server " + i + ":" + kylin_web_port for i in server_clusters_arr) + ";"

# hive
hive_server_host = default("/clusterHostInfo/hive_server_hosts", ['localhost'])[0]
hive_server_port = default('/configurations/hive-site/hive.server2.thrift.port', "10000")

# java home
java_home = config['ambariLevelParams']['java_home']