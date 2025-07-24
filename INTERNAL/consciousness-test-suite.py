import random

def run_trial(observer_phi):
    return observer_phi >= 2.5 and random.random() > 0.3

conscious_results = [run_trial(3.0) for _ in range(100)]
unconscious_results = [run_trial(2.0) for _ in range(100)]

conscious_success = sum(conscious_results)
unconscious_success = sum(unconscious_results)

print("Conscious Success Rate:", conscious_success)
print("Unconscious Success Rate:", unconscious_success)