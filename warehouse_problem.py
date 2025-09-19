import openjij as oj
import numpy as np
import random
from collections import defaultdict
from itertools import combinations

def generate_problem_data(config):
    """
    Generates random data for the knapsack problem based on configuration.

    Args:
        config (dict): A dictionary containing problem parameters.

    Returns:
        tuple: A tuple containing lists for values, weights, categories, 
               and taboo pairs of items.
    """
    n = config['num_items']
    num_categories = config['num_categories']
    
    # Use separate random seeds for reproducibility of each attribute
    random.seed(6)
    values = [random.randint(100, 1000) for _ in range(n)]
    
    random.seed(7)
    weights = [random.randint(10, 100) for _ in range(n)]
    
    random.seed(8)
    categories = [random.randint(0, num_categories - 1) for _ in range(n)]
    
    random.seed(9)
    taboo_pairs = []
    for _ in range(config['num_taboo_pairs']):
        # Ensure the pair is sorted to handle (i, j) and (j, i) consistently
        pair = tuple(sorted(random.sample(range(n), 2)))
        taboo_pairs.append(pair)
        
    return values, weights, categories, list(set(taboo_pairs)) # Return unique pairs

def build_qubo(values, weights, categories, taboo_pairs, config):
    """
    Constructs the QUBO dictionary for the given problem.

    Args:
        values (list): List of item values.
        weights (list): List of item weights.
        categories (list): List of item categories.
        taboo_pairs (list): List of tuples representing forbidden item pairs.
        config (dict): A dictionary containing problem parameters and penalties.

    Returns:
        defaultdict: The QUBO model as a dictionary.
    """
    n = config['num_items']
    max_weight = config['max_weight']
    
    # Penalty constants
    p_mass = config['penalty_mass']
    p_cat = config['penalty_category']
    p_taboo = config['penalty_taboo']

    # Initialize QUBO as a dictionary
    Q = defaultdict(float)

    # --- Objective Function ---
    # We want to MAXIMIZE the sum of values. In a QUBO, we MINIMIZE the energy.
    # So, we add the negative of the values to the diagonal.
    for i in range(n):
        Q[(i, i)] -= values[i]

    # --- Constraint 1: Total weight must not exceed max_weight ---
    # We add a penalty term: P_mass * (sum(w_i * x_i) - W_max)^2
    # This expands to: P_mass * [ sum(w_i^2 * x_i) + 2*sum_{i<j}(w_i*w_j*x_i*x_j) - 2*W_max*sum(w_i*x_i) ]
    # The constant term P_mass * W_max^2 is ignored as it only shifts the energy offset.
    for i in range(n):
        # Linear part (diagonal)
        Q[(i, i)] += p_mass * (weights[i]**2 - 2 * max_weight * weights[i])
        # Quadratic part (off-diagonal)
        for j in range(i + 1, n):
            Q[(i, j)] += p_mass * 2 * weights[i] * weights[j]
            
    # --- Constraint 2: Select at most one item from each category ---
    # Group items by their category
    items_by_category = defaultdict(list)
    for i, cat in enumerate(categories):
        items_by_category[cat].append(i)

    # For each category, add a penalty for selecting more than one item.
    # The penalty term for a category is P_cat * (sum_{i in cat}(x_i) - 1)^2 if sum > 1
    # which simplifies to adding a penalty for each pair (i, j) in the category.
    for cat, items in items_by_category.items():
        if len(items) > 1:
            for i, j in combinations(items, 2):
                Q[(i, j)] += p_cat

    # --- Constraint 3: Do not select taboo pairs ---
    # Add a penalty P_taboo * x_i * x_j for each taboo pair (i, j).
    for i, j in taboo_pairs:
        Q[(i, j)] += p_taboo
        
    return Q

def solve_and_display_results(qubo, values, weights, config):
    """
    Solves the QUBO using a simulated annealer and prints the results.

    Args:
        qubo (dict): The QUBO model.
        values (list): List of item values.
        weights (list): List of item weights.
        config (dict): Configuration dictionary.
    """
    # Solve using OpenJij's Simulated Annealing Sampler
    sampler = oj.SASampler()
    response = sampler.sample_qubo(qubo, num_reads=config['num_reads'])

    # Get the best solution (lowest energy)
    best_sample = response.first.sample
    
    # Calculate metrics for the best solution
    selected_items = [i for i, bit in best_sample.items() if bit == 1]
    total_value = sum(values[i] for i in selected_items)
    total_weight = sum(weights[i] for i in selected_items)

    # Print a summary of the results
    print("--- QUBO Optimization Results ---")
    print(f"Lowest Energy: {response.first.energy:.2f}")
    print("-" * 35)
    print(f"Selected Items: {selected_items}")
    print(f"Total Value: {total_value}")
    print(f"Total Weight: {total_weight} (Max: {config['max_weight']})")
    print("-" * 35)


if __name__ == "__main__":
    # --- Problem Configuration ---
    problem_config = {
        'num_items': 100,
        'num_categories': 10,
        'num_taboo_pairs': 5,
        'max_weight': 1000,
        'penalty_mass': 50,
        'penalty_category': 50,
        'penalty_taboo': 100,
        'num_reads': 100, # Number of reads for the sampler
    }

    # 1. Generate the problem data
    item_values, item_weights, item_categories, taboo_item_pairs = generate_problem_data(problem_config)

    # 2. Build the QUBO model from the data
    qubo_model = build_qubo(item_values, item_weights, item_categories, taboo_item_pairs, problem_config)
    
    # 3. Solve the QUBO and display the results
    solve_and_display_results(qubo_model, item_values, item_weights, problem_config)
