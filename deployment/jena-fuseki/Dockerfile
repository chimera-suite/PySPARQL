FROM secoresearch/fuseki

COPY --chown=9008 simple-foaf.ttl /tmp/simple-foaf.ttl

RUN $TDBLOADER --graph=http://example.com/people /tmp/simple-foaf.ttl \
	&& $TEXTINDEXER \
	&& $SPATIALINDEXER \
	&& $TDBSTATS --graph urn:x-arq:UnionGraph > /tmp/stats.opt \
	&& mv /tmp/stats.opt /fuseki-base/databases/tdb/ \
	&& rm -r /tmp/*