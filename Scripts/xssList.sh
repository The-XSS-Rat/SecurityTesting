tput setaf 2;
echo "=========================================================="
echo "Welcome to my Nub Script for automating xssTrike"
echo ""
echo "Make sure you have Python3 intstalled and XSStrike/xsstrike.py in '$HOME'"
echo ""
echo "Usage: $0 -f domain.txt"
echo -e "\t-f FileName(domains.txt or domain.lst)"
echo "=========================================================="
tput sgr0;

helpFunction()
{
   tput setaf 2;
   echo ""
   echo "Usage: $0 -f domain.txt"
   echo -e "\t-f FileName(domains.txt or domain.lst)"
   tput sgr0;
   exit 1 # Exit script after printing help
}

while getopts "f:" opt
do
   case "$opt" in
      f ) parameterF="$OPTARG" ;;
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterF" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

while read line; do
   echo "Starting: $line"
   python3 $HOME/XSStrike/xsstrike.py -u "$line" >> "XSS_$parameterF.txt"
done < "$parameterF"
