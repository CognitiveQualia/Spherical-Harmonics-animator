import itertools
import sys
import math
import scipy.special as sp
import numpy as np
import os
import imageio
import natsort

__author__ = 'Marcin Kucharski'


def get_param(filein):
    """
    Function gets data from input file.
    :param filein:
    Name of input file.
    :return:
    Array with data from file.
    """
    modee_freq = []
    a = []
    p = []
    l_ = []
    m = []
    f = open(filein, 'r')
    for lines in f:
        parts = lines.split()
        modee_freq.append(float(parts[0]))
        a.append(float(parts[1]))
        p.append(float(parts[2]))
        l_.append(float(parts[3]))  # degree
        m.append(float(parts[4]))  # order
    return modee_freq, a, p, l_, m


def combinations(n_teta, n_fi):
    """
    Function makes theta and fi combinations.
    :param n_teta:
    Number of theta parts.
    :param n_fi:
    Number of phi parts.
    :return:
    Array with combinations.
    """
    teta = np.linspace(0, math.pi, n_teta)
    fi = np.linspace(0, 2 * math.pi, n_fi)

    comb = list(itertools.product(fi, teta))
    return comb


def r_values(combine, t, delta_t, freq, a, p, l_, m, name):
    """
    Function calculates r values for time t.
    Writes results to .dat file, and calls function with gnuplot commands.
    After making .png images, converts them to gif animation and removes temporary files.
    :param combine:
    Array with combinations.
    :param t:
    Time
    :param delta_t:
    Time period.
    :param freq:
    Frequency from file.
    :param a:
    Amplitude from file.
    :param p:
    Phase from file.
    :param l_:
    Degree of Spherical harmonic.
    :param m:
    Azimuthal order of spherical harmonics.
    :param name:
    Name of the output gif.
    """
    r = []
    time = 0.0
    while time < t:
        f = open('%s.dat' % round(time, 2), 'w+')
        f.write("PHI    THETA   R\n")
        for element in combine:
            i = 0
            sum = 0.0
            while i < len(a):
                sum += (a[i] *
                        np.sqrt((2 * l_[i] + 1 *
                                 np.math.factorial(l_[i] - m[i])) /
                                (4 * np.pi * np.math.factorial(l_[i] + m[i]))) *
                        sp.lpmv(m[i], l_[i], np.cos(element[1])) *
                        np.cos(m[i] * element[0]) *
                        np.cos(2 * np.pi * freq[i] * time + p[i]))
                i += 1
            theta_zamiana = ((math.pi / 2) - float(element[1]))
            r = (1.0 + sum)
            f.write("{}     {}      {}\n".format(str(element[0]), theta_zamiana, r))
        f.close()
        gnuplot_template(time, time)
        os.system("%s.plt" % time)
        os.system("del /f %s.plt" % time)
        os.system("del /f %s.dat" % round(time, 2))
        time += delta_t
    to_gif(name)
    os.system("del /f *.png")


def gnuplot_template(filename, time):
    """
    Function creates gnuplot commands.
    :param filename:
    Name of the file with commands.
    :param time:
    A moment in animation.
    :return:
    File with commands.
    """
    f = open('%s.plt' % filename, 'w+')
    f.write('''set terminal pngcairo size 1600,1000 enhanced
set pm3d
set hidden3d
set palette rgb 23,28,3
set mapping spherical
set border linewidth 2
unset key
set mxtics
set xrange [-1.1:1.3]
set yrange [-1.1:1.3]
set zrange [-1.1:1.3]
set cbrange [0.95:1.1]
set mytics
set mztics
set mcbtics
set xtics font 'Helvetica,13' offset 0,-1,0
set ytics font 'Helvetica,13' offset 2,0,0
set ztics font 'Helvetica,13' offset 0,0,0
set cbtics font 'Helvetica,17'
set format x "%.1f"
set format y "%.1f"
set format z "%.1f"
set format cb "%.2f"
set xlabel '(X/R_{star})' font 'Helvetica,15' offset 0,-1
set ylabel '(Y/R_{star})' font 'Helvetica,15' offset 0,-1
set zlabel '(Z/R_{star})' font 'Helvetica,15' offset -4
set cblabel 'Radial Displacement (1+{/Symbol D}r/R_{star})' font 'Helvetica,15' offset 5''')
    f.write("\nset title 'Elapsed Time = %s d" % round(time, 2))
    f.write("""\nset title  font 'Helvetica,30' offset 0,0,-2
set view 65,45,1.1
set view equal xyz
set ticslevel 0.1""")
    f.write("\nset output '%s.png'" % round(time, 2))
    f.write("\nsplot '%s.dat' u 1:2:3:3 w p lt 7 ps 0.9 palette" % round(time, 2))
    f.close()


def to_gif(name):
    """
    Functon that converts .png files to gif.
    :param name:
    Name of the output file.
    :return:
    Animation in gif.
    """
    gif_name = '%s.gif' % name
    file_list = []
    filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]))
    # filenames = natsort.natsorted(filenames)  <--- Uncomment when the file name contains '10'
    for filename in filenames:
        file_list.append(imageio.imread(filename))
    duration = 0.05
    imageio.mimsave(gif_name, file_list, duration=duration)


def print_help():
    """Prints help for user"""
    print("Warning!\n Script syntax:\n app.py <filein.txt> <fileout> <T> <delta_t> <N_teta> <N_fi>")
    exit()


def main():
    print("***************************")
    print("****Spherical Harmonics****")
    print("***************************")
    if len(sys.argv) != 7:
        print_help()
    else:
        o = sys.argv[1]
        freq, a, p, l_, m = get_param(o)
        com = combinations(int(sys.argv[5]), int(sys.argv[6]))
        r_values(com, int(sys.argv[3]), float(sys.argv[4]), freq, a, p, l_, m, sys.argv[2])


if __name__ == '__main__':
    main()
