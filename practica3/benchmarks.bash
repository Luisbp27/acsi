#!/bin/bash

case $1 in
	help)
		echo "Usage: bench <sysbench stress> <number cpus> <number iterations>"
		exit 1;
		;;
	sysbench) ;;
	stress) ;;
	*)
		echo "Define a valid monitor <sysbench stress>"
		exit 1
		;;
esac

if [ -z "$2" ] 
then # Check number of cpus
	echo "Define the number of cpus"
	exit 1
else
	if [ "$2" -lt 1 ] 
	then # Number of cpus < 1
		echo "Define a valid number of cpus"
		exit 1
	fi
fi

if [ -z "$3" ]
then # Check number of iterations
	echo "Define the number of iterations"
	exit 1
else
	if [ "$3" -lt 1 ]
	then # Number of iterations < 1
		echo "Define a valid number of iterations n > 1"
		exit 1
	fi
fi

# Here you can put the workloads you want to test
for i in 25000 50000 100000 150000 250000
do
	echo "=== Start workload $i ==="
	j=1

	while [ "$j" -le "$3" ]; do
		echo "$1 iteration $j..."

		case $1 in
			sysbench)
				sysbench --test=cpu --cpu-max-prime="$i" --num-threads="$2" run
				;; # Break

			stress)
				stress-ng --cpu="$2" --cpu-ops="$i"
				;; # Break
		esac

		echo "Done"
		j=$((j + 1))

		sleep 2
	done
	echo ""
done