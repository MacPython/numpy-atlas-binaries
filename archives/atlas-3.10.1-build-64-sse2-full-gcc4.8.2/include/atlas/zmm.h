#ifndef ZMM_H
   #define ZMM_H

   #define ATL_mmMULADD
   #define ATL_mmLAT 5
   #define ATL_mmMU  2
   #define ATL_mmNU  2
   #define ATL_mmKU  2
   #define MB 58
   #define NB 58
   #define KB 58
   #define NBNB 3364
   #define MBNB 3364
   #define MBKB 3364
   #define NBKB 3364
   #define NB2 116
   #define NBNB2 6728

   #define ATL_MulByNB(N_) ((N_) * 58)
   #define ATL_DivByNB(N_) ((N_) / 58)
   #define ATL_MulByNBNB(N_) ((N_) * 3364)
void ATL_zJIK58x58x58TN58x58x0_a1_b0(const int M, const int N, const int K, const TYPE alpha, const TYPE *A, const int lda, const TYPE *B, const int ldb, const TYPE beta, TYPE *C, const int ldc);
void ATL_zJIK58x58x58TN58x58x0_a1_b1(const int M, const int N, const int K, const TYPE alpha, const TYPE *A, const int lda, const TYPE *B, const int ldb, const TYPE beta, TYPE *C, const int ldc);
void ATL_zJIK58x58x58TN58x58x0_a1_bX(const int M, const int N, const int K, const TYPE alpha, const TYPE *A, const int lda, const TYPE *B, const int ldb, const TYPE beta, TYPE *C, const int ldc);

   #define NBmm_b1(m_, n_, k_, al_, A_, lda_, B_, ldb_, be_, C_, ldc_) \
{ \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_), lda_, (B_), ldb_, ATL_rnone, C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_b1(m_, n_, k_, al_, (A_), lda_, (B_)+NBNB, ldb_, ATL_rone, (C_)+1, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_)+NBNB, ldb_, ATL_rnone, C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_b1(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_), ldb_, ATL_rone, (C_)+1, ldc_); \
   }
   #define NBmm_b0(m_, n_, k_, al_, A_, lda_, B_, ldb_, be_, C_, ldc_) \
{ \
   ATL_zJIK58x58x58TN58x58x0_a1_b0(m_, n_, k_, al_, (A_), lda_, (B_), ldb_, ATL_rzero, C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_b0(m_, n_, k_, al_, (A_), lda_, (B_)+NBNB, ldb_, ATL_rzero, (C_)+1, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_)+NBNB, ldb_, ATL_rnone, C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_b1(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_), ldb_, ATL_rone, (C_)+1, ldc_); \
   }
   #define NBmm_bX(m_, n_, k_, al_, A_, lda_, B_, ldb_, be_, C_, ldc_) \
{ \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_), lda_, (B_), ldb_, -(be_), C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_), lda_, (B_)+NBNB, ldb_, be_, (C_)+1, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_bX(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_)+NBNB, ldb_, ATL_rnone, C_, ldc_); \
   ATL_zJIK58x58x58TN58x58x0_a1_b1(m_, n_, k_, al_, (A_)+NBNB, lda_, (B_), ldb_, ATL_rone, (C_)+1, ldc_); \
   }
   #define rNBmm_b1 ATL_dJIK58x58x58TN58x58x0_a1_b1
   #define rNBmm_b0 ATL_dJIK58x58x58TN58x58x0_a1_b0
   #define rNBmm_bX ATL_dJIK58x58x58TN58x58x0_a1_bX

#endif
