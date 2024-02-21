import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 20})

rs = np.linspace(0.95, 2.5, 100)
epsilon = 1
sigma = 1
wca = []
r_min_wca = 2 ** (1/6) * sigma
for r in rs:
    if r < r_min_wca:
        wca.append(4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6) + 1)
    else:
        wca.append(0)

lj = []
r_min_lj = 2.5 * sigma
for r in rs:
    if r < r_min_lj:
        lj.append(4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6))
    else:
        lj.append(0)

fig, ax = plt.subplots()
ax.set_xlabel('$r$')
ax.set_ylabel('$U$')
# ax.set_title('Потенциал Леннарда-Джонса')
ax.xaxis.set_major_locator(ticker.FixedLocator([sigma, r_min_wca]))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(['$\sigma$', '$2^\\frac{1}{6}\sigma$']))
ax.yaxis.set_major_locator(ticker.FixedLocator([0, -epsilon]))
ax.yaxis.set_major_formatter(ticker.FixedFormatter(['0', '$\epsilon$']))
(_, stemlines_sigma, __) = ax.stem([sigma], [0], linefmt='--', bottom=-epsilon-0.2)
stemlines_sigma.set_linewidth(0.9)
(_, stemlines_epsilon, __) = ax.stem([-epsilon], [2**(1/6)*sigma], linefmt='--', markerfmt='ob', orientation='horizontal')
stemlines_epsilon.set_linewidth(0.9)
(_, stemlines_threshold, __) = ax.stem([r_min_wca], [0], linefmt='--', markerfmt='ob', bottom=-epsilon-0.2)
stemlines_threshold.set_linewidth(0.9)
ax.plot(rs, wca, label='WCA')
ax.plot(rs, lj, label='LJ')
ax.legend()
ax.set_ylim(-epsilon-0.2)
ax.set_xlim(0.8)
ax.axhline(0, color='black', linewidth=0.5)
plt.show()