# aminer-aelastic

This daemon polls logs from elasticsearch and writes it to a unix-domain-socket(for logdata-anomaly-miner)

# Installation

```
sudo make install
```

After that set owner of /var/lib/aelastic to aminer-user:

```
sudo chown aminer:aminer /var/lib/aelastic
```

# Poll manually

```
sudo /usr/lib/logdata-anomaly-miner/aelastic_daemon.py
```

# Starting the daemon

```
sudo systemctl enable aelastic_daemon
sudo systemctl start aelastic_daemon
```

# Testing

Normally the daemon starts polling the elasticsearch as soon as some other programm reads from the unix-domain-socket.
It is possible to read from the socket manually using the following command:

```
sudo ncat -U /var/lib/aminer/aminer.sock
```

# Uninstall

The following command will uninstall aelastic but keeps the configuration file:
```
sudo make uninstall
```
