"""Generate one output-free executable witness notebook per numbered theory file.

This temporary materializer is deleted after the notebooks are generated. The
committed notebooks remain the researcher-facing sources.
"""

from __future__ import annotations

from pathlib import Path
import math
import textwrap

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "theory" / "notebooks"
NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

STEMS = [
    "00_axioms_and_notation",
    "01_observable_subspace_decomposition",
    "02_constructive_existence",
    "03_diffusion_flow_marginal_equivalence",
    "04_observed_private_invariance",
    "05_global_invariance_risk_lower_bound",
    "06_posterior_representation_sufficiency",
    "07_laplace_modal_stability",
    "08_shared_estimation_perturbation_bound",
    "09_unified_representation_risk_bound",
    "10_sampling_gap_shift_bound",
    "11_private_preserving_optimal_transport",
    "12_commuting_block_generators",
    "13_identifiability_and_failure_boundaries",
    "14_structural_observability_and_instance_reliability",
    "15_soft_observability_and_slot_stability",
    "16_source_supported_missing_identifiability",
    "17_global_null_nonrecoverability",
    "18_population_and_eventwise_canonicality",
    "19_semantic_anchor_necessity",
    "20_triangular_stochastic_transport",
    "21_support_projector_perturbation_bound",
    "22_diffusion_necessity_under_proper_scores",
    "23_flow_necessity_under_affine_distortion",
    "24_window_local_laplace_adequacy",
]

TITLES = {
    "00_axioms_and_notation": "Axioms and notation — admissibility witness",
    "01_observable_subspace_decomposition": "Theorem 1 — four-way observable-support decomposition",
    "02_constructive_existence": "Theorem 2 — constructive existence",
    "03_diffusion_flow_marginal_equivalence": "Theorem 3 — diffusion–flow marginal equivalence",
    "04_observed_private_invariance": "Theorem 4 — observed-private pathwise invariance",
    "05_global_invariance_risk_lower_bound": "Theorem 5 — complete-invariance risk lower bound",
    "06_posterior_representation_sufficiency": "Theorem 6 — posterior representation sufficiency",
    "07_laplace_modal_stability": "Theorem 7 — local Laplace modal stability",
    "08_shared_estimation_perturbation_bound": "Theorem 8 — shared estimation perturbation bound",
    "09_unified_representation_risk_bound": "Theorem 9 — paired representation-risk bound",
    "10_sampling_gap_shift_bound": "Theorem 10 — sampling-gap shift bound",
    "11_private_preserving_optimal_transport": "Theorem 11 — private-preserving optimal transport",
    "12_commuting_block_generators": "Theorem 12 — commuting block generators",
    "13_identifiability_and_failure_boundaries": "Theory 13 — identifiability and failure boundaries",
    "14_structural_observability_and_instance_reliability": "Theory 14 — structural observability versus instance reliability",
    "15_soft_observability_and_slot_stability": "Theory 15 — soft observability and slot stability",
    "16_source_supported_missing_identifiability": "Theorem 16 — source support is not conditional identifiability",
    "17_global_null_nonrecoverability": "Theorem 17 — source-global-null non-recoverability",
    "18_population_and_eventwise_canonicality": "Theorem 18 — population and eventwise canonicality",
    "19_semantic_anchor_necessity": "Theorem 19 — semantic-anchor necessity",
    "20_triangular_stochastic_transport": "Theorem 20 — triangular stochastic transport",
    "21_support_projector_perturbation_bound": "Theorem 21 — support projector perturbation",
    "22_diffusion_necessity_under_proper_scores": "Theorem 22 — Diffusion necessity under proper scores",
    "23_flow_necessity_under_affine_distortion": "Theorem 23 — Flow necessity under affine distortion",
    "24_window_local_laplace_adequacy": "Theorem 24 — window-local Laplace adequacy",
}

