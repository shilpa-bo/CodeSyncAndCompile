import paramiko
import os
from scp import SCPClient, SCPException


class RemoteCompiler:

    def __init__(self, host, username, password, local_path, remote_path, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.local_path = local_path
        self.remote_path = remote_path
        self.port = port

    def create_ssh_client(self):
        """
        Creates an SSH client and establishes a connection to the remote server.

        Args:
            host (str): The hostname or IP address of the remote server.
            username (str): SSH username for authentication.
            password (str): SSH password for authentication.
            port (int, optional): SSH port to connect to. Default is 22.

        Returns:
            SSHClient: A connected SSH client.
        """
        client = paramiko.SSHClient()

        # Automatically add the server's host key if it's new
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Logging into {self.username}@{self.host}")
        client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)

        return client


    def transfer_files(self):
        """
        Transfers a directory or file from the local machine to the remote server.

        Args:
            local_path (str): The local file or directory path to transfer.
            remote_path (str): The destination directory on the remote server.
            host (str): The hostname or IP address of the remote server.
            username (str): SSH username for authentication.
            password (str): SSH password for authentication.
            port (int, optional): SSH port to connect to. Default is 22.
        """
        ssh = None
        try:
            ssh = self.create_ssh_client()
            self.local_path = os.path.expanduser(self.local_path)  # Expand user home directory (~) in local path

            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(self.local_path, self.remote_path, recursive=True)
                    print(f"Successfully transferred {self.local_path} to {self.host}:{self.remote_path}")
                
            except SCPException as scp_error:
                print(f"SCP error: {scp_error}")
            
            finally:
                if ssh:
                    ssh.close()
        
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
        except paramiko.SSHException as ssh_error:
            print(f"SSH error: {ssh_error}")
        except FileNotFoundError:
            print(f"File not found: {self.local_path}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def execute_ssh_command(self, cmd):
        """
        Executes a list of commands on the remote server.

        Args:
            host (str): The hostname or IP address of the remote server.
            username (str): SSH username for authentication.
            password (str): SSH password for authentication.
            cmd (list): A list of commands to execute on the remote server.
            port (int, optional): SSH port to connect to. Default is 22.
        """
        all_output = ""
        client = None
        try:
            client = self.create_ssh_client()
            for command in cmd:
                print(f"Running command: {command}")
                stdin, stdout, stderr = client.exec_command(command)

                # Get command's output and error
                output = stdout.read().decode()
                error = stderr.read().decode()

                if output:
                    all_output += (f"Output:\n{output}\n")
                if error:
                    all_output += (f"Error:\n{error}\n")
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
        except paramiko.SSHException as ssh_error:
            print(f"SSH error: {ssh_error}")
        except Exception as e:
            print(f"Operation failed: {e}")
        finally:
            if client:
                client.close()
        return all_output


    def construct_compile_command(self, file_names):
        """
        Constructs the compile command to compile .cpp files on the remote server.

        Args:
            local_path (str): File path of the project on the local machine.
            file_names (list): List of .cpp file names that need to be compiled.
            remote_path (str): Remote path where the project was transferred.

        Returns:
            str: The full command to compile the .cpp files.
        """
        def get_last_directory(path):
            return os.path.basename(os.path.normpath(path))
        
        project_directory = get_last_directory(self.local_path)
        compile_command = "/usr/local/cs/bin/g32 -o exec"
        
        for file in file_names:
            file_path = os.path.join(self.remote_path, project_directory, file)
            compile_command += f" {file_path}"
        
        return compile_command

