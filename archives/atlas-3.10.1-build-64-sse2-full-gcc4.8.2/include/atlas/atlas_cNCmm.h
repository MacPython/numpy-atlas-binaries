#ifndef CMM_H
   #define CMM_H

   #define ATL_mmNOMULADD
   #define ATL_mmLAT 4
   #define ATL_mmMU  4
   #define ATL_mmNU  1
   #define ATL_mmKU  4
   #define MB 76
   #define NB 76
   #define KB 76
   #define NBNB 5776
   #define MBNB 5776
   #define MBKB 5776
   #define NBKB 5776
   #define NB2 152
   #define NBNB2 11552

   #define ATL_MulByNB(N_) ((N_) * 76)
   #define ATL_DivByNB(N_) ((N_) / 76)
   #define ATL_MulByNBNB(N_) ((N_) * 5776)

#endif
