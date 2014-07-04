#umask 022
#if [ -f ~/.bash_profile ]; then
#    . ~/.bash_profile
#fi
#
#if [ -d ~/bin ] ; then
#    PATH=~/bin:"${PATH}"
#fi
#export PATH
export PATH=$HOME/local/bin:$PATH
