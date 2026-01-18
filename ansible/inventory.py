#!/usr/bin/env python3

import subprocess
import json
import sys

def terraform_output():
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd="../terraform",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        sys.exit(1)

outputs = terraform_output()

public_ip = outputs["public_ip"]["value"]

inventory = {
    "all": {
        "hosts": [public_ip],
        "vars": {
            "ansible_user": "ubuntu",
            "ansible_ssh_private_key_file": "~/.ssh/Ansible_key.pem",
            "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
        }
    }
}


print(json.dumps(inventory, indent=2))
