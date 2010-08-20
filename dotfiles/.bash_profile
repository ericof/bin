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
 
parse_git_branch ()
{
  if git rev-parse --git-dir >/dev/null 2>&1
  then
          gitver=$(git branch 2>/dev/null| sed -n '/^\*/s/^\* //p')
  else
          return 0
  fi
  echo -e $gitver
}

branch_color ()
{
        if git rev-parse --git-dir >/dev/null 2>&1
        then
                color=""
                if git diff --quiet 2>/dev/null >&2 
                then
                        color="${c_green}"
                else
                        color=${c_red}
                fi
        else
                return 0
        fi
        echo -ne $color
}

# user@server, relative path, current time 
export PS1='\[\e[32m\][\u@\h] \[\e[33m\w\] [\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\]] \n\[\e[1;34m\][\t]\[\e[0m\] \$ '

##
# Your previous /Users/erico/.bash_profile file was backed up as /Users/erico/.bash_profile.macports-saved_2010-07-06_at_18:14:32
##

# MacPorts Installer addition on 2010-07-06_at_18:14:32: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

