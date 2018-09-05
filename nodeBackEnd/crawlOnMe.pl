use strict;
use warnings;
use LWP::Simple qw(get);
use utf8;
binmode STDOUT, ':utf8';

sub uniq {
         #This works well, but we need more fine grained control
         #my %seen;
         #grep !$seen{$_}++, @_;
 
         my (@storeArray) = @_;
  
         foreach (my $i = 0; $i <= scalar(@storeArray); $i++)
         {
                 foreach (my $j = $i+1; $j < scalar(@storeArray); $j++)
                 {
                         my $idI = $1 if ($storeArray[$i] =~ m/^\((\d+)/);
                         my $idJ = $1 if ($storeArray[$j] =~ m/^\((\d+)/);
  
                         if ( $idI && $idJ && $idI eq $idJ )
                         {
				$storeArray[$j] = "";
                         }
                 }
        }

         return @storeArray;
}
 
sub cleanData
{
	my $filename = 'rawdata.sql';
 
	open(my $fh, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
		chomp(my @lines = <$fh>);
	close $fh;
 
	my @cleanData = uniq(@lines);
 
	# Remove trailing comma from array.
	print "Last element was: " . $cleanData[-1] . "\n";
	$cleanData[-1] =~ s/(\)),/$1/;
	print "Last element is now: " . $cleanData[-1] . "\n";

	open(my $fh2, '>:encoding(UTF-8)', "appidlist.sql") or die "cant open file to write clean data too. \n";
		foreach my $arrayEntry (@cleanData)
		{
			print $fh2 "$arrayEntry\n";
		}
	close($fh2);
}

sub createSQLFile
{
	my $filename = 'rawdata.sql';
	open(my $fh, '>:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
		print $fh "INSERT INTO appIdTable ( appId, productName, discount ) VALUES\n";
	close $fh;
}

sub scrapeDataToFile
{
	my ($pageNum) = @_;

	my $url = 'https://store.steampowered.com/search/?os=win%2Cmac%2Clinux&specials=1&page='.$pageNum;
	my $html = get $url or die "Unable to get HTML data, aborting incase Vavle is angry with us.";

	#my @appIDData = $html =~ m/<a href="https:\/\/store\.steampowered\.com\/app\/.*"  data-ds-appid="(.*)" onmouseover=/g;
	my @appIDData = $html =~ m/<a href="https:\/\/store\.steampowered\.com\/[A-z]{3}\/.*"  data-ds-.*="(\d+)"/g;
	my @productNameData = $html =~ m/<div class="col search_name ellipsis">.*\n.*<span class="title">(.*)<\/span>/g;

	foreach my $name (@productNameData)
	{
		if ($name =~ /'/)
		{
			print "$name has a comma thing escaping it...\n.";
			$name =~ s/'//;
		}
	}

	#my @discountData = $html =~ m/<div class="col search_discount responsive_secondrow">.*\n.*<span>(.*)<\/span>/g;
	my @discountData = $html =~ m/<div class="col search_discount responsive_secondrow">.*\n.*<span>-(.*)%<\/span>/g;

	# Basic error catching, if something goes wrong with the html parsing.
	my $appsize = scalar @appIDData;
	my $prodsize = scalar @productNameData;
	my $discsize = scalar @discountData;
	if ($appsize != $prodsize)
	{
		print "AppArraySize: $appsize : ProductArraySize: $prodsize : DiscountArraySize $discsize \n";
		die "Warning, arrays do not align for items on page $pageNum, aborting..."
	}

	foreach my $val (0..(@appIDData-1))
	{

		my $filename = 'rawdata.sql';
		open(my $fh, '>>:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
			print $fh "($appIDData[$val], \'$productNameData[$val]\',\'$discountData[$val]\'), \n";
		close $fh;
	}
}

print "Making SQL file if it doesn't exist\n";

createSQLFile() unless -e "rawdata.sql";

print "Done making SQL file if it didn't exist \n";

my $totalRuns = 1;
$| = 1;
for (my $i=1; $i <= $totalRuns; $i++) {
	print "Starting run ...\n";
	scrapeDataToFile($i);
	sleep(60);
	print "Finishing run ...\n";
}

cleanData();
