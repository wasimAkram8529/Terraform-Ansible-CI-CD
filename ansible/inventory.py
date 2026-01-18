#!/usr/bin/env python3

import subprocess
import json
import sys
import os

TERRAFORM_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "terraform")
)

def terraform_output():
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd=TERRAFORM_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        print("terraform output failed", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError:
        print("terraform binary not found", file=sys.stderr)
        sys.exit(1)

outputs = terraform_output()

if "public_ip" not in outputs:
    print("public_ip output not found in terraform state", file=sys.stderr)
    sys.exit(1)

public_ip = outputs["public_ip"]["value"]

inventory = {
    "all": {
        "hosts": [public_ip],
        "vars": {
            "ansible_user": os.getenv("ANSIBLE_USER", "ubuntu"),
            "ansible_ssh_private_key_file": os.getenv(
                "ANSIBLE_PRIVATE_KEY_FILE", "~/.ssh/id_rsa"
            ),
            "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
        }
    }
}

print(json.dumps(inventory))
