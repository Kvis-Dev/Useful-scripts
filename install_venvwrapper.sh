#!/bin/bash

vdir=~/venvs
bfile=~/.bashrc


py3=$( which python3 )

installer="#Kvis-Dev venvwrapper installer"

am_I_sourced()
{
	if [ "${FUNCNAME[1]}" = source ]; then
		if [ "$1" = -v ]; then
			echo ""
		fi
	return 0
	else
		if [ "$1" = -v ]; then
			echo ""
		fi
		return 1
	fi
}

if am_I_sourced -v; then

	cat $bfile | grep --quiet --regexp="$installer"
	test=$?

	if [[ $test -eq 0 ]]; then
		echo "Scrip already installed"
	else
		sudo pip3 install -U virtualenv virtualenvwrapper
		vw=$( which virtualenvwrapper.sh )

		export WORKON_HOME="$vdir"
		export VIRTUALENVWRAPPER_PYTHON="$py3"

		mkdir -p $WORKON_HOME

		printf '\n%s\n%s\n%s\n%s\n' "$installer" "export VIRTUALENVWRAPPER_PYTHON=$py3" "export WORKON_HOME=$vdir" "source $vw" >> $bfile

		source "$vw"
	fi
else
	echo "run this script with 'source $0'"
fi
