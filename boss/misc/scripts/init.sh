#!/bin/sh

# Boss Utilities
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'
COLOR_OFF='\033[0m'

echo_info() {
  printf "${COLOR_GREEN}${1}${COLOR_OFF}\n"
}

echo_fade() {
  printf "${COLOR_CYAN}${1}${COLOR_OFF}\n"
}

echo_error() {
  printf "${COLOR_RED}${1}${COLOR_OFF}\n"
}
