export SVN_EDITOR=vim
export PATH=/opt/subversion/bin:$PATH
export PYTHONSTARTUP=~/.pythonrc.py
shopt -s histappend 
export PROMPT_COMMAND='history -a' 
# Don't put duplicate lines in the history 
export HISTCONTROL=ignoreboth 
export HISTSIZE=50000

# GIT Magic
c_cyan=`tput setaf 6`
c_red=`tput setaf 1`
c_green=`tput setaf 2`
c_sgr0=`tput sgr0`
 
#Get git information
parse_git_branch () {
        git name-rev HEAD 2>/dev/null | sed 's#HEAD\ \(.*\)#(git::\1)#'
}

#Get svn information
##Get svn url
parse_svn_url() {
        svn info 2>/dev/null | sed -ne 's#^URL: ##p'
}

##Get svn repository root
parse_svn_repository_root() {
        svn info 2>/dev/null | sed -ne 's#^Repository Root: ##p'
}
##Get svn revision
parse_svn_current_revision() {
        svn info 2>/dev/null | sed -ne 's#^Revision: ##p'
}
##Parse everything and return the svn general info
parse_svn_branch_revision() {
    parse_svn_url | sed -e 's#^'"$(parse_svn_repository_root)"'##g' | awk -F / '{print $1 "/" $2 }' | awk '{print "(svn::_@" $1 ")" } ' | sed -e 's#_@#'"$(parse_svn_current_revision)"':#g'
}
branch_color ()
{
        if parse_git_branch >/dev/null 2>&1
        then
                color=""
                if git diff --quiet 2>/dev/null >&2 
                then
                        color="${c_green}"
                else
                        color=${c_red}
                fi
        else
                if parse_svn_branch_revision 2>/dev/null >&2 
                then
                        if svn diff 1>/dev/null >&2 
                        then
                                color="${c_green}"
                        else
                                color=${c_red}
                        fi
                else
                    return 0
                fi
        fi
        echo -ne $color
}

# user@server, relative path, current time 
export PS1='\[\e[32m\][\u@\h] \[\e[33m\w\] [\[$(branch_color)\]$(parse_git_branch)$(parse_svn_branch_revision)\[${c_sgr0}\]\e[33m] \n\[\e[1;34m\][\t]\[\e[0m\] \$ '

##
# Your previous /Users/erico/.bash_profile file was backed up as /Users/erico/.bash_profile.macports-saved_2010-07-06_at_18:14:32
##

# MacPorts Installer addition on 2010-07-06_at_18:14:32: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

