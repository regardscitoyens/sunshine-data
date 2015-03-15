#### CONSTANTS

# Remove internes_exploitable files from CSV_FILES because it is merged in
# medecins_exploitables file
CSV_FILES=dentistes.csv infirmiers.csv medecins_exploitables.csv pharmaciens.csv sagefemmes.csv medecins_inexploitables.csv transparencesante_avantages.csv transparencesante_conventions.csv
RAW_FILES=$(addprefix data/raw/, $(CSV_FILES))
FORMATTED_FILES=$(patsubst %.csv,data/formatted/%.formatted.csv,$(CSV_FILES))
REFINED_FILES=$(patsubst %.csv,data/refined/%.refined.csv,$(CSV_FILES))
UNIFIER_DIR = data/unifier
vpath %.refined.csv data/refined/
vpath %.formatted.csv data/formatted/
vpath %.csv data/raw/


#### COMMANDS
all: clean formatall refineall data/public/beneficiaires.csv data/public/beneficiaires.top.csv data/public/labos.departements.csv data/public/labos.departements.csv data/public/metiers.departements.csv data/public/avantages.departements.csv data/public/conventions.departements.csv

data/public/beneficiaires.top.csv: data/public/beneficiaires.csv
	bash scripts/generate_public_beneficiaire_top.sh
data/public/beneficiaires.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl BENEFICIAIRE > data/public/beneficiaires.csv
data/public/labos.departements.csv: data/all.anonymes.csv
	perl scripts/generate_public_aggrega.pl LABO > data/public/labos.departements.csv
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
	perl scripts/unify_names_rpps.pl data/all.csv > data/all.unames.csv

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
	touch .mkdirs

data/refined/%.refined.csv: %.formatted.csv scripts/apply_refine_operations_from_csv.py .mkdirs
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
