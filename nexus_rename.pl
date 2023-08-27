#!/bin/perl

use strict;
use warnings;
use Getopt::Long;


my $input;
my $output;
GetOptions ("input=s" 	=>\$input,
	    "output=s"  => \$output)
or die("Error in command line arguments\n");

my %one_line;
open (INPUT, "<", $input) or die;
open (OUTPUT, ">>", $output) or die;
while (<INPUT>){
	my $line=$_;
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

