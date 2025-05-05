rm -rf $1_pkg
mkdir $1_pkg
cp -r $1 shared $1/__init__.py $1/requirements.txt $1_pkg/

fission spec apply --wait -v=2
#rm -rf $1_pkg