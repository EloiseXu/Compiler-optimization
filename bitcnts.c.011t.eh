
;; Function main1 (main1, funcdef_no=2, decl_uid=3622, cgraph_uid=2)

main1 (int argc, char * * argv, int print)
{
  static char * text[7] = {(char *) "Optimized 1 bit/loop counter", (char *) "Ratko\'s mystery algorithm", (char *) "Recursive bit count by nybbles", (char *) "Non-recursive bit count by nybbles", (char *) "Non-recursive bit count by bytes (BW)", (char *) "Non-recursive bit count by bytes (AR)", (char *) "Shift and count bits"};
  static int (*<T92d>) (long int) pBitCntFunc[7] = {bit_count, bitcount, ntbl_bitcnt, ntbl_bitcount, BW_btbl_bitcount, AR_btbl_bitcount, bit_shifter};
  int iterations;
  long int seed;
  long int n;
  long int j;
  int i;
  int D.3661;
  char * D.3660;
  long int D.3657;
  long int D.3656;
  int D.3655;
  int (*<T92d>) (long int) D.3654;
  char * D.3651;
  char * * D.3650;
  struct _IO_FILE * stderr.0;

  if (argc <= 1) goto <D.3647>; else goto <D.3648>;
  <D.3647>:
  stderr.0 = stderr;
  __builtin_fwrite ("Usage: bitcnts <iterations>\n", 1, 28, stderr.0);
  exit (1);
  <D.3648>:
  D.3650 = argv + 8;
  D.3651 = *D.3650;
  iterations = atoi (D.3651);
  if (print != 0) goto <D.3652>; else goto <D.3653>;
  <D.3652>:
  puts ("Bit counter algorithm benchmark\n");
  <D.3653>:
  i = 0;
  goto <D.3636>;
  <D.3635>:
  n = 0;
  j = n;
  seed = 1;
  goto <D.3633>;
  <D.3632>:
  D.3654 = pBitCntFunc[i];
  D.3655 = D.3654 (seed);
  D.3656 = (long int) D.3655;
  n = D.3656 + n;
  j = j + 1;
  seed = seed + 13;
  <D.3633>:
  D.3657 = (long int) iterations;
  if (D.3657 > j) goto <D.3632>; else goto <D.3634>;
  <D.3634>:
  if (print != 0) goto <D.3658>; else goto <D.3659>;
  <D.3658>:
  D.3660 = text[i];
  printf ("%-38s> Bits: %ld\n", D.3660, n);
  <D.3659>:
  i = i + 1;
  <D.3636>:
  if (i <= 6) goto <D.3635>; else goto <D.3637>;
  <D.3637>:
  D.3661 = 0;
  goto <D.3662>;
  <D.3662>:
  return D.3661;
}



;; Function bit_shifter (bit_shifter, funcdef_no=3, decl_uid=3618, cgraph_uid=3)

bit_shifter (long int x)
{
  int n;
  int i;
  int D.3667;
  unsigned int i.1;
  int D.3664;
  int D.3663;

  n = 0;
  i = n;
  goto <D.3644>;
  <D.3643>:
  D.3663 = (int) x;
  D.3664 = D.3663 & 1;
  n = D.3664 + n;
  i = i + 1;
  x = x >> 1;
  <D.3644>:
  if (x != 0) goto <D.3665>; else goto <D.3645>;
  <D.3665>:
  i.1 = (unsigned int) i;
  if (i.1 <= 63) goto <D.3643>; else goto <D.3645>;
  <D.3645>:
  D.3667 = n;
  goto <D.3668>;
  <D.3668>:
  return D.3667;
}


