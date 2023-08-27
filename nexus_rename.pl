#!/bin/perl

use strict;
use warnings;
use Getopt::Long;

my %names=(
'GCA_000151295.1' => 'Allomyces_macrogynus',      
'GCA_000166175.1' => 'Microbotryum_lychnidis_dioicae',
'GCA_000183025.1' => 'Moniliophthora_perniciosa',
'GCA_000389695.3' => 'Ceratocystis_fimbriata',
'GCA_000412225.2' => 'Ashbya_aceris',
'GCA_000442015.1' => 'Rozella_allomycis',
'GCA_000988875.2' => 'Rhodotorula_toruloides',
'GCA_001191645.1' => 'Puccinia_striiformis',
'GCA_001466705.1' => 'Moniliophthora_roreri',
'GCA_001636735.1' => 'Beauveria_brongniartii',
'GCA_001636795.1' => 'Akanthomyces_lecanii',
'GCA_001969505.1' => 'Zancudomyces_culisetae',
'GCA_002760635.1' => 'Ganoderma_sinense',
'GCA_002794465.1' => 'Paramicrosporidium_saccamoebae',
'GCA_003344705.1' => 'Aspergillus_niger',
'GCA_006535955.1' => 'Synchytrium_endobioticum',
'GCA_007735645.1' => 'Venturia_effusa',
'GCA_009017415.1' => 'Aspergillus_flavus',
'GCA_009428345.1' => 'Tilletia_indica',
'GCA_009805715.1' => 'Hanseniaspora_uvarum',
'GCA_009809945.1' => 'Gigaspora_margarita',
'GCA_010203745.1' => 'Mucor_lusitanicus',
'GCA_011066465.2' => 'Verticillium_dahliae',
'GCA_011066565.1' => 'Orbilia_oligospora',
'GCA_011801645.1' => 'Rhizopus_arrhizus',
'GCA_014872705.1' => 'Agaricus_bisporus_var__burnettii',
'GCA_014904855.1' => 'Thelephora_ganbajun',
'GCA_016584185.1' => 'Kazachstania_unispora',
'GCA_016584205.1' => 'Rhodotorula_mucilaginosa',
'GCA_905067625.1' => 'Blumeria_graminis_f__sp__triticale',
'GCA_905337335.1' => 'Gomphillus_americanus',
'GCA_905337345.1' => 'Heterodermia_speciosa',
'GCA_905337355.1' => 'Imshaugia_aleurites',
'GCA_910890315.1' => 'Serendipita_indica',
'GCF_000001985.1' => 'Talaromyces_marneffei',
'GCF_000002515.2' => 'Kluyveromyces_lactis',
'GCF_000002525.2' => 'Yarrowia_lipolytica',
'GCF_000002545.3' => 'Candida_glabrata',
'GCF_000002655.1' => 'Aspergillus_fumigatus',
'GCF_000002715.2' => 'Aspergillus_clavatus',
'GCF_000002945.1' => 'Schizosaccharomyces_pombe',
'GCF_000003835.1' => 'Clavispora_lusitaniae',
'GCF_000006335.3' => 'Candida_tropicalis',
'GCF_000006445.2' => 'Debaryomyces_hansenii',
'GCF_000026365.1' => 'Zygosaccharomyces_rouxii',
'GCF_000091025.4' => 'Eremothecium_gossypii',
'GCF_000091045.1' => 'Cryptococcus_neoformans_var__neoformans',
'GCF_000142805.1' => 'Lachancea_thermotolerans',
'GCF_000143185.1' => 'Schizophyllum_commune',
'GCF_000143535.2' => 'Botrytis_cinerea',
'GCF_000146045.2' => 'Saccharomyces_cerevisiae',
'GCF_000146945.2' => 'Sclerotinia_sclerotiorum',
'GCF_000149035.1' => 'Colletotrichum_graminicola',
'GCF_000149205.2' => 'Aspergillus_nidulans_FGSC_A4',
'GCF_000149335.2' => 'Coccidioides_immitis',
'GCF_000149425.1' => 'Meyerozyma_guilliermondii',
'GCF_000149685.1' => 'Lodderomyces_elongisporus',
'GCF_000150035.1' => 'Vanderwaltozyma_polyspora',
'GCF_000150505.1' => 'Schizosaccharomyces_octosporus',
'GCF_000150735.1' => 'Paracoccidioides_brasiliensis',
'GCF_000151425.1' => 'Trichophyton_rubrum',
'GCF_000167675.1' => 'Trichoderma_reesei',
'GCF_000181695.1' => 'Malassezia_globosa',
'GCF_000182565.1' => 'Spizellomyces_punctatus',
'GCF_000182805.2' => 'Sordaria_macrospora',
'GCF_000182925.2' => 'Neurospora_crassa',
'GCF_000182965.3' => 'Candida_albicans',
'GCF_000184455.2' => 'Aspergillus_oryzae',
'GCF_000219625.1' => 'Zymoseptoria_tritici',
'GCF_000221225.1' => 'Thermochaetoides_thermophila',
'GCF_000225605.1' => 'Cordyceps_militaris',
'GCF_000226395.1' => 'Penicillium_rubens',
'GCF_000226545.1' => 'Podospora_anserina_S_mat_',
'GCF_000230625.1' => 'Exophiala_dermatitidis',
'GCF_000237345.1' => 'Naumovozyma_castellii',
'GCF_000243375.1' => 'Torulaspora_delbrueckii',
'GCF_000271585.1' => 'Trametes_versicolor',
'GCF_000271605.1' => 'Fomitiporia_mediterranea',
'GCF_000271745.1' => 'Fusarium_oxysporum',
'GCF_000280675.1' => 'Beauveria_bassiana',
'GCF_000293215.1' => 'Trichosporon_asahii_var__asahii',
'GCF_000315645.1' => 'Penicillium_digitatum',
'GCF_000315875.1' => 'Candida_orthopsilosis',
'GCF_000320585.1' => 'Heterobasidion_irregulare',
'GCF_000328475.2' => 'Ustilago_maydis',
'GCF_000439145.1' => 'Rhizophagus_irregularis',
'GCF_000516985.1' => 'Pestalotiopsis_fici',
'GCF_000721785.1' => 'Aureobasidium_pullulans',
'GCF_000814965.1' => 'Metarhizium_brunneum',
'GCF_000961545.1' => 'Sporothrix_schenckii',
'GCF_001278385.1' => 'Malassezia_pachydermatis',
'GCF_001477545.1' => 'Pneumocystis_carinii',
'GCF_001642055.1' => 'Alternaria_alternata',
'GCF_001661405.1' => 'Cyberlindnera_jadinii',
'GCF_001664035.1' => 'Metschnikowia_bicuspidata_var__bicuspidata',
'GCF_011745365.1' => 'Cryphonectria_parasitica',
'GCF_014466165.1' => 'Pleurotus_ostreatus',
'GCF_016906535.1' => 'Rhizoctonia_solani',
'GCF_019207475.1' => 'Ogataea_angusta',
'GCF_902498895.1' => 'Saprochaete_ingens',
'GCA_008802775.1' => 'Taphrina_betulina',
'GCA_000710275.1' => 'Penicillium_chrysogenum',
'GCF_021015755.1' => 'Lentinula_edodes',
'GCA_000149245.3' => 'Cryptococcus_neoformans_var__grubii_H99',
'GCA_000300575.2' => 'Agaricus_bisporus_var__bisporus_H97',
'GCA_000418435.1' => 'Blumeria_graminis_f__sp__tritici_96224',
'GCA_001275765.2' => 'Madurella_mycetomatis',
'GCA_005406105.1' => 'Zygosaccharomyces_mellis',
'GCA_006535975.1' => 'Chytriomyces_confervae',
'GCF_000300575.1' => 'Agaricus_bisporus_var__bisporus_H97'
);

