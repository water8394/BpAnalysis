import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')


def measure_difference(real_Y, predict_Y, mad):
    diff = []
    for real, predict in zip(real_Y, predict_Y):
        diff.append(real - predict)

    plt.scatter(real_Y, diff)

    plt.plot([min(real_Y), max(real_Y)], [0, 0], c='r', alpha=0.4)
    # plt.plot([min(real_Y), max(real_Y)], [5, 5], c='r')
    # plt.plot([min(real_Y), max(real_Y)], [-5, -5], c='r')
    plt.plot([min(real_Y), max(real_Y)], [10, 10], c='r', alpha=0.4)
    plt.plot([min(real_Y), max(real_Y)], [-10, -10], c='r', alpha=0.4)
    plt.plot([min(real_Y), max(real_Y)], [20, 20], c='r', alpha=0.4)
    plt.plot([min(real_Y), max(real_Y)], [-20, -20], c='r', alpha=0.4)

    plt.title(f'Predict Value Plot    MAD = {round(mad, 2)} mmHg')
    plt.xlabel('Real value of BP (mmHg)')
    plt.ylabel('Measurement difference (mmHg)')
    plt.show()