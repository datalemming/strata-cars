from riak import RiakClient
c=RiakClient(protocol='pbc',nodes=[{'host':'192.168.0.15','port':8087}])
print c.ping()