my $input;
my $output;
GetOptions ("input=s" 	=>\$input,
			"output=s"  => \$output
			)
or die("Error in command line arguments\n");

my %one_line;
open (INPUT, "<", $input) or die;
open (OUTPUT, ">>", $output) or die;
while (<INPUT>){
	my $line=$_;
	#foreach my $acc(keys %names){
	#	$line=~s\$acc\$names{$acc}\g;
	#}
	my $len=0;
	if ($line=~/(^\-+)/g){
		$len=length($1);
		my $string = "X" x $len;
		$line=~s/^\-+/$string/g;
	}
	if ($line=~/(\-+$)/g){
		$len=length($1);
		my $string = "X" x $len;
		$line=~s/\-+$/$string/g;
	}
#if ($line=~/X(\-+)X/g){
#	$len=length($1);
#	my $string = "X" x $len;
#	$string="X".$string."X";
#	$line=~s/X.*X/$string/g;	
#}
#if ($line=~/(\.\-+)X/g){
#	$len=length($1);
#	my $string = "X" x $len;
#	$string.="X";
#	$line=~s/\.\-+X/$string/g;	
#}
#if ($line=~/(\.\-+)([A-W,Y-Z])/g){
#	$len=length($1);
#	my $string = "X" x $len;
#	$string.=$2;
#	$line=~s/\.\-+[A-Z]/$string/g;	
#}

	while ($line=~/(\-+X+\-+)/){
		$len=length($1);
		my $string = "X" x ($len);
		$line=~s/\-+X+\-+/$string/;	
	}
	while ($line=~/(X\-+)/){
		$len=length($1);
		my $string = "X" x ($len);
		$line=~s/X\-+/$string/;	
	}
	while ($line=~/(\.\-+)/){
		$len=length($1);
		my $string = "X" x ($len);
		$line=~s/\.\-+/$string/;	
	}
	while ($line=~/((\s+)\-+)/){
		$len=length($1);
		my $space_len=length($2);
		my $string = (" " x$space_len).("X" x ($len-$space_len));
		$line=~s/\s+\-+/$string/;	
	}
	$line=~s/X/\?/g;
	$line=~s/#NE\?US/\#NEXUS/g;
	
	print OUTPUT $line;
}

close INPUT; close OUTPUT;

