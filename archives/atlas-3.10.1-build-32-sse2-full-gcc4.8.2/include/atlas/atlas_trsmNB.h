#ifndef ATLAS_TRSMNB_H
   #define ATLAS_TRSMNB_H

   #ifdef SREAL
      #define TRSM_NB 80
   #elif defined(DREAL)
      #define TRSM_NB 108
   #elif defined(SCPLX)
      #define TRSM_NB 60
   #elif defined(DCPLX)
      #define TRSM_NB 24
   #endif

#endif
