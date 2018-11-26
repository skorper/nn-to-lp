%['c20', 's20', 's21', 's22', 's23', 's24', 's25', 's26']
a2 :- z.
t1 :- x3, y3.
a4 :- z.
t3 :- x2, y3.
a6 :- z.
t5 :- x1, y3.
a8 :- z.
t7 :- x0, y3.
i7 :- a8, not t7.
i7 :- t7, not a8.
s7 :- i7, not z.
s7 :- z, not i7.
c7 :- a8, t7.
c7 :- z, i7.
i5 :- a6, not t5.
i5 :- t5, not a6.
s5 :- i5, not c7.
s5 :- c7, not i5.
c5 :- a6, t5.
c5 :- c7, i5.
i3 :- a4, not t3.
i3 :- t3, not a4.
s3 :- i3, not c5.
s3 :- c5, not i3.
c3 :- a4, t3.
c3 :- c5, i3.
i1 :- a2, not t1.
i1 :- t1, not a2.
s1 :- i1, not c3.
s1 :- c3, not i1.
c1 :- a2, t1.
c1 :- c3, i1.
t9 :- x3, y2.
t10 :- x2, y2.
t11 :- x1, y2.
t12 :- x0, y2.
t13 :- z.
i13 :- s7, not t13.
i13 :- t13, not s7.
s13 :- i13, not z.
s13 :- z, not i13.
c13 :- s7, t13.
c13 :- z, i13.
i12 :- s5, not t12.
i12 :- t12, not s5.
s12 :- i12, not c13.
s12 :- c13, not i12.
c12 :- s5, t12.
c12 :- c13, i12.
i11 :- s3, not t11.
i11 :- t11, not s3.
s11 :- i11, not c12.
s11 :- c12, not i11.
c11 :- s3, t11.
c11 :- c12, i11.
i10 :- s1, not t10.
i10 :- t10, not s1.
s10 :- i10, not c11.
s10 :- c11, not i10.
c10 :- s1, t10.
c10 :- c11, i10.
i9 :- c1, not t9.
i9 :- t9, not c1.
s9 :- i9, not c10.
s9 :- c10, not i9.
c9 :- c1, t9.
c9 :- c10, i9.
t14 :- x3, y1.
t15 :- x2, y1.
t16 :- x1, y1.
t17 :- x0, y1.
t18 :- z.
t19 :- z.
i19 :- s13, not t19.
i19 :- t19, not s13.
s19 :- i19, not z.
s19 :- z, not i19.
c19 :- s13, t19.
c19 :- z, i19.
i18 :- s12, not t18.
i18 :- t18, not s12.
s18 :- i18, not c19.
s18 :- c19, not i18.
c18 :- s12, t18.
c18 :- c19, i18.
i17 :- s11, not t17.
i17 :- t17, not s11.
s17 :- i17, not c18.
s17 :- c18, not i17.
c17 :- s11, t17.
c17 :- c18, i17.
i16 :- s10, not t16.
i16 :- t16, not s10.
s16 :- i16, not c17.
s16 :- c17, not i16.
c16 :- s10, t16.
c16 :- c17, i16.
i15 :- s9, not t15.
i15 :- t15, not s9.
s15 :- i15, not c16.
s15 :- c16, not i15.
c15 :- s9, t15.
c15 :- c16, i15.
i14 :- c9, not t14.
i14 :- t14, not c9.
s14 :- i14, not c15.
s14 :- c15, not i14.
c14 :- c9, t14.
c14 :- c15, i14.
t20 :- x3, y0.
t21 :- x2, y0.
t22 :- x1, y0.
t23 :- x0, y0.
t24 :- z.
t25 :- z.
t26 :- z.
i26 :- s19, not t26.
i26 :- t26, not s19.
s26 :- i26, not z.
s26 :- z, not i26.
c26 :- s19, t26.
c26 :- z, i26.
i25 :- s18, not t25.
i25 :- t25, not s18.
s25 :- i25, not c26.
s25 :- c26, not i25.
c25 :- s18, t25.
c25 :- c26, i25.
i24 :- s17, not t24.
i24 :- t24, not s17.
s24 :- i24, not c25.
s24 :- c25, not i24.
c24 :- s17, t24.
c24 :- c25, i24.
i23 :- s16, not t23.
i23 :- t23, not s16.
s23 :- i23, not c24.
s23 :- c24, not i23.
c23 :- s16, t23.
c23 :- c24, i23.
i22 :- s15, not t22.
i22 :- t22, not s15.
s22 :- i22, not c23.
s22 :- c23, not i22.
c22 :- s15, t22.
c22 :- c23, i22.
i21 :- s14, not t21.
i21 :- t21, not s14.
s21 :- i21, not c22.
s21 :- c22, not i21.
c21 :- s14, t21.
c21 :- c22, i21.
i20 :- c14, not t20.
i20 :- t20, not c14.
s20 :- i20, not c21.
s20 :- c21, not i20.
c20 :- c14, t20.
c20 :- c21, i20.
x3.
x1.
y3.
y0.
#show s.
