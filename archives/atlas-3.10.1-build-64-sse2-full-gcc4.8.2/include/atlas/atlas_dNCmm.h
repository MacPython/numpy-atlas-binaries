#ifndef DMM_H
   #define DMM_H

   #define ATL_mmNOMULADD
   #define ATL_mmLAT 5
   #define ATL_mmMU  6
   #define ATL_mmNU  1
   #define ATL_mmKU  48
   #define MB 48
   #define NB 48
   #define KB 48
   #define NBNB 2304
   #define MBNB 2304
   #define MBKB 2304
   #define NBKB 2304
   #define NB2 96
   #define NBNB2 4608

   #define ATL_MulByNB(N_) ((N_) * 48)
   #define ATL_DivByNB(N_) ((N_) / 48)
   #define ATL_MulByNBNB(N_) ((N_) * 2304)

#endif
