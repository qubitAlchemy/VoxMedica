import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ax.bar(np.arange(1, 5), [30.09, 41.95, 44.16, 46.53], 0.4, color='#0504aa',alpha=0.7)

for spine in plt.gca().spines.values():
    if spine.spine_type != 'bottom' and spine.spine_type != 'left':
        spine.set_visible(False)
plt.grid(axis='y', alpha=0.75)
plt.xticks(
    np.arange(1, 5),
    ['Amazon\nMedical\nTranscribe', 'Mozilla\nDeepSpeech', 'IBM\nWatson', 'Google\nSpeech\nRecognition'],
    fontsize=12)

plt.yticks(np.arange(0, 55, 5), ["%s%%" % str(x) for x in np.arange(0, 55, 5)])

plt.ylabel('Word Error Rate', fontsize=12)
plt.title('Comparison of Word Error Rate of Speech-to-Text Models and Services\n')
plt.show()