from flask import Flask, request, render_template_string
from script import RemoteCompiler  # Import your RemoteCompiler class from script.py

app = Flask(__name__)

# HTML template with form
form_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Compiler</title>
        <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
            font-size: 25px;
        }
    </style>

</head>
<body>
    <!-- Button to navigate to the info page -->
    <button onclick="window.location.href='/info';">How To Use</button>
    <!-- Button to navigate to the about page -->
    <button onclick="window.location.href='/about';">How This Works</button>
    <!-- Button to navigate to the command line page -->
    <button onclick="window.location.href='/command_line';">Instructions to use Command Line</button>

    <h1>Enter Details to Compile Project</h1>

    <form method="POST" action="/execute">
        <label for="hostname">Remote Server Hostname:</label>
        <input type="text" id="hostname" name="hostname" value="lnxsrv07.seas.ucla.edu"><br><br>

        <label for="username">SSH Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">SSH Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <label for="local_path">Local Project Directory:</label>
        <input type="text" id="local_path" name="local_path" required><br><br>

        <label for="remote_path">Remote Save Directory:</label>
        <input type="text" id="remote_path" name="remote_path" value="~/"><br><br>

        <label for="files">Enter .cpp file names (space-separated):</label>
        <input type="text" id="files" name="files" required><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

info_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How to Use</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
        }
        h1 {
            font-size: 25px;
            color: #333;
        }
    </style>
</head>
<body>
    <!-- Button to navigate back to home page -->
    <button onclick="window.location.href='/';">Go Back</button>

    <h3>How to use the remote compiler:</h3>
    <p>
        This tool lets you compile C++ code on a remote server without needing to manually log into the server and transfer files. Here’s how it works step-by-step:
    </p>
    <ul>
        <li><b>Step 1: Enter your SSH Credentials</b> - This is how you securely log into the remote server.</li>
            <ul>
                <li>You need to provide your username and password for the remote server (in this case, the `lnxsrv07` server). </li>
                <li>By default, your project will be compiled on the <strong>lnxsrv07</strong> server. If you prefer to use a different server, you can change this by specifying the desired server's hostname.</li>
                <li>If no changes are needed, leave the default option as is.</li>
            </ul>

        <li><b>Step 2: Specify Your Project</b> –  This helps the tool locate the files it needs to upload.</li>
            <ul>
                <li>You’ll be asked to provide the full path to the folder on your local computer where your C++ project is stored.</li>
                <li>For example, if your project directory is on your Desktop, run the <code>pwd</code> command in your terminal to get the full path. If you see something like <code>/Users/MyName/Desktop/my_project</code>, enter this path in the local path field.</li>
            </ul>

        <li><b>Step 3: Choose a Destination on the Remote Server</b> – You can choose where on the remote server the project should be uploaded. </li>
            <ul>
                <li>If you’re unsure, you can leave this blank, and the project will be uploaded to the default directory.</li>
            </ul>

        <li><b>Step 4: List the Files to Compile</b> – These are the actual code files you want to run on the server.</li>
             <ul>
                <li>You’ll enter the names of the <strong>C++ source files</strong> (`.cpp` files) that need to be compiled. </li>
                <li> Do not include any header files (`.h` files).</li>
                <li>For example, if your project contains <code>hello.cpp</code> and <code>bye.cpp</code>, enter: <code>hello.cpp bye.cpp</code>.</li>
            </ul>

        <li><b>Step 5: Compilation on the Remote Server</b> </li>
        <ul>
            <li>Once you hit "Submit," the tool transfers your files to the remote server and runs the necessary commands to compile the C++ project.</li>
        </ul> 

        <li><b>Step 6: View the Output</b> </li>
            <ul>
                <li>After the code runs on the remote server, you can see the results (or any errors) directly in your browser. No need to manually check the server.</li>
            </ul>
    </ul>

    <p> This tool helps you save time and effort by automating the file transfer and compilation process, making it easier for you to test your project.</p>
</body>
</body>