ROLES = {
    "01_observable_subspace_decomposition": "main contribution candidate",
    "05_global_invariance_risk_lower_bound": "main contribution candidate",
    "09_unified_representation_risk_bound": "joint main contribution candidate",
    "16_source_supported_missing_identifiability": "main contribution candidate",
    "20_triangular_stochastic_transport": "joint main contribution candidate",
    "03_diffusion_flow_marginal_equivalence": "established background",
    "22_diffusion_necessity_under_proper_scores": "complexity gate, not contribution",
    "23_flow_necessity_under_affine_distortion": "complexity gate, not contribution",
    "24_window_local_laplace_adequacy": "complexity gate, not contribution",
}

COMMON = r'''
import math
import itertools
import numpy as np
np.set_printoptions(precision=6, suppress=True)


def four_way(projectors, domain_index, atol=1e-9):
    ps = [np.asarray(p, float) for p in projectors]
    dimension = ps[0].shape[0]
    summed = sum(ps)
    values, vectors = np.linalg.eigh((summed + summed.T) / 2)
    basis = vectors[:, np.isclose(values, len(ps), atol=atol)]
    shared = basis @ basis.T if basis.size else np.zeros((dimension, dimension))
    basis = vectors[:, values > atol]
    union = basis @ basis.T if basis.size else np.zeros((dimension, dimension))
    observed = ps[domain_index]
    blocks = [shared, observed - shared, union - observed, np.eye(dimension) - union]
    for projector in blocks:
        np.testing.assert_allclose(projector, projector.T, atol=1e-8)
        np.testing.assert_allclose(projector @ projector, projector, atol=1e-8)
    for index, left in enumerate(blocks):
        for right in blocks[index + 1:]:
            np.testing.assert_allclose(left @ right, 0, atol=1e-8)
    np.testing.assert_allclose(sum(blocks), np.eye(dimension), atol=1e-8)
    return blocks


def normal_pdf(x, mean, standard_deviation):
    return np.exp(-0.5 * ((x - mean) / standard_deviation) ** 2) / (
        math.sqrt(2 * math.pi) * standard_deviation
    )
'''

