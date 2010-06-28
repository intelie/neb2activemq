#!/usr/bin/perl

while(my $line = <STDIN>) {
  next if( $line =~ m/^#/ );
  next if ( length($line) == 1 );
  $line =~ s/^\s+//;
  @chars = split(/ +/, $line);
  next if scalar @chars != 9;
	next if @chars[2] eq "PID";
	
  ($time, $ampm,
    $pid, $minflt, $majflt, $cpu_user,
    $cpu_system, $nswap,
    $cpu) = @chars;

  print "${time} ${cpu_system} ${cpu_user} ${nswap}\n";
	$|++;
}
