#!/usr/bin/env bash
#
# Simple wrapper to run the output from the ansiblefz python script
# form within bash
#
# Uses unbuffer to preserve colouring

# Check where we start
START_DIR=$PWD

# And where the script exists
#SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
	DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)
	SOURCE=$(readlink "$SOURCE")
	[[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
SCRIPT_DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)

# Go insto the script directory
cd "$SCRIPT_DIR"

# Check if there's a .env file
if [ -f ".env" ]; then

	# Create a logfile name with timestamp
	TIMESTAMP=$(date "+%Y-%m-%d_%H%M%S")
	LOGDIR=$(sed -n 's/^LOG_DEST=\(.*\)/\1/p' <.env)
	LOGFILE="${LOGDIR}ansible_execution_${TIMESTAMP}.log"

	# Set the command to execute based on the output of ansiblefz python
	EXEC_CMD=$(python3 -m ansiblefz)

	# Check if unbuffer is installed silently
	command -v unbuffer 1>/dev/null 2>&1

	# Execute the command
	if [ $? -eq 0 ]; then
		eval "unbuffer ""$EXEC_CMD | tee -a ""$LOGFILE"
	else
		eval """$EXEC_CMD | tee -a ""$LOGFILE"
	fi

	# Change back to starting directory
	cd "$START_DIR"

	# Inform of logfile
	printf 'Logfile Written: %s\n' "$LOGFILE"

else
	echo "ERROR! - No .env file exists yet!"
	echo "Copy .env-example to .env and edit accordingly"
	exit 1
fi
