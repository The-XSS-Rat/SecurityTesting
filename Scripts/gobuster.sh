helpFunction()
{
   echo ""
   echo "Usage: $0 -a true/[EMPTY] -h domain.com -o main-site"
   echo -e "\t-u url(http://bla.domain.com/)"
   echo -e "\t-w Wordlist, default /Users/wesleythijs/Documents/BugBounties/SecurityTesting/wordlists/dirlist.txt"
   echo -e "\t-f domain list, leave empty if you want to do a single domain"
   echo -e "\t-m mode, default dir mode"
   exit 1 # Exit script after printing help
}

while getopts "u:w:m:" opt
do
   case "$opt" in
      u ) parameterU="$OPTARG" ;;
      w ) parameterW="$OPTARG" ;;
      m ) parameterM="$OPTARG" ;;
      f ) parameterF="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

if [ -z "$parameterW" ]
then
   parameterW="/Users/wesleythijs/Documents/BugBounties/SecurityTesting/wordlists/dirlist.txt"
fi

if [ -z "$parameterM" ]
then
   parameterM="dir"
fi

gobuster -w "$parameterW" "$parameterM" -u "$parameterU" -k
