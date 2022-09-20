if [ $PGPASSWORD -z ]
then
	export PGPASSWORD=secretpassword
fi
psql -h localhost -U postgres -d notifserv