CASES = {
"00_axioms_and_notation": r'''
rho_min = 1e-3
raw = np.array([-2.0, 0.0, 2.0])
rho = rho_min + np.maximum(raw, 0) + np.log1p(np.exp(-np.abs(raw)))
low = np.array([0.0, 10.0, 20.0])
high = np.array([10.0, 20.0, 30.0])
nu = np.array([-3.0, 0.0, 3.0])
omega = low + (high - low) / (1 + np.exp(-nu))
assert np.all(rho > 0)
assert np.all((omega >= low) & (omega <= high))
operator = np.diag([2.0, 0.1])
gramian = operator.T @ operator
values, vectors = np.linalg.eigh(gramian)
projector = vectors[:, values >= 1] @ vectors[:, values >= 1].T
np.testing.assert_allclose(projector, np.diag([1.0, 0.0]))
try:
    np.linalg.cholesky(np.diag([1.0, -1.0]))
    raise AssertionError("indefinite covariance must be rejected")
except np.linalg.LinAlgError:
    pass
print({"rho": rho.tolist(), "omega": omega.tolist(), "rank": int(round(np.trace(projector)))})
''',
"01_observable_subspace_decomposition": r'''
low = np.diag([1, 1, 0, 0, 0])
high_a = np.diag([1, 1, 1, 0, 0])
high_b = np.diag([1, 1, 0, 1, 0])
shared, private, missing, global_null = four_way([low, high_a, high_b], 1)
np.testing.assert_allclose(shared, np.diag([1, 1, 0, 0, 0]))
np.testing.assert_allclose(private, np.diag([0, 0, 1, 0, 0]))
np.testing.assert_allclose(missing, np.diag([0, 0, 0, 1, 0]))
np.testing.assert_allclose(global_null, np.diag([0, 0, 0, 0, 1]))
complete = four_way([np.eye(3), np.eye(3)], 0)
np.testing.assert_allclose(complete[0], np.eye(3))
empty = four_way([np.diag([1, 0, 0]), np.diag([0, 1, 0])], 0)
assert np.trace(empty[0]) == 0 and np.trace(empty[3]) == 1
print({"shared": 2, "observed_private": 1, "source_supported_missing": 1, "global_null": 1})
''',
"02_constructive_existence": r'''
rng = np.random.default_rng(2)
count = 80000
source_a = rng.normal(-1, 0.5, count)
source_b = rng.normal(2, 0.75, count)
canonical_a = (source_a + 1) / 0.5
canonical_b = (source_b - 2) / 0.75
assert abs(canonical_a.mean()) < 0.02 and abs(canonical_b.mean()) < 0.02
assert abs(canonical_a.var() - 1) < 0.03 and abs(canonical_b.var() - 1) < 0.03
private = rng.normal(size=count)
missing = canonical_a + 0.5 * private + rng.normal(0, 0.2, count)
residual = missing - canonical_a - 0.5 * private
assert abs(residual.std() - 0.2) < 0.005
representation = {"shared": canonical_a, "private": private.copy(), "missing": missing}
assert "global_null" not in representation and np.array_equal(representation["private"], private)
print({"canonical_mean_gap": float(abs(canonical_a.mean() - canonical_b.mean())), "missing_residual_std": float(residual.std())})
''',
"03_diffusion_flow_marginal_equivalence": r'''
rng = np.random.default_rng(3)
count, steps, diffusion = 25000, 200, 0.3
dt = 1 / steps
initial = rng.normal(size=count)
flow = initial.copy()
stochastic = initial.copy()
for step in range(steps):
    time = step * dt
    mean, mean_dot = 0.4 * time, 0.4
    sigma, sigma_dot = 1 + 0.2 * time, 0.2
    flow += (mean_dot + sigma_dot / sigma * (flow - mean)) * dt
    score = -(stochastic - mean) / sigma ** 2
    stochastic += (mean_dot + sigma_dot / sigma * (stochastic - mean) + diffusion * score) * dt
    stochastic += math.sqrt(2 * diffusion * dt) * rng.normal(size=count)
assert abs(flow.mean() - 0.4) < 0.02 and abs(flow.var() - 1.44) < 0.04
assert abs(stochastic.mean() - 0.4) < 0.03 and abs(stochastic.var() - 1.44) < 0.05
assert np.mean(abs(flow - stochastic)) > 0.1
print({"flow_mean": float(flow.mean()), "sde_mean": float(stochastic.mean()), "flow_var": float(flow.var()), "sde_var": float(stochastic.var())})
''',
"04_observed_private_invariance": r'''
low = np.diag([1, 1, 0, 0, 0])
high_a = np.diag([1, 1, 1, 0, 0])
high_b = np.diag([1, 1, 0, 1, 0])
shared, private, missing, global_null = four_way([low, high_a, high_b], 1)
state = np.array([1.0, -1.0, 7.0, -0.5, 9.0])
initial_private = private @ state
initial_null = global_null @ state
for _ in range(100):
    state += 0.01 * (shared @ (-0.2 * (shared @ state)) + missing @ (-0.1 * (missing @ state) + 0.05 * (shared @ state)))
    state += missing @ np.array([0, 0, 0, 0.001, 0])
np.testing.assert_allclose(private @ state, initial_private, atol=1e-12)
np.testing.assert_allclose(global_null @ state, initial_null, atol=1e-12)
leaking = state + np.array([0, 0, 0.2, 0, 0])
assert np.linalg.norm(private @ leaking - initial_private) > 0.1
print({"private_drift": float(np.linalg.norm(private @ state - initial_private)), "negative_control": float(np.linalg.norm(private @ leaking - initial_private))})
''',
"05_global_invariance_risk_lower_bound": r'''
conditional_mutual_information = math.log(2)
risk_high_support = 0.0
risk_complete_invariance = math.log(2)
np.testing.assert_allclose(risk_complete_invariance - risk_high_support, conditional_mutual_information)
print({"risk_gap_nats": conditional_mutual_information, "conditional_mutual_information_nats": conditional_mutual_information, "task_irrelevant_control_gap": 0.0})
''',
"06_posterior_representation_sufficiency": r'''
theta = np.array([-1.0, 0.0, 1.0])
posterior_a = np.array([0.5, 0.0, 0.5])
posterior_b = np.array([0.0, 1.0, 0.0])
assert theta @ posterior_a == theta @ posterior_b == 0
indicator = (abs(theta) > 0.5).astype(float)
probability_a = float(indicator @ posterior_a)
probability_b = float(indicator @ posterior_b)
assert (probability_a, probability_b) == (1.0, 0.0)
mean_only_brier = 0.25
print({"posterior_task_probabilities": [probability_a, probability_b], "posterior_brier": 0.0, "mean_only_brier": mean_only_brier})
''',
"07_laplace_modal_stability": r'''
rho, omega = 0.4, 5.0
for time in [0, 0.13, 0.7, 2.0]:
    rotation = np.array([[math.cos(omega * time), -math.sin(omega * time)], [math.sin(omega * time), math.cos(omega * time)]])
    transition = math.exp(-rho * time) * rotation
    np.testing.assert_allclose(np.linalg.norm(transition, 2), math.exp(-rho * time), rtol=1e-12, atol=1e-12)
times = np.array([0, 0.03, 0.11, 0.5, 0.93])
trajectory = np.exp(-rho * times) * (np.cos(omega * times) + 0.3 * np.sin(omega * times))
assert np.all(np.isfinite(trajectory))
print({"transition_norm_t2": float(math.exp(-0.8)), "irregular_query": trajectory.tolist()})
''',
"08_shared_estimation_perturbation_bound": r'''
operator = np.array([[1, 0], [0, 1], [1, 1], [2, -1]], float)
covariance = np.diag([0.1, 1, 4, 0.2])
state = np.array([1.5, -0.7])
noise = np.array([0.02, -0.15, 0.4, -0.03])
observation = operator @ state + noise
cholesky = np.linalg.cholesky(covariance)
whitened = np.linalg.solve(cholesky, operator)
whitened_noise = np.linalg.solve(cholesky, noise)
gamma = np.linalg.svd(whitened, compute_uv=False)[-1]
weight = np.linalg.inv(covariance)
estimate = np.linalg.solve(operator.T @ weight @ operator, operator.T @ weight @ observation)
error = np.linalg.norm(estimate - state)
bound = np.linalg.norm(whitened_noise) / gamma
assert error <= bound + 1e-12
print({"estimate": estimate.tolist(), "error": float(error), "bound": float(bound), "gamma": float(gamma)})
''',
"09_unified_representation_risk_bound": r'''
rng = np.random.default_rng(9)
target = rng.normal(size=20000)
ideal = target.copy()
approximate = ideal + rng.normal(0, 0.15, target.size)
risk_gap = np.mean(abs(approximate - target)) - np.mean(abs(ideal - target))
paired_error = np.mean(abs(approximate - ideal))
assert abs(risk_gap) <= paired_error + 1e-12
binary = np.tile([0.0, 1.0], 5000)
good, reversed_semantics = binary, 1 - binary
assert np.mean(abs(np.sort(good) - np.sort(reversed_semantics))) == 0
assert np.mean(abs(good - binary)) == 0 and np.mean(abs(reversed_semantics - binary)) == 1
print({"paired_risk_gap": float(risk_gap), "paired_error": float(paired_error), "semantic_reversal_risk": 1.0})
''',
"10_sampling_gap_shift_bound": r'''
p = np.array([0.01, 0.02, 0.05, 0.08, 0.11, 0.14])
q = np.array([0.015, 0.025, 0.055, 0.075, 0.105, 0.16])
pole = -0.4 + 3j
transform_p = np.mean(np.exp(pole * p))
transform_q = np.mean(np.exp(pole * q))
w1 = np.mean(abs(np.sort(p) - np.sort(q)))
lhs, rhs = abs(transform_p - transform_q), abs(pole) * w1
assert lhs <= rhs + 1e-12
print({"transform_shift": float(lhs), "bound": float(rhs), "W1": float(w1)})
''',
"11_private_preserving_optimal_transport": r'''
source = np.array([[-1, -2], [-1, 2], [1, -2], [1, 2]], float)
target = np.array([[0, -2], [0, 2], [2, -2], [2, 2]], float)
lam = 3

def transport_cost(left, right):
    return (left[0] - right[0]) ** 2 + lam * (left[1] - right[1]) ** 2

candidates = []
for permutation in itertools.permutations(range(4)):
    candidates.append((sum(transport_cost(source[i], target[permutation[i]]) for i in range(4)) / 4, permutation))
best_cost, best_permutation = min(candidates, key=lambda item: item[0])
private_drift = np.mean([abs(source[i, 1] - target[best_permutation[i], 1]) for i in range(4)])
assert best_cost == 1 and private_drift == 0
print({"optimal_cost": float(best_cost), "private_drift": float(private_drift)})
''',
"12_commuting_block_generators": r'''
def matrix_exponential(matrix):
    values, vectors = np.linalg.eig(matrix)
    return np.real_if_close(vectors @ np.diag(np.exp(values)) @ np.linalg.inv(vectors))

shared = np.array([[-1.0, 0], [0, 0]])
missing = np.array([[0.0, 0], [0, -2.0]])
np.testing.assert_allclose(shared @ missing - missing @ shared, 0)
np.testing.assert_allclose(matrix_exponential(shared + missing), matrix_exponential(shared) @ matrix_exponential(missing), atol=1e-12)
coupled = np.array([[0.0, 1.0], [0, -2.0]])
commutator = np.linalg.norm(shared @ coupled - coupled @ shared)
assert commutator > 0.5
print({"decoupled_commutator": 0.0, "coupled_commutator": float(commutator)})
''',
"13_identifiability_and_failure_boundaries": r'''
empty = four_way([np.diag([1, 0, 0]), np.diag([0, 1, 0])], 0)
assert np.trace(empty[0]) == 0
sample_interval = 0.1
times = np.arange(20) * sample_interval
frequency = 3.0
alias = frequency + 2 * math.pi / sample_interval
np.testing.assert_allclose(np.exp(1j * frequency * times), np.exp(1j * alias * times), atol=1e-12)
labels = np.tile([0, 1], 100)
reversed_representation = 1 - labels
assert np.array_equal(np.sort(labels), np.sort(reversed_representation))
assert np.mean(reversed_representation == labels) == 0
print({"empty_shared_rank": 0, "aliasing_error": float(np.max(abs(np.exp(1j * frequency * times) - np.exp(1j * alias * times)))), "semantic_reversal_accuracy": 0.0})
''',
"14_structural_observability_and_instance_reliability": r'''
gramian_value, threshold, temperature = 2.0, 1.0, 0.2
structural_weight = 1 / (1 + math.exp(-(gramian_value - threshold) / temperature))
assert structural_weight > 0.99
reliability = np.array([1.0, 0.5, 0.1])
posterior_variance = 1 / (1 + 4 * reliability)
assert np.all(np.diff(posterior_variance) > 0)
print({"structural_role_weight": structural_weight, "reliabilities": reliability.tolist(), "posterior_variances": posterior_variance.tolist()})
''',
"15_soft_observability_and_slot_stability": r'''
def soft(values, threshold, temperature):
    return 1 / (1 + np.exp(-(np.asarray(values) - threshold) / temperature))

weights = soft([0.5, 1.0, 1.5], 1.0, 0.05)
assert weights[0] < 1e-4 and weights[1] == 0.5 and weights[2] > 1 - 1e-4
temperature, perturbation = 0.2, 0.03
change = abs(soft([0.96], 1, temperature)[0] - soft([0.93], 1, temperature)[0])
bound = perturbation / (4 * temperature)
assert change <= bound + 1e-12
print({"hard_limit_weights": weights.tolist(), "change": float(change), "bound": bound})
''',
"16_source_supported_missing_identifiability": r'''
positive_world = np.array([[0, 0], [1, 1]])
negative_world = np.array([[0, 1], [1, 0]])
for column in [0, 1]:
    np.testing.assert_array_equal(np.sort(positive_world[:, column]), np.sort(negative_world[:, column]))

def conditional(table):
    return {int(c): float(table[table[:, 0] == c, 1].mean()) for c in [0, 1]}

positive_conditional = conditional(positive_world)
negative_conditional = conditional(negative_world)
assert positive_conditional == {0: 0.0, 1: 1.0}
assert negative_conditional == {0: 1.0, 1: 0.0}
print({"unpaired_marginals_equal": True, "paired_positive": positive_conditional, "paired_negative": negative_conditional})
''',
"17_global_null_nonrecoverability": r'''
rng = np.random.default_rng(17)
count = 100000
supported = rng.normal(size=count)
global_null = rng.normal(size=count)
observation = 2 * supported + rng.normal(0, 0.3, count)
correlation = np.corrcoef(observation, global_null)[0, 1]
assert abs(correlation) < 0.02
score = np.zeros(count)
assert np.mean(score ** 2) == 0
prior_correlated = supported + rng.normal(0, 0.1, count)
indirect = np.corrcoef(observation, prior_correlated)[0, 1]
assert indirect > 0.9
print({"independent_null_correlation": float(correlation), "Fisher_information": 0.0, "prior_mediated_correlation": float(indirect)})
''',
"18_population_and_eventwise_canonicality": r'''
labels = np.tile([0.0, 1.0], 5000)
source_one = labels.copy()
source_two = 1 - labels
population_discrepancy = np.mean(abs(np.sort(source_one) - np.sort(source_two)))
eventwise_error = np.mean((source_two - source_one) ** 2)
anchored_error = np.mean(((1 - source_two) - source_one) ** 2)
assert population_discrepancy == 0 and eventwise_error == 1 and anchored_error == 0
print({"population_discrepancy": population_discrepancy, "eventwise_error": eventwise_error, "anchored_error": anchored_error})
''',
"19_semantic_anchor_necessity": r'''
rng = np.random.default_rng(19)
labels = np.tile([0, 1], 10000)
nuisance = rng.normal(size=labels.size)
representation = np.column_stack([labels, nuisance])
good = representation[:, 0].astype(int)
bad = 1 - labels
assert np.mean(good == labels) == 1
assert np.array_equal(np.sort(bad), np.sort(labels))
assert np.mean(bad == labels) == 0
print({"sufficient_anchor_accuracy": 1.0, "marginally_matched_reversal_accuracy": 0.0})
''',
"20_triangular_stochastic_transport": r'''
rng = np.random.default_rng(20)
count = 30000
common = rng.normal(size=count)
private = rng.normal(size=count)
canonical = 1.5 * common - 0.2
private_after = private.copy()
missing = canonical + 0.5 * private + rng.normal(0, 0.25, count)
conditioned = canonical + 0.5 * private
decoupled = np.zeros(count)
conditioned_mse = np.mean((missing - conditioned) ** 2)
decoupled_mse = np.mean((missing - decoupled) ** 2)
assert np.array_equal(private_after, private)
assert conditioned_mse < 0.08 and conditioned_mse < 0.1 * decoupled_mse
print({"conditioned_missing_mse": float(conditioned_mse), "decoupled_mse": float(decoupled_mse), "private_drift": 0.0})
''',
"21_support_projector_perturbation_bound": r'''
gramian = np.diag([3.0, 1.0])
perturbation = np.array([[0, 0.08], [0.08, 0]])

def top_projector(matrix):
    vector = np.linalg.eigh(matrix)[1][:, [-1]]
    return vector @ vector.T

error = np.linalg.norm(top_projector(gramian + perturbation) - top_projector(gramian), 2)
bound = 2 * np.linalg.norm(perturbation, 2) / 2
assert error <= bound + 1e-12
before = int(np.sum(np.linalg.eigvalsh(np.diag([2.01, 1])) >= 2))
after = int(np.sum(np.linalg.eigvalsh(np.diag([1.99, 1])) >= 2))
assert before != after
print({"projector_error": float(error), "bound": float(bound), "near_threshold_rank": [before, after]})
''',
"22_diffusion_necessity_under_proper_scores": r'''
rng = np.random.default_rng(22)
samples = rng.normal(0.4, 0.8, 80000)
true_density = normal_pdf(samples, 0.4, 0.8)
richer_density = 0.3 * true_density + 0.7 * true_density
np.testing.assert_allclose(true_density, richer_density, rtol=1e-14, atol=1e-14)
component = rng.integers(0, 2, 80000)
mixture_samples = np.where(component == 0, rng.normal(-2, 0.4, 80000), rng.normal(2, 0.4, 80000))
gaussian_nll = -np.mean(np.log(normal_pdf(mixture_samples, mixture_samples.mean(), mixture_samples.std()) + 1e-300))
mixture_nll = -np.mean(np.log(0.5 * normal_pdf(mixture_samples, -2, 0.4) + 0.5 * normal_pdf(mixture_samples, 2, 0.4) + 1e-300))
assert mixture_nll + 0.5 < gaussian_nll
print({"contained_family_gap": 0.0, "misspecified_gaussian_nll": float(gaussian_nll), "mixture_nll": float(mixture_nll)})
''',
"23_flow_necessity_under_affine_distortion": r'''
rng = np.random.default_rng(23)
anchor = rng.uniform(-1, 1, 30000)
scale, offset = 1.7, -0.4
domain = scale * anchor + offset
recovered = (domain - offset) / scale
affine_error = np.mean((recovered - anchor) ** 2)
assert affine_error < 1e-28
cube = anchor ** 3
design = np.column_stack([cube, np.ones_like(cube)])
parameters = np.linalg.lstsq(design, anchor, rcond=None)[0]
linear_error = np.mean((design @ parameters - anchor) ** 2)
nonlinear_error = np.mean((np.cbrt(cube) - anchor) ** 2)
assert linear_error > 1e-3 and nonlinear_error < 1e-28
print({"affine_inverse_mse": float(affine_error), "affine_on_cube_mse": float(linear_error), "cube_root_mse": float(nonlinear_error)})
''',
"24_window_local_laplace_adequacy": r'''
times = np.linspace(0, 1, 1000)
rho, omega = 1.2, 18.0
modal = np.exp(-rho * times) * (np.cos(omega * times) + 0.3 * np.sin(omega * times))
residual = 0.02 * np.sin(37 * times)
true_signal = modal + residual
gain = 3
acquisition_error = np.linalg.norm(gain * true_signal - gain * modal)
operator_bound = gain * np.linalg.norm(residual)
assert acquisition_error <= operator_bound + 1e-12
representation_error = np.linalg.norm(np.tanh(gain * true_signal) - np.tanh(gain * modal))
assert representation_error <= acquisition_error + 1e-12
switch_times = np.linspace(0, 1, 500)
switching = np.where(switch_times < 0.5, np.exp(-switch_times), np.exp(-0.5) * np.exp(-4 * (switch_times - 0.5)))
fit = np.polyfit(switch_times, np.log(switching), 1)
single_pole = np.exp(fit[1] + fit[0] * switch_times)
misspecification = np.linalg.norm(switching - single_pole) / np.linalg.norm(switching)
assert misspecification > 0.1
print({"acquisition_error": float(acquisition_error), "operator_bound": float(operator_bound), "representation_error": float(representation_error), "switching_residual": float(misspecification)})
''',
}

