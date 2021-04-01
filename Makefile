init:
	pip3 install -r requirements.txt

install: init
	test -d /usr/lib/logdata-anomaly-miner || mkdir -p /usr/lib/logdata-anomaly-miner
	cp -r aelastic /usr/lib/logdata-anomaly-miner
	test -d /etc/aminer/ || mkdir /etc/aminer/
	test -e /etc/aminer/elasticsearch.conf || cp etc/elasticsearch.conf /etc/aminer/elasticsearch.conf
	test -d /etc/systemd/system && cp etc/aelastic_daemon.service /etc/systemd/system/aelastic_daemon.service
	test -d /var/lib/aelastic || mkdir /var/lib/aelastic
	cp bin/aelastic_daemon.py /usr/lib/logdata-anomaly-miner/aelastic_daemon.py
	test -e /usr/local/bin/aelastic_daemon.py || ln -s /usr/lib/logdata-anomaly-miner/aelastic_daemon.py /usr/local/bin/aelastic_daemon.py

uninstall:
	rm -rf /usr/lib/logdata-anomaly-miner/aelastic
	rm -f /usr/lib/logdata-anomaly-miner/aelastic_daemon.py
	rm -f /usr/local/bin/aelastic_daemon.py

