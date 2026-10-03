# Chuck Sudo: source this file from Zsh or load it as an Oh My Zsh custom plugin.
[[ -n ${ZSH_VERSION-} ]] || return 0
[[ ${_SUDO_CHUCK_LOADED:-0} == 1 ]] && return 0
typeset -g _SUDO_CHUCK_LOADED=1
typeset -g _SUDO_CHUCK_DIR=${${(%):-%x}:A:h}

_sudo_chuck_pick_joke() {
    local fortune_file="${SUDO_CHUCK_JOKES:-$_SUDO_CHUCK_DIR/jokes.txt}"
    local line entry='' index
    if (( ! ${#_SUDO_CHUCK_POOL} )); then
        typeset -ga _SUDO_CHUCK_POOL=()
        if [[ -r $fortune_file ]]; then
            while IFS= read -r line || [[ -n $line ]]; do
                if [[ $line == '%' ]]; then
                    [[ -n $entry ]] && _SUDO_CHUCK_POOL+=("$entry")
                    entry=''
                elif [[ -n $line ]]; then
                    entry+="${entry:+ }$line"
                fi
            done < "$fortune_file"
            [[ -n $entry ]] && _SUDO_CHUCK_POOL+=("$entry")
        fi
        if (( ! ${#_SUDO_CHUCK_POOL} )); then
            _SUDO_CHUCK_POOL=(
                'Chuck Norris can divide by zero.'
                'Chuck Norris can power solar panels. At night.'
                'Chuck Norris counted to infinity. Twice.'
            )
        fi
    fi
    index=$(( RANDOM % ${#_SUDO_CHUCK_POOL} + 1 ))
    # Avoid repeating the previous joke when a fresh cycle begins.
    if (( ${#_SUDO_CHUCK_POOL} > 1 )) && [[ ${_SUDO_CHUCK_POOL[index]} == "${_SUDO_CHUCK_LAST-}" ]]; then
        index=$(( index % ${#_SUDO_CHUCK_POOL} + 1 ))
    fi
    typeset -g _SUDO_CHUCK_LAST=${_SUDO_CHUCK_POOL[index]}
    _SUDO_CHUCK_POOL[index]=()
}

sudo_chuck_banner() {
    emulate -L zsh
    _sudo_chuck_pick_joke
    local renderer="$_SUDO_CHUCK_DIR/render.py"
    if [[ -r $renderer ]] && (( ${+commands[python3]} )); then
        command python3 "$renderer" "$_SUDO_CHUCK_LAST" && return 0
    fi
    print -r -- "$_SUDO_CHUCK_LAST"
    print -r -- "Chuck Norris doesn't sudo. The root user asks him for permission."
} >&2

# Preserve an existing sudo customization. The preview command still works.
if (( ${+functions[sudo]} || ${+aliases[sudo]} )); then
    print -u2 -- 'Chuck Sudo: existing sudo function/alias detected; only sudo_chuck_banner was loaded.'
    return 0
fi

function sudo {
    emulate -L zsh
    local arg probe_only=0 flags flag
    if [[ ! -t 0 || ! -t 2 || ${SUDO_QUIET:-0} == 1 ]]; then
        command sudo "$@"
        return $?
    fi
    # Examine only options, respecting arguments consumed by sudo options.
    local -i skip_value=0
    for arg in "$@"; do
        if (( skip_value )); then
            skip_value=0
            continue
        fi
        case $arg in
            --non-interactive|--stdin|--askpass|--reset-timestamp|--remove-timestamp|--help|--version|--list|--edit|--login|--shell)
                probe_only=1; break ;;
            --user|--group|--host|--prompt|--chdir|--chroot|--close-from|--command-timeout|--role|--type|--other-user)
                skip_value=1 ;;
            --*=*) ;;
            --) break ;;
            --validate|--preserve-env|--set-home|--preserve-groups|--background) ;;
            --*) probe_only=1; break ;;
            -*)
                # Combined short flags (-nv, -Sk, etc.) must also bypass art.
                # Stop at value-taking options so a username is not parsed as flags.
                flags=${arg#-}
                while [[ -n $flags ]]; do
                    flag=${flags[1]}
                    flags=${flags[2,-1]}
                    case $flag in
                        n|S|A|k|K|h|V|l|e|i|s) probe_only=1; break ;;
                        u|g|p|D|R|C|T|r|t|U)
                            [[ -z $flags ]] && skip_value=1
                            break ;;
                    esac
                done
                (( probe_only )) && break ;;
            *) break ;;
        esac
    done
    if (( ! probe_only )) && ! command sudo -n true 2>/dev/null; then
        sudo_chuck_banner
    fi
    command sudo "$@"
}
