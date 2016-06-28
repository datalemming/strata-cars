from riak import RiakClient

c=RiakClient()
print c.ping()

fmt="""
	CREATE TABLE stratalaptimes (
		event varchar not null,
		ts timestamp not null,
		email varchar not null,
		laptime double not null,
		PRIMARY KEY(
			(event,quantum(ts, 5,'d')),
			event,ts)
			)
"""
c.ts_query('stratalaptimes',fmt)
