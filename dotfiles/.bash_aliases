#!/usr/bin/env bash
# Plone / Zope
alias bootstrap='wget http://downloads.buildout.org/1/bootstrap.py'

# headers (display headers for a http request)
alias headers="wget -S --delete-after"

# Simple HTTP Server
alias http_server="python -m SimpleHTTPServer"

# GUID (UUID4 gen)
alias guid="python -c 'from uuid import uuid4;print(uuid4())'"

# Sublime
function project_aware_subl {
    if [ -z "$1" ];then
        path="./"
    else
        path="$1"
    fi
    project_file=$(find "$path" -name '*.sublime-project' -d 1 2>/dev/null | head -n 1)
    /usr/local/bin/subl "${project_file:-"$path"}"
}

alias subl="project_aware_subl"