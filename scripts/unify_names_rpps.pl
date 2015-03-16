#!/usr/bin/perl

use Digest::MD5 qw(md5_hex);
$salt = rand();

sub tokenizeName($){
    $n = shift;
    $n =~ s/[çÇ]/c/ig;
    $n =~ s/[éèëêÉÈËÊ]/e/ig;
    $n =~ s/[àäâÀÄÂ]/a/ig;
    $n =~ s/[ïîÏÎ]/i/ig;
    $n =~ s/[ùüûÙÜÛ]/u/ig;
    $n =~ s/[ôöÔÖ]/o/ig;
    $n =~ s/[ÿŷŸŶ]/y/ig;
    $n =~ s/[^a-z]/ /ig;
    $n = uc($n);
    $n =~ s/(^|\s)(\S{1,2}|IDE|MADAME|MONSIEUR|DOCTEUR|PROFESSEUR|INFIRMIER|DRS|TITRE|STOMATOLOGUE|MEDECIN|DENTISTE)(\s|$)/ /g;
    $n =~ s/  */ /ig;
    $n =~ s/^ //ig;
    $n =~ s/ $//ig;
    @n = split / /, $n;
    if ($n[0] eq $n[($#n + 1)/2]) {
	$n = '';
	for ($i = 0 ; $i < ($#n + 1)/2 ; $i++) {
	    $n .= $n[$i].' ';
	}
	chop($n);
    }
    return $n;
}
sub associateNameCP($$) {
    $n = shift;
    $cp = shift;
    $cp =~ s/^(\d{2}).*/\1/;
    return $n." - ".$cp;
}
sub tokenizeNameCP($$){
    $n = tokenizeName(shift);
    return associateNameCP($n, shift);
}
sub trymatches($$) {
    $n = shift;
    $t = tokenizeName($n);
    $cp = shift;
    @t = split / /, $t;
    for ($i = 0 ; $i <= $#t ; $i++) {
	$id = associateNameCP(join( ' ',@t), $cp);
	return $id if($id2rpps{$id});
	return $id if($id2names{$id});
	push(@t, shift(@t));
    }
    $id2names{$id} = $n;
    return ;
}

$file = shift;

#extract RPPS
open FILE, $file;
while(<FILE>) {
    @l = split /,/;
    $id = '';
    if ($l[7] > 10000000000 && $l[7] < 99999999999 && $l[3] && $l[4]) {
	$l[7] =~ s/\.0//;
	$id = tokenizeNameCP($l[3], $l[4]);
	if ($id && !$rpps{$id}) {
	    $id2rpps{$id} = $l[7];
	    $id2names{$id} = $l[3];
	    $rpps2id{$l[7]} = $id;
	}
    }
}
close FILE;

#search for matches
open FILE, $file;
$_ = <FILE>;
chomp;
print;
print ",BENEF_PS_ID,BENEF_PS_DEPARTEMENT\n";
while(<FILE>){
    chomp;
    $id = '';
    while(s/"([^"]*),([^"]*)"/"\1 \2"/){};
    s/"//g;
    @l = split /,/;
    $l[17] = 'NC';
    $l[7] =~ s/\.0//;
    if ($l[7] && $rpps2id{$l[7]}) {
	$id = $rpps2id{$l[7]};
    }
    $id = trymatches($l[3], $l[4]) unless ($id);
    if ($id) {
	$l[7] = $id2rpps{$id};
	$l[3] = $id2names{$id};
    }
    if ($l[4]) {
	$l[17] = $l[4];
	$l[17] =~ s/^(\d{2}).*/\1/;
    }
    if ($l[7] > 10000000000 && $l[7] < 99999999999) {
	$l[16] = md5_hex($salt."RPPS:".$l[7]);
    }elsif($l[3] || $l[4]){
	$l[7] = '';
	$l[16] = md5_hex($salt."NOM/DEP:".$l[3].$l[4]);
    }else{
	$l[7] = '';
	$l[16] = md5_hex($salt."RANDOM:".rand());
    }
    print join(',',@l)."\n";
}
