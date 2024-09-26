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
    <button onclick="window.location.href='/info';">Go to Info Page</button>
    
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
<div>
    <h3>How to Use the Remote C++ Compiler</h3>
    <ul>
        <li><strong>Step 1: Enter Your SSH Username</strong>
            <ul>
                <li>Start by entering your <strong>lnxsrv07</strong> (or other server) <strong>username</strong>.</li>
            </ul>
        </li>

        <li><strong>Step 2: Enter Your SSH Password</strong>
            <ul>
                <li>Provide the <strong>password</strong> associated with your SSH username. This is required to authenticate and connect to the remote server.</li>
            </ul>
        </li>

        <li><strong>Step 3: Enter Local Project Path</strong>
            <ul>
                <li>You must specify the full path to your project directory on your local machine.</li>
                <li>For example, if your project directory is on your Desktop, run the <code>pwd</code> command in your terminal to get the full path. If you see something like <code>/Users/MyName/Desktop/my_project</code>, enter this path in the local path field.</li>
            </ul>
        </li>

        <li><strong>Step 4: Enter Remote Directory Path</strong>
            <ul>
                <li>Enter the path on the remote server where you want to transfer your project. If you're unsure or don’t have a preference, press Enter to use the default directory (typically the home directory).</li>
            </ul>
        </li>

        <li><strong>Step 5: Specify the C++ Files to Compile</strong>
            <ul>
                <li>Enter the names of the <strong>C++ source files</strong> you want to compile. These are your <code>.cpp</code> files. Do not include any header files (<code>.h</code>).</li>
                <li>For example, if your project contains <code>hello.cpp</code> and <code>bye.cpp</code>, enter: <code>hello.cpp bye.cpp</code>.</li>
            </ul>
        </li>

        <li><strong>Step 6: Select Remote Server (Optional)</strong>
            <ul>
                <li>By default, your project will be compiled on the <strong>lnxsrv07</strong> server. If you prefer to use a different server, you can change this by specifying the desired server's hostname.</li>
                <li>If no changes are needed, leave the default option as is.</li>
            </ul>
        </li>

        <li><strong>Step 7: Submit the Form</strong>
            <ul>
                <li>After filling out all the required fields, press the <strong>Submit</strong> button.</li>
                <li>Once submitted, your files will be transferred to the remote server, compiled, and the output or errors will be displayed on the screen.</li>
            </ul>
        </li>
    </ul>
</div>

<div>
<h3> How this works </h3>
</div>
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
                    font-family: Arial, sans-serif;
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
