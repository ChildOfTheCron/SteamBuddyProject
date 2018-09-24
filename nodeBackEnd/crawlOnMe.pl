use strict;
use warnings;
use LWP::Simple qw(get);
use utf8;
use POSIX qw(strftime);
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
 
# Lets clean up our data, it's better than trying to parse HTML for every case ever.
# HTML parsing is inheritantly messy and if they do and change how it's formatted we have to redo a bunch of parsing
# Just grab the data in some kinda format that make sense and clean here
sub cleanData
{
	my ($filename) = @_;
	#my $filename = 'rawdata.sql';
 
	open(my $fh, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
		chomp(my @lines = <$fh>);
	close $fh;
 
	# Remove any potential dupes. Shouldn't really happen but I've had cases where it did for some weird reason
	my @cleanData = uniq(@lines);

	print "Why does printing this line fix my parser? $cleanData[-1]";

	# Add weird cases we need to catch and clean in this loop
	foreach my $line (@cleanData)
	{
		# Gets us the name of the title
		if ($line =~ /\(\d+,\s*'(.*)',.*,/)
		{
			# Attempt to remove those weird curley quotes as they are pure evil to parse
			$line =~ s/’//g;
			print "Name: $line\n";
		}
		if ($line =~ /\(\d+,\s*'.*',('')\),/)
		{
			$line =~ s/$1/0/;
			print "Game discount not parsed, setting empty discount to 0 for now.\n";
			#Todo, figure out why I cant parse these cases, there is a discount.
		}
	}

	# Remove empty array elements
	@cleanData = grep /\S/, @cleanData;

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
	my ($filename) = @_;
	#my $filename = 'rawdata.sql';
	open(my $fh, '>:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
		print $fh "INSERT INTO appIdTable ( appId, productName, discount ) VALUES\n";
	close $fh;
}

sub scrapeDataToFile
{
	my ($pageNum, $fileName) = @_;

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

		my $filename = $fileName;
		open(my $fh, '>>:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
			print $fh "($appIDData[$val], \'$productNameData[$val]\',\'$discountData[$val]\'), \n";
		close $fh;
	}
}

#my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime();
my $dateToday = strftime "%d_%m_%Y", localtime;
my $fileName = "rawdata_$dateToday.sql";
print "Making SQL file if it doesn't exist\n";

createSQLFile($fileName) unless -e $fileName;

print "Done making SQL file if it didn't exist \n";

my $totalRuns = 10;
$| = 1;
for (my $i=1; $i <= $totalRuns; $i++) {
	print "Starting run ...\n";
	scrapeDataToFile($i, $fileName);
	sleep(60);
	print "Finishing run ...\n";
}

cleanData($fileName);
