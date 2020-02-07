import os
from Common import Config
import paramiko


class SshClient:

    def connect(self):
        global client
        client = paramiko.SSHClient()
        hostname = Config.Config.ssh_hostname
        port = Config.Config.ss_port
        username = Config.Config.ssh_client
        password = Config.Config.ssh_password

        try:
            print("Establishing SSH connection")
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username=username, password=password)
            print("Connected via SSH")
            return client
        except Exception as e:
            print("SSH CONNECTION FAILED!")
            print(e)

    def execute_command(self, client, command):
        print("Running command: " + command)
        stdin, stdout, stderr = client.exec_command(command)
        print('Command output:')
        resultLines = stdout.readlines()
        for line in resultLines:
            print(' + ' + line)

        return resultLines

    def execute_adapter_reset(self, client):
        self.execute_command(client, 'cd ' + Config.Config.webroot_path + '; bin/magento indaba:import:adapter:reset')

    def transfer_file(self, client, local_path, remote_path):
        sftp = client.open_sftp()
        try:
            sftp.put(local_path, remote_path)
        except Exception as e:
            print("FILE TRANSFER FAILED!")
            print(e)
        sftp.close()

    def check_is_file_tansferred(self, client, remote_path, file_name):
        lsResult = self.execute_command(client, 'ls ' + remote_path)
        for line in lsResult:
            if file_name in line:
                return True

        return False
