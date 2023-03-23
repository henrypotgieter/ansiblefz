from pyfzf.pyfzf import FzfPrompt

# Instantiate fzf
fzf = FzfPrompt()


class Fzf(object):
    def __init__(self):
        pass

    def fzfc(self, selections, header, label):
        fzf_style = " --border=rounded --margin=10% --header-first --border-label-pos=15 --color=dark --inline-info"
        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def fzfu(self, selections, header, label):
        fzf_style = " --border=rounded --margin=30,10% --header-first --border-label-pos=15 --color=dark --inline-info"

        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata

    def fzfs(self, selections, header, label, becomeRoot):
        fzf_style = " --border=rounded --margin=30,10% --header-first --border-label-pos=15 --color=dark --inline-info"
        if not becomeRoot:
            fzf_style += " --tac"

        options = (
            "--header='" + header + "' --border-label=' " + label + " '" + fzf_style
        )
        inputdata = fzf.prompt(selections, options)
        return inputdata
