
REFINED_FILES = data/refined/medecins_inexploitables.csv data/refined/dentistes.csv data/refined/pharmaciens.csv data/refined/sagefemmes.csv #data/refined/medecins_exploitables.csv
UNIFIER_DATA = data/unifier/DECL_AVANT_NATURE.csv data/unifier/LABO.csv

data/all.json: data/all.csv
	csvjson data/all.csv > $@
data/all.csv: ${REFINED_FILES}
	csvstack ${REFINED_FILES} > $@

data/refined/medecins_inexploitables.csv: data/formatted/medecins_inexploitables.csv scripts/apply_refine_operations_from_csv.py ${UNIFIER_DATA}
	python scripts/apply_refine_operations_from_csv.py data/formatted/medecins_inexploitables.csv data/unifier $@

#data/refined/medecins_exploitables.csv: data/formatted/medecins_exploitables.csv scripts/apply_refine_operations.py
#	python scripts/apply_refine_operations.py data/formatted/medecins_exploitables.csv data/refine_operations/medecins_exploitables.json $@

data/refined/dentistes.csv: data/formatted/dentistes.csv scripts/apply_refine_operations_from_csv.py ${UNIFIER_DATA}
	python scripts/apply_refine_operations_from_csv.py data/formatted/dentistes.csv data/unifier $@

data/refined/pharmaciens.csv: data/formatted/pharmaciens.csv scripts/apply_refine_operations_from_csv.py ${UNIFIER_DATA}
	python scripts/apply_refine_operations_from_csv.py data/formatted/pharmaciens.csv data/unifier $@

data/refined/sagefemmes.csv: data/formatted/sagefemmes.csv scripts/apply_refine_operations_from_csv.py ${UNIFIER_DATA}
	python scripts/apply_refine_operations_from_csv.py data/formatted/sagefemmes.csv data/unifier $@

data/refined/infirmiers.csv: data/formatted/infirmiers.csv scripts/apply_refine_operations_from_csv.py ${UNIFIER_DATA}
	python scripts/apply_refine_operations_from_csv.py data/formatted/infirmiers.csv data/unifier $@

#data/formatted/medecins_exploitables.csv: scripts/format_exploitables_medecins.sh data/raw/medecins_exploitables.csv data/raw/internes_exploitables.csv data/headers.csv
#	. scripts/format_exploitables_medecins.sh

data/formatted/medecins_inexploitables.csv: data/raw/header_medecins_inexploitables data/raw/medecins_inexploitables.csv scripts/format_inexploitables_medecins.sh scripts/process_inexploitables_medecins.py data/raw/header_medecins_inexploitables
	. scripts/format_inexploitables_medecins.sh

data/formatted/dentistes.csv: data/raw/dentistes.csv scripts/format_dentistes.py
	python scripts/format_dentistes.py data/raw/dentistes.csv $@

data/formatted/pharmaciens.csv: data/raw/pharmaciens.csv scripts/format_pharmaciens.py
	python scripts/format_pharmaciens.py data/raw/pharmaciens.csv $@

data/formatted/infirmiers.csv: data/raw/infirmiers.csv scripts/format_infirmiers.py
	python scripts/format_infirmiers.py data/raw/infirmiers.csv $@

data/formatted/sagefemmes.csv: data/raw/sagefemme.csv
	in2csv data/raw/sagefemme.csv > $@

clean:
	rm -f data/formatted/*.csv
	rm -f data/refined/*.csv
