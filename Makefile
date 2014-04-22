#### CONSTANTS

# Remove internes_exploitable files from CSV_FILES because it is merged in
# medecins_exploitables file
CSV_FILES=dentistes.csv infirmiers.csv medecins_exploitables.csv pharmaciens.csv sagefemmes.csv medecins_inexploitables.csv internes_inexploitables.csv
RAW_FILES=$(addprefix data/raw/, $(CSV_FILES))
FORMATTED_FILES=$(patsubst %.csv,data/formatted/%.formatted.csv,$(CSV_FILES))
REFINED_FILES=$(patsubst %.csv,data/refined/%.refined.csv,$(CSV_FILES))
UNIFIER_DIR = data/unifier
vpath %.refined.csv data/refined/
vpath %.formatted.csv data/formatted/
vpath %.csv data/raw/


#### COMMANDS
all: refineall formatall
	make refineall
	make formatall

refineall: ${REFINED_FILES}
	echo "Refine all files"

formatall: ${FORMATTED_FILES}
	echo "Format all files"

clean:
	rm -f data/formatted/*.csv
	rm -f data/refined/*.csv
	rm -f data/raw/medecins_inexploitables.csv
	rm -f data/raw/internes_inexploitables.csv


data/refined/%.refined.csv: %.formatted.csv
	python scripts/apply_refine_operations_from_csv.py $< ${UNIFIER_DIR} $@

data/formatted/%.formatted.csv: %.csv
	if test -e scripts/format_$*.py ; \
	then python scripts/format_$*.py $< $@ ; \
	else if test -e scripts/format_$*.sh ; \
	then . scripts/format_$*.sh ; \
	else cp $< $@ ; \
	fi; fi;

data/formatted/sagefemmes.formatted.csv: data/raw/sagefemmes.csv
	cat $< | sed 's/,/ /g' | sed 's/;/,/g' > $@

data/raw/medecins_inexploitables.csv: data/raw/medecins_inexploitables.tsv
	cat $< | sed 's/,/ /g' | sed 's/	/,/g' > $@

data/raw/internes_inexploitables.csv: data/raw/internes_inexploitables.tsv
	cat $< | sed 's/,/ /g' | sed 's/	/,/g' > $@
