#export SVN_EDITOR="gvim --nofork"
# MacOSX Lion
export ARCHFLAGS="-arch x86_64"
export MACOSX_DEPLOYMENT_TARGET="10.11"
export SVN_EDITOR="subl -w"
export LC_ALL="en_US.UTF-8"
export LC_LANG=en_US.UTF-8
export LC_MESSAGES=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
export COPYFILE_DISABLE=1 #Remove resource forks from tar files
export PYTHONSTARTUP=~/.pythonrc.py
shopt -s histappend
export PROMPT_COMMAND='history -a'
# Don't put duplicate lines in the history
export HISTCONTROL=ignoreboth
export HISTSIZE=50000

# Docker
export DOCKER_HOST=tcp://192.168.99.100:2376
export DOCKER_CERT_PATH=~/.docker/machine/machines/default/
export DOCKER_TLS_VERIFY=1

unset LC_CTYPE

# GIT Magic
c_cyan=`tput setaf 6`
c_red=`tput setaf 1`
c_green=`tput setaf 2`
c_sgr0=`tput sgr0`

#Get git information
parse_git_branch () {
        git name-rev HEAD 2>/dev/null | sed 's#HEAD\ \(.*\)#(git::\1)#'
}

#Should we push?
parse_git_push () {
        git st 2>/dev/null|sed -ne "s/#\ Your\ branch\ is\ ahead\ of\ '.*' by \([0-9]*\)\ commits\{0,1\}./ +\1/p"
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
					if [ `git st -s --untracked-files=no 2>/dev/null|wc -l` -gt 0 ]
					then
                        color="${c_cyan}"
					else
						color="${c_green}"
					fi
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
export PS1='\[\e[32m\][\u@\h] \[\e[33m\w\] [\[$(branch_color)\]$(parse_git_branch)$(parse_git_push)$(parse_svn_branch_revision)\[${c_sgr0}\]\e[33m] \n\[\e[1;34m\][\t]\[\e[0m\] \$ '
