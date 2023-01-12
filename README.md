# Spherical Harmonics Animator
Python project for imaging star pulsations using spherical harmonics.
Program uses gnuplot for making images. And then combines them to a gif.


Proper syntax:
```
app.py <filein.txt> <fileout> <T> <delta_t> <N_teta> <N_fi>
```

File in:

Name of a five-column file containing modes parameters in which the star is pulsating.

Order: 
```diff
-! All parameters must be in the same line separated by the tab !-
1 Mode frequency f (c / d)
2 Amplitude A (R_sun)
3 Initial phase of mode p (rad)
4 Degree of spherical harmonics
5 Azimuth order
```


Sample output:
![](/spherical_harmonic_animation.gif)
