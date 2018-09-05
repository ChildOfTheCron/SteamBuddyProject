use strict;
use warnings;
use LWP::UserAgent();

my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;

my $response = $ua->get('http://search.cpan.org/');

if ($response->is_success)
{
	print $response->decoded_content;
}
else
{
	die $response->status_line;
}
