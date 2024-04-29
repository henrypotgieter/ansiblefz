import os
import sys
import argparse
from . import sqlinterface
from . import fzf

# Instantiate fzf
fzf = fzf.Fzf()

# Instantiate sql
sql_conn = sqlinterface.Sqlconn()


class Ansiblefz(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Ansiblefz script")
        self.parser.add_argument("-c", "--category", help="Specify the category")
        self.parser.add_argument("-s", "--scriptname", help="Specify the scriptname")
        self.args = self.parser.parse_args()
        self.run()

    def run(self):
        # Set command prefix to use
        cmd_prefix = "ansible-playbook "
        # Define empty command args var to append to as needed
        cmd_args = ""

        if self.args.category and self.args.scriptname:
            script_description = sql_conn.script_desc(self.args.category, self.args.scriptname)
            print(script_description)
            sys.exit(0)
        elif self.args.category:
            category_description = sql_conn.category_desc(self.args.category)
            print(category_description)
            sys.exit(0)

        # Get the playbooks we want to use from SQL
        platform = sql_conn.categories()

        # Handle platform and populate playbooks/command suffix var
        platform_select = fzf.fzfu(platform, "Choose platform", "Ansiblefz - Playbook Selection Script")
        playbooks = sql_conn.playbooks(platform_select[0])
        cmd_suffix = sql_conn.directory(platform_select[0])

        playbook_select = fzf.fzfc(
            playbooks, "Playbook Selection", "CMD: " + cmd_prefix + cmd_suffix, platform_select[0]
        )

        playbooks_return = sql_conn.filedata(playbook_select[0])
        cmd_suffix += "/" + playbooks_return[0]

        # Assemble and return the command back to the calling shell script
        command = cmd_prefix + cmd_args + cmd_suffix
        print(command)

if __name__ == "__main__":
    Ansiblefz()
