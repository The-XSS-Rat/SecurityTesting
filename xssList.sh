helpFunction()
{
   echo ""
   echo "Usage: $0 -a true/[EMPTY] -f domain.txt"
   echo -e "\t-f FileName(domains.txt or domain.lst)"
   echo -e "\t-a OPTIONAL: Advanced(run portscan on all ports), set to value true"
   exit 1 # Exit script after printing help
}

while getopts "f:a:" opt
do
   case "$opt" in
      f ) parameterF="$OPTARG" ;;
      a ) parameterA="$OPTARG" ;;
   esac
done

while read line; do
   echo "Starting: $line"
   python3 /Users/wesleythijs/Documents/BugBounties/ScriptsGeneral/XSStrike/xsstrike.py -u "$line" >> "XSS_$parameterF.txt"
done < "$parameterF"

