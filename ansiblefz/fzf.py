from pyfzf.pyfzf import FzfPrompt

# Instantiate fzf
fzf = FzfPrompt()


class Fzf(object):
    def __init__(self):
        pass

    def fzfc(self, selections, header, label, category = "None"):
        fzf_style = " --border=rounded --header-first --border-label-pos=15 --color=dark --inline-info"
        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style + " --preview 'python3 -m ansiblefz -c " + category + " -s \"{}\"'"

        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def fzfu(self, selections, header, label):
        fzf_style = " --border=rounded --header-first --border-label-pos=15 --color=dark --inline-info"

        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style + " --preview 'python3 -m ansiblefz -c {}'"
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata
