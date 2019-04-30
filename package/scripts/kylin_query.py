import pwd
import grp
from resource_management import *


class KylinQuery(Script):
    def install(self, env):
        import params
        env.set_params(params)
        # create kylin directories
        Directory([params.kylin_log_dir, params.kylin_pid_dir],
                  mode=0755,
                  cd_access='a',
                  create_parents=True
                  )
        # download apache-kylin-2.6.1-bin-hadoop3.tar.gz
        Execute('{0} | xargs wget -O /tmp/kylin.tar.gz'.format(params.kylin_download))
        # Install kylin
        Execute('tar -zxvf /tmp/kylin.tar.gz -C /usr/local')
        # Remove kylin installation file
        Execute('rm -rf /tmp/kylin.tar.gz')
        # Rename kylin installation dir
        Execute('mv /usr/local/{0} {1}'.format(params.kylin_project_name, params.kylin_install_dir))
        # Create Hadoop conf dir
        Execute('mkdir -p {0}/hadoop-conf'.format(params.kylin_install_dir))
        # Create kylin user and group
        try:
            Execute('groupadd kylin && useradd kylin -g kylin')
        except:
            print " "
        # Ensure all files owned by kylin user:group
        cmd = format("chown -R kylin:kylin {kylin_install_dir}")
        Execute(cmd)
        # Link hadoop conf
        Execute('ln -s /usr/hdp/current/hadoop-client/conf/core-site.xml {0}/hadoop-conf/core-site.xml'.format(params.kylin_install_dir))
        Execute('ln -s /usr/hdp/current/hadoop-client/conf/hdfs-site.xml {0}/hadoop-conf/hdfs-site.xml'.format(params.kylin_install_dir))
        Execute('ln -s /usr/hdp/current/hadoop-client/conf/yarn-site.xml {0}/hadoop-conf/yarn-site.xml'.format(params.kylin_install_dir))
        Execute('ln -s /usr/hdp/current/hadoop-client/conf/mapred-site.xml {0}/hadoop-conf/mapred-site.xml'.format(params.kylin_install_dir))
        Execute('ln -s /usr/hdp/current/hbase-client/conf/hbase-site.xml {0}/hadoop-conf/hbase-site.xml'.format(params.kylin_install_dir))
        Execute('ln -s /usr/hdp/current/hive-client/conf/hive-site.xml {0}/hadoop-conf/hive-site.xml'.format(params.kylin_install_dir))

        # Create HDFS dir for kylin
        Execute('hadoop fs -mkdir -p /kylin', user='hdfs')
        Execute('hadoop fs -chown kylin:kylin /kylin', user='hdfs')
        
        # Initialize environment variables
        File(format("{tmp_dir}/kylin_env.rc"),
             content=Template("env.rc.j2"),
             owner='kylin',
             group='kylin',
             mode=0o700
             )

    def configure(self, env):
        import params
        env.set_params(params)
        kylin_properties = InlineTemplate(params.kylin_properties)
        File(format("{kylin_install_dir}/conf/kylin.properties"),
             owner='kylin',
             group='kylin',
             content=kylin_properties)
        Execute(format("chown -R kylin:kylin {kylin_log_dir} {kylin_pid_dir}"))
        cmd = format(". {tmp_dir}/kylin_env.rc;{kylin_install_dir}/bin/check-env.sh")
        Execute(cmd, user="kylin")
        Execute("hadoop fs -mkdir -p /kylin/kylin_metadata", user="kylin")
        Execute("hadoop fs -chmod -R 777 /kylin/kylin_metadata", user="kylin")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        cmd = format(
            ". {tmp_dir}/kylin_env.rc;{kylin_install_dir}/bin/kylin.sh start;cp -rf {kylin_install_dir}/pid {kylin_pid_file}")
        Execute(cmd, user='kylin')

    def stop(self, env):
        import params
        env.set_params(params)
        cmd = format("{kylin_install_dir}/bin/kylin.sh stop")
        Execute(cmd, user='kylin')
        File(params.kylin_pid_file,
             action="delete",
             owner='kylin'
             )

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status('/var/run/kylin/kylin.pid')


if __name__ == "__main__":
    KylinQuery().execute()
