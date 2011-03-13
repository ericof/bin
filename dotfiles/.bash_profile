#export SVN_EDITOR="gvim --nofork"
export SVN_EDITOR="mate -w"
export LANG=en_US.UTF-8
export PYTHONSTARTUP=~/.pythonrc.py
export PYTHONPATH="~/Desenvolvimento/google_appengine:$PYTHONPATH"
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
export PATH="~/Desenvolvimento/google_appengine:$PATH"
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
        if [ `parse_git_branch|grep -c 'git'` -gt 0 ]
        then
                color=""
                if git diff --quiet 2>/dev/null >&2 
                then
                        color="${c_green}"
                else
                        color=${c_red}
                fi
        else
                if [ `parse_svn_branch_revision|grep -c 'svn'` -gt 0 ] 
                then	
						color=''
						##Parse st response
                        if [ `svn st -q|wc -l` -eq 0 ]
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

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

# user@server, relative path, current time 
export PS1='\[\e[32m\][\u@\h] \[\e[33m\w\] [\[$(branch_color)\]$(parse_git_branch)$(parse_svn_branch_revision)\[${c_sgr0}\]\e[33m] \n\[\e[1;34m\][\t]\[\e[0m\] \$ '