</html>
"""

about_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About The Compiler</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
        }
        h1 {
            font-size: 25px;
            color: #333;
        }
    </style>

</head>
    <body>
    <!-- Button to navigate back to home page -->
    <button onclick="window.location.href='/';">Go Back</button>

    <h3>How does this tool work behind the scenes?</h3>
    <p>
        This remote compiler tool is built using <b>Python</b>, <b>Flask</b> (for the web interface), and a library called <a href="https://docs.paramiko.org/en/stable/" target="_blank"><b>Paramiko</b></a> that handles SSH connections. Here’s what happens behind the scenes when you use this tool:
    </p>
    <ul>
        <li><b>Step 1: Connecting to the Remote Server</b> – The tool uses a Python library called <b>Paramiko</b> to establish an <b>SSH connection</b> with the remote server. SSH (Secure Shell) allows secure data transfer between your local machine and the server. Behind the scenes, Paramiko uses the SSH credentials you provided to log into the remote server without you having to manually do it yourself.</li>

        <li><b>Step 2: Transferring Files</b> – After logging in, the tool uses <b>SCP (Secure Copy Protocol)</b> to transfer your C++ project files from your local machine to the remote server. <b>SCP</b> ensures that your files are securely transferred over the network. The Python script, powered by Paramiko’s <b>SCPClient</b>, takes the files from the path you specified and uploads them to the remote server.</li>

        <li><b>Step 3: Compiling the Code</b> – Once your files are on the server, the tool runs a remote <b>compilation command</b> on your C++ files using the server's compiler (like <code>g++</code> or <code>g32</code>). This happens remotely on the server, meaning the server does the heavy lifting of compiling the code. The tool constructs the compilation command dynamically based on the file names you provided and executes it using Paramiko’s SSH connection.</li>

        <li><b>Step 4: Fetching Output</b> – After the code is compiled, the tool executes the compiled binary file on the server and captures the <b>output or error messages</b> that occur during execution. This is also done through Paramiko, which runs the command and retrieves the output via SSH. The Python code then sends this output back to the web interface.</li>

        <li><b>Step 5: Displaying Results</b> – The web app, built using <b>Flask</b>, shows you the results (success or error messages) directly in your browser. The result is dynamically inserted into the HTML page, giving you real-time feedback on the compilation and execution of your code on the remote server.</li>
    </ul>

    <p>TLDR: the tool automates the process of transferring files, compiling code, and fetching results from a remote server using <b>Paramiko</b> and <b>SCP</b>, making it much easier to work with remote servers for C++ projects.</p>
    <p>Want to see the code and learn more? Check out the project on <a href="https://github.com/shilpa-bo/CodeSyncAndCompile" target="_blank"><b>GitHub</b></a>.</p>

</body>

</body>
</html>

"""

command_line_instructions = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Command Line Instructions</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
            font-size: 25px;
        }
    </style>
</head>
<body>
    <!-- Button to navigate back to home page -->
    <button onclick="window.location.href='/';">Go Back</button>

    <h3>How to Perform Actions from the Command Line</h3>
    <ol>
        <li><b>Step 1: Transfer Files from Local to Remote</b><br>
            Use <b>scp</b> (Secure Copy Protocol) to transfer your files from your local machine to the remote server. Replace <code>local_path</code> with your local directory path, and <code>username</code> and <code>server_address</code> with your server login credentials.<br>
            <pre>
scp -r /path/to/local/directory username@server_address:/path/to/remote/directory
            </pre>
            Example:
            <pre>
scp -r /Users/MyName/Desktop/my_project username@lnxsrv07.seas.ucla.edu:Desktop
            </pre>
        </li>

        <li><b>Step 2: SSH into the Remote Server</b><br>
            Log into the remote server using the <b>ssh</b> command. Replace <code>username</code> and <code>server_address</code> with your credentials.<br>
            <pre>
ssh username@server_address
            </pre>
            Example:
            <pre>
ssh username@lnxsrv07.seas.ucla.edu
            </pre>
        </li>

        <li><b>Step 3: Navigate to Your Project Directory on the Remote Server</b><br>
            Once logged into the remote server, change directory to the location where you transferred your files.<br>
            <pre>
cd /path/to/remote/directory
            </pre>
            Example:
            <pre>
cd Desktop/my_project
            </pre>
        </li>

        <li><b>Step 4: Compile the C++ Code</b><br>
            Use <b>g32</b> to compile your project. Replace <code>source_files</code> with the names of your C++ files.<br>
            <pre>
g++ -o exec source_files.cpp
            </pre>
            Example:
            <pre>
g++ -o exec hello.cpp bye.cpp
            </pre>
        </li>

        <li><b>Step 5: Run the Compiled Program</b><br>
            After compiling the code, run the executable file generated.<br>
            <pre>
./exec
            </pre>
        </li>
    </ol>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(form_template)

@app.route('/execute', methods=['POST'])
def execute():
    # Get form data from the request
    hostname = request.form.get('hostname')
    username = request.form.get('username')
    password = request.form.get('password')
    local_path = request.form.get('local_path')
    remote_path = request.form.get('remote_path')
    files = request.form.get('files').split()  # Split the .cpp files by space

    # Create an instance of RemoteCompiler with the form data
    remote_compiler = RemoteCompiler(hostname, username, password, local_path, remote_path)

    # Transfer files to the remote server
    remote_compiler.transfer_files()

    # Construct the compile command and execute it
    compile_command = remote_compiler.construct_compile_command(files)
    commands = [compile_command, "./exec"]
    
    # Execute the commands on the remote server
    output = remote_compiler.execute_ssh_command(commands)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Command Output</title>
            <style>
                body {
                    font-family: 'Courier New', Courier, monospace;
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                pre {
                    background-color: #333;
                    color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>                      
            <!-- Button to navigate back to home page -->
            <button onclick="window.location.href='/';">Go Back</button>
            <h1>Executed Compile Command:</h1>
            <pre>{{ output }}</pre>
        </body>
        </html>
    ''', output=output)  # Pass the output variable to the template


@app.route('/info')
def info():
    return render_template_string(info_template)

@app.route('/about')
def about():
    return render_template_string(about_template)

@app.route('/command_line')
def commandLine():
    return render_template_string(command_line_instructions)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
