tput setaf 2;
echo "=========================================================="
echo "Welcome to my Nub Script for automating Your initial scan of a domain."
echo ""
echo "Make sure you have nmap installed"
echo ""
echo ""
echo "Usage: $0 -a true/[EMPTY] -h domain.com -o main-site"
echo -e "\t-h Host(bla.domain.com or domain.com)"
echo -e "\t-o OutputName"
echo -e "\t-a OPTIONAL: Advanced(run portscan on all ports), set to value true"
echo "=========================================================="
tput sgr0;

helpFunction()
{
   echo ""
   echo "Usage: $0 -a true/[EMPTY] -h domain.com -o main-site"
   echo -e "\t-h Host(bla.domain.com or domain.com)"
   echo -e "\t-o OutputName"
   echo -e "\t-a OPTIONAL: Advanced(run portscan on all ports), set to value true"
   exit 1 # Exit script after printing help
}

while getopts "h:o:a:" opt
do
   case "$opt" in
      h ) parameterH="$OPTARG" ;;
      o ) parameterO="$OPTARG" ;;
      a ) parameterA="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterH" ] || [ -z "$parameterO" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

#if advanced is set do a full portscan
if [ "$parameterA" == "true" ]
then
   echo "Scanning all ports...-p- -sC -sV -oA"
   nmap -p- -sC -sV -oA "$parameterO" "$parameterH"
else
   echo "quick nmap scan..."
   nmap -sC -sV -oA "$parameterO" "$parameterH"
fi

