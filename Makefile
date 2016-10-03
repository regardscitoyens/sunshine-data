#### CONSTANTS

# Remove internes_exploitable files from CSV_FILES because it is merged in
# medecins_exploitables file
CSV_FILES=declaration_conventions.csv declaration_avantages.csv dentistes.csv infirmiers.csv medecins_exploitables.csv pharmaciens.csv sagefemmes.csv medecins_inexploitables.csv
RAW_FILES=$(addprefix data/raw/, $(CSV_FILES))
FORMATTED_FILES=$(patsubst %.csv,data/formatted/%.formatted.csv,$(CSV_FILES))
REFINED_FILES=$(patsubst %.csv,data/refined/%.refined.csv,$(CSV_FILES))
UNIFIER_DIR = data/unifier
vpath %.refined.csv data/refined/
vpath %.formatted.csv data/formatted/
vpath %.csv data/raw/

all: data/data4publication.tgz

cleanandmakeall: clean all

data/data4publication.tgz: data/public/beneficiaires.csv data/public/beneficiaires.top.csv data/public/labos.departements.csv data/public/labos.csv data/public/metiers.departements.csv data/public/avantages.departements.csv data/public/conventions.departements.csv
	tar zcvf data/data4publication.tgz data/public/*csv
data/public/beneficiaires.top.csv: data/public/beneficiaires.csv
	bash scripts/generate_public_beneficiaire_top.sh
data/public/beneficiaires.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl BENEFICIAIRE > data/public/beneficiaires.csv
data/public/labos.departements.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl LABO > data/public/labos.departements.csv
data/public/labos.csv: data/public/labos.departements.csv
	python scripts/generate_labos_aggrega.py > data/public/labos.csv
data/public/metiers.departements.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl METIER > data/public/metiers.departements.csv
data/public/avantages.departements.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl "NATURE AVANTAGE" > data/public/avantages.departements.csv
data/public/conventions.departements.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl "OBJET CONVENTION" > data/public/conventions.departements.csv

data/all.anonymes.csv: data/all.unames.csv
	bash scripts/generate_anon_file.sh

data/all.unames.csv: data/all.csv
#	python scripts/clean_nom_prenom.py
	perl scripts/unify_names_rpps.pl data/all.csv data/rpps.csv > tmp/all.unames.csv
	head -n 1 tmp/all.unames.csv > data/all.unames.csv
	sed 1d tmp/all.unames.csv | sort -u -t ',' -k 8,16 >> data/all.unames.csv

data/all.csv: ${REFINED_FILES}
	. scripts/create_global_csv.sh

refineall: ${REFINED_FILES}
	echo "Refine all files"

formatall: ${FORMATTED_FILES}
	echo "Format all files"

clean:
	rm -f data/formatted/*.csv
	rm -f data/refined/*.csv
	rm -f data/raw/medecins_inexploitables.csv
	rm -f data/raw/internes_inexploitables.csv

.mkdirs:
	mkdir -p data/formatted data/refined data/tmp data/public

data/refined/%.refined.csv: %.formatted.csv scripts/apply_refine_operations_from_csv.py .mkdirs data/unifier/BENEF_PS_QUALIFICATION.csv  data/unifier/DECL_AVANT_NATURE.csv  data/unifier/DECL_CONV_OBJET.csv  data/unifier/LABO.csv  data/unifier/ORIGIN.csv
	python scripts/apply_refine_operations_from_csv.py $< ${UNIFIER_DIR} $@

data/formatted/%.formatted.csv: %.csv .mkdirs
	if test -e scripts/format_$*.py ; \
	then python scripts/format_$*.py $< $@ ; \
	else if test -e scripts/format_$*.sh ; \
	then . scripts/format_$*.sh ; \
	else cp $< $@ ; \
	fi; fi;

data/raw/medecins_inexploitables.csv: data/raw/medecins_inexploitables.tsv
	cat $< | sed 's/,/ /g' | sed 's/	/,/g' > $@

data/raw/internes_inexploitables.csv: data/raw/internes_inexploitables.tsv
	cat $< | sed 's/,/ /g' | sed 's/	/,/g' > $@

data/raw/sagefemmes.csv:
	test -f data/raw/sagefemme.csv && mv data/raw/sagefemme.csv data/raw/sagefemmes.csv

data/raw/declaration_avantages.csv: data/tmp/exports-etalab.zip
	mv data/tmp/declaration_avantage_*.csv data/raw/declaration_avantages.csv
	touch data/raw/declaration_avantages.csv

data/raw/declaration_conventions.csv: data/tmp/exports-etalab.zip
	mv data/tmp/declaration_convention_*.csv data/raw/declaration_conventions.csv
	touch data/raw/declaration_conventions.csv

data/tmp/exports-etalab.zip:
	wget --continue -O data/tmp/exports-etalab.zip --no-check-certificate https://www.transparence.sante.gouv.fr/exports-etalab/exports-etalab.zip
	unzip data/tmp/exports-etalab.zip declaration*csv -d data/tmp/

