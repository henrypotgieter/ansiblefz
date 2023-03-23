import os
import mysql.connector as mysql
from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv

fzf = FzfPrompt()


class Ansiblefz(object):
    def __init__(self):
        load_dotenv(".env")
        self.HOST = os.getenv("MYSQL_HOST")
        self.DB = os.getenv("MYSQL_DB")
        self.USER = os.getenv("MYSQL_USER")
        self.PASS = os.getenv("MYSQL_PASS")
        self.run()

    def run(self):
        # platform = ["EV", "NMS", "NOS", "GEM", "GEARS"]
        # actions = ["Update", "Inventory"]
        cmd_prefix = "ansible-playbook "
        cmd_args = ""

        platform = self.categories()
        platform_select = self.fzfu(platform, "Choose platform", "We will do it")

        # platform_selections = " ".join(platform_select)

        actions = self.playbooks(platform_select[0])

        cmd_suffix = self.directory(platform_select[0])

        actions_select = self.fzfc(
            actions, "Playbook Selection", "CMD: " + cmd_prefix + cmd_suffix
        )

        filedata = self.filedata(actions_select[0])
        cmd_suffix += "/" + filedata[0]

        # Get the username we are running the script as
        my_user = os.getlogin()

        # Get the prefered username from SQL if defined
        poss_users = []
        poss_users.append(my_user)
        poss_users.append("NONE")
        if filedata[1]:
            poss_users.append(filedata[1])
            suggested = filedata[1]
            selected_user = self.fzfs(
                poss_users,
                "Specify user? (suggested: " + suggested + ")",
                "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
                0,
            )
        else:
            selected_user = self.fzfs(
                poss_users,
                "Specify user?",
                "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
                0,
            )

        if not selected_user == "NONE":
            cmd_args += "-u " + selected_user[0]

        # Check if we are to become root or not
        becomeRoot = self.fzfs(
            ["YES", "NO"],
            "Become Root?",
            "CMD: " + cmd_prefix + cmd_args + " " + cmd_suffix,
            filedata[2],
        )

        if becomeRoot[0] == "YES":
            cmd_args += " -b -k -K "
        else:
            cmd_args += " "

        command = cmd_prefix + cmd_args + cmd_suffix
        print(command)

    def fzfc(self, selections, header, label):
        fzf_style = " --border=rounded --margin=10 --header-first --border-label-pos=15 --color=dark --inline-info"
        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def fzfu(self, selections, header, label):
        fzf_style = " --border=rounded --margin=30,10 --header-first --border-label-pos=15 --color=dark --inline-info"

        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def fzfs(self, selections, header, label, becomeRoot):
        fzf_style = " --border=rounded --margin=30,10 --header-first --border-label-pos=15 --color=dark --inline-info"
        if not becomeRoot:
            fzf_style += " --tac"

        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def sql_read(self, query):
        self.db_conn = mysql.connect(
            host=self.HOST, database=self.DB, user=self.USER, password=self.PASS
        )
        self.c = self.db_conn.cursor()
        self.c.execute(query)
        data = self.c.fetchall()
        self.db_conn.close()
        return data

    def sql_write(self, query):
        self.db_conn = mysql.connect(
            host=self.HOST, database=self.DB, user=self.USER, password=self.PASS
        )
        self.c = self.db_conn.cursor()
        data = self.c.execute(query)
        self.db_conn.commit()
        self.db_conn.close()
        return data

    def categories(self):
        tuples = self.sql_read("SELECT host_category FROM category")

        categories = []
        for category in tuples:
            categories.append(category[0])
        return categories

    def directory(self, host_category):
        tuples = self.sql_read(
            "SELECT playbook_dir FROM category WHERE host_category = '"
            + host_category
            + "'"
        )
        return tuples[0][0]

    def playbooks(self, host_category):
        tuples = self.sql_read(
            "SELECT scriptname FROM scripts WHERE host_category = '"
            + host_category
            + "'"
        )

        scriptnames = []
        for script in tuples:
            scriptnames.append(script[0])
        return scriptnames

    def filedata(self, scriptname):
        tuples = self.sql_read(
            "SELECT filename, req_user, req_become FROM scripts WHERE scriptname = '"
            + scriptname
            + "'"
        )
        return list(tuples[0])
