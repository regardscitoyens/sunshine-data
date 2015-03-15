#!/usr/bin/perl

$type = shift;
$nodepartement = shift || 0;

%types = ('LABO' => 2, 'METIER' => 1, 'NATURE AVANTAGE' => 7, 'OBJET CONVENTION' => 10, 'BENEFICIAIRE'=> 4);

open(CSV, "data/all.anonymes.csv");
$premiereligne = <CSV>;
while(<CSV>) {
    @l = split /,/;
    $dep = $l[5];
    if ($nodepartement) {
	$dep = 'DESACTIVE';
    }
    if (!$data{$l[$types{$type}]}{$dep}) {
	$data{$l[$types{$type}]}{$dep}{'AVANTAGE'} = 0;
	$data{$l[$types{$type}]}{$dep}{'CONVENTION'} = 0;
	$data{$l[$types{$type}]}{$dep}{'AVANTAGE_MONTANT'} = 0;
    }
    $data{$l[$types{$type}]}{$dep}{$l[0]}++;
    $data{$l[$types{$type}]}{$dep}{'TOTAL'}++;
    if ($l[0] eq 'AVANTAGE') {
	$data{$l[$types{$type}]}{$dep}{'AVANTAGE_MONTANT'} += $l[8];
    }
    $data{$l[$types{$type}]}{$dep}{'QUALIFICATION'} = $l[3] if ($type eq 'BENEFICIAIRE' && $l[3] && $l[3] ne 'Médecine générale' && $l[3] ne 'Non renseigné');
    $data{$l[$types{$type}]}{$dep}{'QUALIFICATION'} = $l[3] if ($type eq 'BENEFICIAIRE' && !$data{$l[$types{$type}]}{$dep}{'QUALIFICATION'} && $l[3]);
    $data{$l[$types{$type}]}{$dep}{'ORIGIN'} = $l[1] if ($type eq 'BENEFICIAIRE');
}
print $type;
print ",ORIGIN,QUALIFICATION" if ($type eq 'BENEFICIAIRE');
print ",DEPARTEMENT,NB TOTAL CONVENTIONS + AVANTAGES,NB CONVENTIONS,NB AVANTAGES,MONTANT AVANTAGES\n";
foreach $key (keys %data) {
    foreach $dep (keys %{$data{$key}}) {
	print $key;
	print ','.$data{$key}{$dep}{'ORIGIN'} if ($type eq 'BENEFICIAIRE');
	print ','.$data{$key}{$dep}{'QUALIFICATION'} if ($type eq 'BENEFICIAIRE');
	print ",$dep,";
	print $data{$key}{$dep}{'TOTAL'};
	print ",";
	print $data{$key}{$dep}{'CONVENTION'};
	print ",";
	print $data{$key}{$dep}{'AVANTAGE'};
	print ",";
	print $data{$key}{$dep}{'AVANTAGE_MONTANT'};
	print "\n";
    }
}
