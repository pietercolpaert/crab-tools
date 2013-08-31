# CRAB : the address - geocode database for Flanders


## Set up

Download the CRAB db from http://download.agiv.be/Producten/Detail?id=102&title=CRAB_adresposities (it's free and open)

Be sure to have a postgis ready.

After you have unzipped the files, run this:

```bash
ogr2ogr -a_srs EPSG:31370 -f "PostgreSQL" PG:"host=localhost user=... dbname=... password=... port=5432" GML/terrobj.gml -overwrite
```

Wait for ~4hours (on a machine with 4 cores and an SSD)

(there are some common pitfalls when installing postgis. Just use the internet to get you out there if stuck.)

## Tools

Load the DBF (the data files) in the postgresql db:

First change them to csv using your favourite tool (a proprietery perl file in the bin/ folder of this repo may help)





