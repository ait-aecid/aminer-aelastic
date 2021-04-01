init:
	pip3 install -r requirements.txt

install: init
	test -d /usr/lib/aelastic || mkdir -p /usr/lib/aelastic
	cp -r aelastic/* /usr/lib/aelastic/
	test -d /etc/aminer/ || mkdir /etc/aminer/
	test -e /etc/aminer/elasticsearch.conf || cp etc/elasticsearch.conf /etc/aminer/elasticsearch.conf
	test -d /etc/systemd/system && cp etc/aelasticd.service /etc/systemd/system/aelasticd.service
	test -d /var/lib/aelastic || mkdir /var/lib/aelastic
	cp bin/aelasticd.py /usr/lib/aelastic/aelasticd.py
	test -e /usr/local/bin/aelasticd.py || ln -s /usr/lib/aelastic/aelasticd.py /usr/local/bin/aelasticd.py

uninstall:
	rm -rf /usr/lib/aelastic
	unlink /usr/local/bin/aelasticd.py

