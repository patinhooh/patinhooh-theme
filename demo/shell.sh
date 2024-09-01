#!/bin/bash
for code in {0..15}; do
  printf "\x1b[48;5;%dm%3d\x1b[0m " $code $code
  if [ $((($code + 1) % 6)) -eq 0 ]; then
    echo
  fi
done

# Define colors
BLACK='\033[0;30m'
BRIGHTBLACK='\033[1;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
BRIGHTMAGENTA='\033[1;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
RESET='\033[0m'

# Define ASCII art with color codes
ASCII_ART="${BLACK}
  _______                     _____                          _    _      _
${BRIGHTBLACK} |__   __|                   / ____|                        | |  | |    (_)
${RED}    | | _   _  _ __    ___  | (___    ___   _ __ ___    ___ | |_ | |__   _  _ __    __ _
${GREEN}    | || | | || '_ \  / _ \  \___ \  / _ \ | '_ \` _ \  / _ \| __|| '_ \ | || '_ \  / _\` |
${YELLOW}    | || |_| || |_) ||  __/  ____) || (_) || | | | | ||  __/| |_ | | | || || | | || (_| |
${BLUE}    |_| \__, || .__/  \___| |_____/  \___/ |_| |_| |_| \___| \__||_| |_||_||_| |_| \__, |
${MAGENTA}         __/ || |                                                                   __/ |
${WHITE}        |___/ |_|                                                                  |___/
${RESET}"
# Define colors
BLACK='\033[0;30m'
BRIGHTBLACK='\033[1;90m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
BRIGHTMAGENTA='\033[1;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
RESET='\033[0m'

# Define ASCII art with color codes
ASCII_ART="${RED}
  _______                     _____                          _    _      _
${YELLOW} |__   __|                   / ____|                        | |  | |    (_)
${GREEN}    | | _   _  _ __    ___  | (___    ___   _ __ ___    ___ | |_ | |__   _  _ __    __ _
${CYAN}    | || | | || '_ \  / _ \  \___ \  / _ \ | '_ \` _ \  / _ \| __|| '_ \ | || '_ \  / _\` |
${BLUE}    | || |_| || |_) ||  __/  ____) || (_) || | | | | ||  __/| |_ | | | || || | | || (_| |
${MAGENTA}    |_| \__, || .__/  \___| |_____/  \___/ |_| |_| |_| \___| \__||_| |_||_||_| |_| \__, |
${RED}         __/ || |                                                                   __/ |
${YELLOW}        |___/ |_|                                                                  |___/
${RESET}"

# Print ASCII art
echo -e "$ASCII_ART"
