export SVN_EDITOR=vim
export PATH=/opt/subversion/bin:$PATH
export PYTHONSTARTUP=~/.pythonrc.py
shopt -s histappend 
export PROMPT_COMMAND='history -a' 
# Don't put duplicate lines in the history 
export HISTCONTROL=ignoreboth 
export HISTSIZE=50000
# user@server, relative path, current time 
export PS1='\[\e[32m\][\u@\h] \[\e[33m\w\]\n\[\e[1;34m\][\t]\[\e[0m\] \$ '

##
# Your previous /Users/erico/.bash_profile file was backed up as /Users/erico/.bash_profile.macports-saved_2010-07-06_at_18:14:32
##

# MacPorts Installer addition on 2010-07-06_at_18:14:32: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

