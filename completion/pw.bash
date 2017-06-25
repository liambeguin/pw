_pw_autocomplete() {
	cmds="set get ccl tgl reset rename"
	outlets="$(pw list)"

	local cur prev words cword
	_init_completion || return

	case $prev in
	-h|--help|-V|--version)
		return
		;;
	get|set|ccl|reset|rename)
		COMPREPLY=(`compgen -W "$outlets" -- $cur`)
		return
		;;
	esac

	if [[ $cur == -* ]]; then
		COMPREPLY=( $( compgen -W '$( _parse_help "$1" )' -- "$cur" ) )
		return
	else
		COMPREPLY=( $( compgen -W "$cmds" -- "$cur" ) )
		return
	fi
}

complete -F _pw_autocomplete pw
