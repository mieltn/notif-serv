if [ $PGPASSWORD -z ]
then
	export PGPASSWORD=postgres
fi
psql -h localhost -U postgres -d postgres
