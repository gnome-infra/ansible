#!/usr/bin/python3

import subprocess
import sys
import json
import requests

# Quick and dirty way to set the SSH key for the lorry user

def get_ansible_var(server, varname):
    result = subprocess.run(["ansible", server, "-m", "debug", "-a", f"var={varname}"], capture_output=True, text=True)
    assert result.returncode == 0
    # strip every character from stdout up to "{"
    expr = result.stdout[result.stdout.find("{"):]
    data = json.loads(expr)
    return data[varname]

def key_with_title(key_data, title):
    for key in key_data:
        if key["title"] == title:
            return key
    return None

def get_keys(gitlab_domain, gitlab_token):
    response = requests.get(f"https://{gitlab_domain}/api/v4/user/keys", params={"private_token": api_token})
    response.raise_for_status()
    return response.json()

def delete_key(gitlab_domain, gitlab_token, key_id):
    response = requests.delete(f"https://{gitlab_domain}/api/v4/user/keys/{key_id}", params={"private_token": gitlab_token})
    response.raise_for_status()

def add_key(gitlab_domain, gitlab_token, ssh_key_name, ssh_key):
    response = requests.post(f"https://{gitlab_domain}/api/v4/user/keys", params={"private_token": gitlab_token, "title":ssh_key_name, "key":ssh_key})

def keys_equal(a, b):
    # strip the label at the end of the key, as that gets rewritten on upload
    a = a[:a.find("=")]
    b = b[:b.find("=")]
    return a == b


lorry_server = sys.argv[1]
api_token_label = "lorry.gitlab_token"
gitlab_domain_label = "gnome_gitlab_domain"
ssh_key_label = "lorry.ssh_pub_key"
ssh_key_name_label = "lorry.gitlab_ssh_key_name"

api_token = get_ansible_var(lorry_server, api_token_label)
gitlab_domain = get_ansible_var(lorry_server, gitlab_domain_label)
ssh_key = get_ansible_var(lorry_server, ssh_key_label)
ssh_key_name = get_ansible_var(lorry_server, ssh_key_name_label)


keys_data = get_keys(gitlab_domain, api_token)
found_key = key_with_title(keys_data, ssh_key_name)
if found_key:
    if not keys_equal(found_key["key"], ssh_key):
        # Old public key installed, delete it
        print("Replacing old key")
        delete_key(gitlab_domain, api_token, found_key["id"])
        add_key(gitlab_domain, api_token, ssh_key_name, ssh_key)
    else:
        print("Key is already installed")
else:
    print("Adding new key")
    add_key(gitlab_domain, api_token, ssh_key_name, ssh_key)
