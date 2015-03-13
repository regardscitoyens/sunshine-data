#!/usr/bin/perl

$type = shift;

%types = ('LABO' => 2, 'METIER' => 1, 'NATURE AVANTAGE' => 7, 'OBJET CONVENTION' => 10, 'BENEFICIAIRE'=> 4);

open(CSV, "data/all.anonymes.csv");
while(<CSV>) {
    @l = split /,/;
    $data{$l[$types{$type}]}{$l[5]}{$l[0]}++;
    $data{$l[$types{$type}]}{$l[5]}{'TOTAL'}++;
    if ($l[0] eq 'AVANTAGE') {
	$data{$l[$types{$type}]}{$l[5]}{'AVANTAGE_MONTANT'} += $l[8];
    }
    $data{$l[$types{$type}]}{$l[5]}{'QUALIFICATION'} = $l[3] if ($type eq 'BENEFICIAIRE' && $l[3]);
}
print $type;
print ",QUALIFICATION" if ($type eq 'BENEFICIAIRE');
print ",DEPARTEMENT,NB TOTAL CONVENTIONS + AVANTAGES,NB CONVENTIONS,NB AVANTAGES,MONTANT AVANTAGES\n";
foreach $key (keys %data) {
    foreach $dep (keys %{$data{$key}}) {
	print $key;
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
