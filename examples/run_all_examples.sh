for f in *.py; do  # or wget-*.sh instead of *.sh
    if [[ ${f} != *"animated"* ]]; then 
	echo $f
	python3 "$f" 
	echo
	echo
    fi
done
