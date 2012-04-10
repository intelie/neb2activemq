grep -rl "ENV=dev" ../src/nebpublisher.sh | xargs sed -i 's/ENV=dev/ENV=prod/g' || : 
cp -R ../src/nebpublisher/conf/dev ../src/nebpublisher/conf/prod
cd ..
mkdir -p dist
tar -czvf dist/ipc2activemq.tar.gz lib/* src/* scripts/install*
