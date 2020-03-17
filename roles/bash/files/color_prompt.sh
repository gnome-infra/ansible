
if [ -n "$PS1" ]; then

FOREG="\[`tput setaf 6 2> /dev/null`\]"
NORMAL="\[`tput sgr0 2> /dev/null`\]"
BOLD="\[`tput bold 2> /dev/null`\]"
#FOREG="\[[36m\]"
#NORMAL="\[(B[m\]"
#BOLD="\[[1m\]"

if [ "$UID" != "0" ]; then
	ALT_FOREG="\[[34m\]"
else
	ALT_FOREG="\[[31m\]"
fi	

if [ -z "${TERM%xterm*}" ]; then
	PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}: ${PWD}\007"'
fi
PS1="${NORMAL}${FOREG}[${BOLD}${ALT_FOREG}\u${NORMAL}${FOREG}@${BOLD}${ALT_FOREG}\h${NORMAL} \W${FOREG}]${NORMAL}\\\$ "

export PS1

fi

