# AnsibleFZF

A tool to provide speedy execution of Ansible playbooks from CLI that you may need to
run semi-frequently.

Playbook locations are divided into categories, each represented by a string name which
reference a specific directory on the host you're running on.

Scripts are assigned to each category with a filename, an optional required user, an
indicator if the script requires sudo/become privileges and a scriptname which will be
visible in the fzf output for selection.

Source the `structure.sql` file to create the required tables within your MySQL instance.

## Getting Started

Make sure to install your requirements as necessary:

```
pip3 install -r requirements.txt
```

You will need to install the `expect-dev` package to have access to the `unbuffer` tool
in order to preserve coloured text being written to your log files.

Copy the example env file and modify with your editor of choice, eg:

```
cp .env-example .env
vi .env

```

Make sure you populate each variable correctly.  The script only needs read-only DB access.

## Execution

You should now be able to run the script from anywhere.  You can place a symlink for it
within a directory that is part of your $PATH to be able to call it readily, or add an
alias to do so.
