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

#if advanced is set do a full portscan
if [ "$parameterA" == "true" ]
then
   echo "$parameterF"
   while read line; do
      echo "Starting: $line"
      sh initialScan.sh -h "$line" -o "$line" -a "true"   
   done < "$parameterF"
else
   echo "$parameterF"
   while read line; do
      echo "Starting: $line"
      sh initialScan.sh -h "$line" -o "$line"
   done < "$parameterF"
fi
