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
</head>
<body>
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

    # Return the output as a response (for simplicity, you can extend this to handle output better)
    return f"<h1>Executed Compile Command:</h1><pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
