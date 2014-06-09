#ifndef DMM_H
   #define DMM_H

   #define ATL_mmMULADD
   #define ATL_mmLAT 3
   #define ATL_mmMU  6
   #define ATL_mmNU  1
   #define ATL_mmKU  72
   #define MB 54
   #define NB 54
   #define KB 54
   #define NBNB 2916
   #define MBNB 2916
   #define MBKB 2916
   #define NBKB 2916
   #define NB2 108
   #define NBNB2 5832

   #define ATL_MulByNB(N_) ((N_) * 54)
   #define ATL_DivByNB(N_) ((N_) / 54)
   #define ATL_MulByNBNB(N_) ((N_) * 2916)
   #define NBmm ATL_dJIK54x54x54TN54x54x0_a1_b1
   #define NBmm_b1 ATL_dJIK54x54x54TN54x54x0_a1_b1
   #define NBmm_b0 ATL_dJIK54x54x54TN54x54x0_a1_b0
   #define NBmm_bX ATL_dJIK54x54x54TN54x54x0_a1_bX

#endif
