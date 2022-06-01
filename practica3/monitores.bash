#!/bin/bash

if [ -z "$1" ]; then # Check monitor
    echo "Define a valid moitor <top, vm>"
    exit 1
else
    case $1 in 
	    help)
	        echo "Usage: mon <top vm> <delay> <messures>"
	        exit 1
		;;
	    top);;
	    vm) ;;
	    *)
            echo "Define a valid moitor <top, vm>"
            exit 1
		;;
    esac
fi

if [ -z "$2" ]; then # Check delay
    echo "Define a delay"
    exit 1
else

    if [ "$2" -lt 1 ]; then # delay < 1
        echo "Define a valid range of delay. d > 1"
        exit 1
    fi
fi

if [ -z "$3" ]; then # Check messures
    echo "Define the number of messures"
    exit 1
else
    if [ "$3" -lt 1 ]; then # messures < 1
        echo "Define a valid range of messures. n > 1"
        exit 1
    fi
fi

# Correct syntax
mkdir "./monitor" > /dev/null 2>&1
echo "=== Starting monitor ==="

printf "Work in process... "
case $1 in
	top)
		top -b -d "$2" -n "$3" | grep "%Cpu(s):" > tempCPU

    	sed -i 's/ni,100.0/ni, 100.0/g' tempCPU    # Add space to nice time. Avoid bug with awk
        awk '{print $2, $4, $8}' tempCPU > "./monitor/TOP.txt"  # Data filtering
        rm tempCPU
        ;; #break

    vm)
        vmstat "$2" "$3" -n >tempVM
            
        sed -i '1,2d' tempVM    # Remove first and second line (header)
        awk '{print $4}' tempVM > "./monitor/VM.txt"
        rm tempVM
        ;; #break
esac

echo "Done"