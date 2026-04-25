#!/bin/bash

# ==========================================
# Default Variables
# ==========================================
WIKI="enwiki"
WGET_EXTRA_OPTS=""

# ==========================================
# Help Function
# ==========================================
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Downloads the latest Wikipedia pages-articles XML dump."
    echo ""
    echo "Options:"
    echo "  -w, --wiki WIKI       Target wiki project (e.g., enwiki, dewiki, frwiki)."
    echo "                        Default: $WIKI"
    echo "  -e, --extra OPTS      Additional wget options (wrap in quotes, e.g., '-c -q')."
    echo "                        Default: none"
    echo "  -h, --help            Show this help message and exit"
    echo ""
    echo "Example:"
    echo "  $0 --wiki dewiki --extra '-c'" 
    exit 0
}

# ==========================================
# Argument Parsing
# ==========================================
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -w|--wiki)
            if [[ -z "$2" ]]; then
                echo "Error: --wiki requires an argument"
                exit 1
            fi
            WIKI="$2"
            shift 2
            ;;
        -e|--extra)
            if [[ -z "$2" ]]; then
                echo "Error: --extra requires an argument"
                exit 1
            fi
            WGET_EXTRA_OPTS="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Error: Unknown parameter passed: $1"
            exit 1
            ;;
    esac
done

# ==========================================
# Construct Regex and Execute
# ==========================================
# Note: Removed the unnecessary backslashes before the forward slashes (\/) 
# as they aren't needed for regex or bash strings.
REGEX="https://dumps\.wikimedia\.org/${WIKI}/latest/${WIKI}-latest-pages-articles[0-9]*\.xml\.bz2"
BASE_URL="https://dumps.wikimedia.org/${WIKI}/latest/"

echo "==> Target Wiki: ${WIKI}"
echo "==> Match Regex: ${REGEX}"
echo "==> Base URL:    ${BASE_URL}"
echo "==> Executing wget..."

# We leave $WGET_EXTRA_OPTS unquoted so it correctly splits into separate arguments
wget -np -r --accept-regex "$REGEX" $WGET_EXTRA_OPTS "$BASE_URL"