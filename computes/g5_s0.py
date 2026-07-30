# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""G5 §0 — orientation numbers.

Three chains, one per "generic question" the note answers:
  (A) short run / n-step   : two-state chain (L16 slide 5, L17 slide 7, L18 slide 3)
  (B) long run / steady    : same chain, limit of r_ij(n) and balance equations
  (C) endgame / absorption : four-state chain of L16 slide 6
  (D) a chain with NO limit: three-state periodic chain of L16 slide 6
Every number quoted in notes/src/fragments/g5_s0.html comes from here.
"""
import io
import json
import sys

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

out = {}

# ---------------------------------------------------------------- (A)+(B)
# Two-state chain: states 1,2 ; p11=.5 p12=.5 p21=.2 p22=.8   (L16 slide 5)
P = np.array([[0.5, 0.5],
              [0.2, 0.8]])

steps = [0, 1, 2, 3, 10, 100, 101]
r = {}
for n in steps:
    Rn = np.linalg.matrix_power(P, n)
    r[n] = Rn
    print(f"r(n={n}) =\n{Rn}")

out["two_state_P"] = P.tolist()
out["two_state_r"] = {str(n): r[n].tolist() for n in steps}

# Steady state by solving the balance equations pi = pi P with sum pi = 1.
# Linear system: (P^T - I) pi = 0, replace last row by the normalization.
A = P.T - np.eye(2)
A[-1, :] = 1.0
b = np.array([0.0, 1.0])
pi = np.linalg.solve(A, b)
print("pi (balance equations) =", pi)
out["two_state_pi"] = pi.tolist()
out["two_state_pi_exact"] = ["2/7", "5/7"]
out["two_state_pi_frac_check"] = [2 / 7, 5 / 7]

# how fast: max deviation of r_ij(n) from pi_j
dev = {}
for n in [1, 2, 3, 5, 10, 20]:
    Rn = np.linalg.matrix_power(P, n)
    dev[n] = float(np.max(np.abs(Rn - np.vstack([pi, pi]))))
    print(f"max |r_ij({n}) - pi_j| = {dev[n]:.6g}")
out["two_state_convergence_gap"] = dev
# second eigenvalue governs the geometric decay rate
eig = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
print("eigenvalue moduli:", eig)
out["two_state_eig_abs"] = eig.tolist()

# ---------------------------------------------------------------- (D)
# Three-state periodic chain: p12=1, p21=.5, p23=.5, p32=1  (L16 slide 6)
Q = np.array([[0.0, 1.0, 0.0],
              [0.5, 0.0, 0.5],
              [0.0, 1.0, 0.0]])
r22 = {n: float(np.linalg.matrix_power(Q, n)[1, 1]) for n in range(0, 9)}
print("periodic chain r22(n) =", r22)
out["periodic_r22"] = {str(k): v for k, v in r22.items()}

# ---------------------------------------------------------------- (C)
# Four-state chain: 1 absorbing; 2: self .4, ->1 .3, ->3 .3; {3,4} recurrent class
# (L16 slide 6; the 3<->4 arcs are unlabelled, take p34=p43=0.5 -- only the
#  {3,4} class membership matters for the numbers quoted).
R = np.array([[1.0, 0.0, 0.0, 0.0],
              [0.3, 0.4, 0.3, 0.0],
              [0.0, 0.0, 0.5, 0.5],
              [0.0, 0.0, 0.5, 0.5]])
big = np.linalg.matrix_power(R, 400)
print("r_11(n) ->", big[0, 0], " r_31(n) ->", big[2, 0], " r_21(n) ->", big[1, 0])
out["four_state_r11_limit"] = float(big[0, 0])
out["four_state_r31_limit"] = float(big[2, 0])
out["four_state_r21_limit"] = float(big[1, 0])
# exact absorption probability from state 2 by first-step analysis:
# a = 0.3*1 + 0.4*a + 0.3*0  =>  a = 0.3/0.6 = 0.5
a_exact = 0.3 / (1 - 0.4)
print("absorption prob from 2 into {1} (first-step analysis) =", a_exact)
out["four_state_absorption_from_2"] = float(a_exact)
# expected time to leave state 2 (geometric with success prob 0.6)
out["four_state_expected_exit_time_from_2"] = float(1 / 0.6)
print("expected time to leave state 2 =", 1 / 0.6)

# ---------------------------------------------------------------- sanity
assert np.allclose(P.sum(axis=1), 1) and np.allclose(Q.sum(axis=1), 1)
assert np.allclose(R.sum(axis=1), 1)
assert np.allclose(pi, [2 / 7, 5 / 7])
assert np.allclose(pi @ P, pi)

with open("d:/Python-UV/MIT_Applied_Prob/computes/g5_s0.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("\nwrote computes/g5_s0.json")
