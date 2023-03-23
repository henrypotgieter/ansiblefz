import os
from . import sqlinterface
from . import fzf

# Instantiate fzf
fzf = fzf.Fzf()

# Instantiate sql
sql_conn = sqlinterface.Sqlconn()


class Ansiblefz(object):
    def __init__(self):
        self.run()

    def run(self):
        # Set command prefix to use
        cmd_prefix = "ansible-playbook "
        # Define empty command args var to append to as needed
        cmd_args = ""

        # Get the playbooks we want to use from SQL
        platform = sql_conn.categories()

        # Handle platform and populate playbooks/command suffix var
        platform_select = fzf.fzfu(platform, "Choose platform", "Ansiblefz - Playbook Selection Script")
        playbooks = sql_conn.playbooks(platform_select[0])
        cmd_suffix = sql_conn.directory(platform_select[0])

        playbook_select = fzf.fzfc(
            playbooks, "Playbook Selection", "CMD: " + cmd_prefix + cmd_suffix
        )

        playbooks_return = sql_conn.filedata(playbook_select[0])
        cmd_suffix += "/" + playbooks_return[0]

        # Get the username we are running the script as
        my_user = os.getlogin()

        # Get the prefered username from SQL if defined
        poss_users = []
        poss_users.append(my_user)
        poss_users.append("NONE")
        if playbooks_return[1]:
            if my_user != playbooks_return[1]:
                poss_users.append(playbooks_return[1])
            suggested = playbooks_return[1]
            selected_user = fzf.fzfs(
                poss_users,
                "Specify user? (suggested: " + suggested + ")",
                "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
                1,
            )
        else:
            selected_user = fzf.fzfs(
                poss_users,
                "Specify user?",
                "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
                0,
            )

        # If we don't select none, then we specify a user in the command prompt
        if not selected_user == "NONE":
            cmd_args += "-u " + selected_user[0]

        # Check if we are to become root or not
        becomeRoot = fzf.fzfs(
            ["YES", "NO"],
            "Become Root?",
            "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
            playbooks_return[2],
        )

        # If we select to become root then we do so and prompt for login/sudo passwords
        if becomeRoot[0] == "YES":
            cmd_args += " -b -k -K "
        else:
            cmd_args += " "

        # Assemble and return the command back to the calling shell script
        command = cmd_prefix + cmd_args + cmd_suffix
        print(command)
