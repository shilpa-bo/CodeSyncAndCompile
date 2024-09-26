import paramiko
import os
from scp import SCPClient, SCPException

def create_ssh_client(host, username, password, port=22):
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

    print(f"Logging into {username}@{host}")
    client.connect(hostname=host, port=port, username=username, password=password)

    return client


def transfer_files(local_path, remote_path, host, username, password, port=22):
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
    try:
        ssh = create_ssh_client(host, username, password)
        local_path = os.path.expanduser(local_path)  # Expand user home directory (~) in local path

        try:
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(local_path, remote_path, recursive=True)
                print(f"Successfully transferred {local_path} to {host}:{remote_path}")
            
        except SCPException as scp_error:
            print(f"SCP error: {scp_error}")
        
        finally:
            ssh.close()
    
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as ssh_error:
        print(f"SSH error: {ssh_error}")
    except FileNotFoundError:
        print(f"File not found: {local_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def execute_ssh_command(host, username, password, cmd, port=22):
    """
    Executes a list of commands on the remote server.

    Args:
        host (str): The hostname or IP address of the remote server.
        username (str): SSH username for authentication.
        password (str): SSH password for authentication.
        cmd (list): A list of commands to execute on the remote server.
        port (int, optional): SSH port to connect to. Default is 22.
    """
    try:
        client = create_ssh_client(host, username, password)
        for command in cmd:
            print(f"Running command: {command}")
            stdin, stdout, stderr = client.exec_command(command)

            # Get command's output and error
            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print(f"Output:\n{output}")
            if error:
                print(f"Error:\n{error}")
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as ssh_error:
        print(f"SSH error: {ssh_error}")
    except Exception as e:
        print(f"Operation failed: {e}")
    finally:
        client.close()


def create_list_of_files():
    """
    Prompts the user to input .cpp file names and returns them as a list.

    Returns:
        list: A list of .cpp file names inputted by the user.
    """
    files = input("Enter .cpp file names that need to be compiled, separated by a space: ")
    file_list = files.split()  # Split the input by spaces to create a list
    return file_list


def construct_compile_command(local_path, file_names, remote_path):
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
    
    project_directory = get_last_directory(local_path)
    compile_command = "/usr/local/cs/bin/g32 -o exec"
    
    for file in file_names:
        file_path = os.path.join(remote_path, project_directory, file)
        compile_command += f" {file_path}"
    
    return compile_command


# User input and execution
username = input("Enter your SSH username: ")
password = input("Enter your SSH password: ")
hostname = input("Enter the remote server hostname (press Enter to use lnxsrv07.seas.ucla.edu as default): ")
if not hostname:
    hostname = "lnxsrv07.seas.ucla.edu"

local_path = input("Enter the local project directory's full file path: ")
remote_path = input("Enter the remote directory where you'd like to save the file (press Enter to use default directory ~): ")
if not remote_path:
    remote_path = "~/"

# Get .cpp file names
file_list = create_list_of_files()

# Transfer files to remote server
transfer_files(local_path, remote_path, hostname, username, password)

# Construct and execute the compile command on the remote server
compile_command = construct_compile_command(local_path, file_list, remote_path)
commands = [compile_command, "./exec"]
print(f"Compiled command: {compile_command}")

# Execute the commands on the remote server
execute_ssh_command(hostname, username, password, commands)

#/Users/Shilpa2/Documents/prac_cpp