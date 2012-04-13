grep -rl "ENV=dev" ../src/nebpublisher.sh | xargs sed -i 's/ENV=dev/ENV=prod/g' || : 
grep -rl "ENV=prod" ../src/nebpublisher.sh | xargs sed -i 's/ENV=qa/ENV=prod/g' || : 

grep -rl "ENV=dev" ../src/ipc2activemq.py | xargs sed -i 's/ENV=dev/ENV=prod/g' || : 
grep -rl "ENV=qa" ../src/ipc2activemq.py | xargs sed -i 's/ENV=qa/ENV=prod/g' || : 

grep -rl "DAEMON = False" ../src/ipc2activemq.py | xargs sed -i 's/DAEMON = False/DAEMON = True/g' || :

mv ../src/nebpublisher/conf/dev ../src/nebpublisher/conf/prod
cd ..
mkdir -p dist
tar -czvf dist/ipc2activemq.tar.gz lib/*.tar.gz src/__init__.py src/ipc2activemq.py src/nebpublisher.sh src/setup.py src/nebpublisher/__init__.py src/nebpublisher/connection_adapter.py src/nebpublisher/manager.py src/nebpublisher/stomp_consumer.py src/nebpublisher/utils src/nebpublisher/conf/prod src/nebpublisher/conf/log.ini  scripts/install*
