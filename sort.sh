DIR=$(cd $(dirname $0) && pwd )
echo  $DIR
cd ./merge_file
DIR=$(cd $(dirname $0) && pwd )
echo  $DIR
filelist=`ls $DIR`
for file in $filelist
do 
    echo $file
    sort -n -k 1 $file -o $file
done