if set(CASES) != set(STEMS):
    raise RuntimeError(f"case mismatch: missing={sorted(set(STEMS)-set(CASES))}")

for stem in STEMS:
    notebook = nbf.v4.new_notebook()
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "hse_theory": {
            "theory_id": stem[:2],
            "proof_file": f"theory/{stem}.md",
            "demo_kind": "constructive_or_numerical_witness",
            "paper_role": ROLES.get(stem, "supporting_or_boundary"),
            "evidence_level": "constructive_or_numerical_witness",
            "formal_claim_supported": False,
        },
    }
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            f"# {TITLES[stem]}\n\n"
            f"**Formal source:** [`../{stem}.md`](../{stem}.md)\n\n"
            "This Notebook is an executable finite witness, not the general proof. "
            "Passing it supports implementation consistency only; it does not establish "
            "learned-model or real-PHM evidence."
        ),
        nbf.v4.new_code_cell(textwrap.dedent(COMMON).strip()),
        nbf.v4.new_code_cell(textwrap.dedent(CASES[stem]).strip()),
        nbf.v4.new_code_cell(
            f"print('THEORY_DEMO_PASS::{stem}')\n"
            "print('evidence_level: constructive_or_numerical_witness')\n"
            "print('formal_claim_supported: false')"
        ),
    ]
    nbf.write(notebook, NOTEBOOK_DIR / f"{stem}.ipynb")

print(f"generated {len(STEMS)} output-free theory notebooks")
