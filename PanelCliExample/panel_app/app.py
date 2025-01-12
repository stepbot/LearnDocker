import panel as pn
import paramiko
import os

pn.extension()

# Retrieve SSH parameters from environment variables
TARGET_HOST = os.environ.get("TARGET_HOST", "target")
TARGET_SSH_USER = os.environ.get("TARGET_SSH_USER", "testuser")
TARGET_SSH_PASS = os.environ.get("TARGET_SSH_PASS", "password")
TARGET_SSH_PORT = int(os.environ.get("TARGET_SSH_PORT", "22"))

# Setup Panel widgets
command_input = pn.widgets.TextInput(
    placeholder="Type bash command here...", 
    width=600
)
execute_button = pn.widgets.Button(name="Execute", button_type="primary")

# Using Markdown pane to display output with preserved formatting
output_pane = pn.pane.Markdown("", min_width=600, min_height=400, sizing_mode="stretch_both", styles={'overflow-y': 'auto'})

def run_command(event):
    cmd = command_input.value.strip()
    if not cmd:
        output_pane.object = "Please enter a command."
        return

    try:
        # Setup an SSH client and connect
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=TARGET_HOST, port=TARGET_SSH_PORT, username=TARGET_SSH_USER, password=TARGET_SSH_PASS)
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # Collect the output (both stdout and stderr)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        result = out + err
        ssh.close()
        
        # Wrap the output in markdown code fences to preserve formatting
        output_pane.object = f"```\n{result if result else 'Command executed with no output.'}\n```"
    except Exception as e:
        output_pane.object = f"Error executing command:\n```\n{e}\n```"

# Bind the button click event
execute_button.on_click(run_command)

# Layout the Panel app
app_layout = pn.Column(
    "# Remote Command Execution via SSH",
    command_input,
    execute_button,
    output_pane,
    sizing_mode="stretch_width"
)

app_layout.servable()

if __name__ == '__main__':
    pn.serve(app_layout, show=True, address='0.0.0.0', port=5006, allow_websocket_origin='*')
