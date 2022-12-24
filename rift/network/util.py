import random


# Adapted From:
# https://maxhalford.github.io/blog/weighted-sampling-without-replacement/
def sample_without_replacement(population, weights=None, k=1, rng=random):
    if not weights:
        weights = [1 / len(population) for _ in range(len(population))]
    weights_sum = sum(weights)
    if weights_sum != 1:
        weights = [w / weights_sum for w in weights]
    v = [rng.random() ** (1 / w) for w in weights]
    order = sorted(range(len(population)), key=lambda i: v[i])
    result = [population[i] for i in order[-k:]]
    if k == 1:
        return result[0]
    return result
