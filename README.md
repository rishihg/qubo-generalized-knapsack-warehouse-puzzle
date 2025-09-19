### The Warehouse Selection Puzzle: A QUBO-Based Optimization Solution
This repository contains a Python script that solves "The Warehouse Selection Puzzle," a complex combinatorial optimization problem. The solution is found by formulating the problem as a QUBO (Quadratic Unconstrained Binary Optimization) model and using a simulated annealer from the openjij library.

### 1. The Challenge: The Warehouse Selection Puzzle
Our company’s distribution hub is preparing for a major outbound shipment from a stock of 100 distinct inventory items. The objective is to choose a subset of these items that maximizes the total monetary value while adhering to a strict set of operational rules.

Each item is defined by three attributes:

- Monetary Figure: The item’s value, in whole dollars (ranging from 100 to 1000).
- Mass Value: The item’s mass in kilograms (an integer between 10 and 100).
- Categorical Tag: An integer label from 0 to 9, representing its group or supplier.

**Selection Guidelines**
The selection must satisfy the following non-negotiable rules:
- Rule A (Mass Ceiling): The total mass of all chosen items must not exceed 1000 kilograms.
- Rule B (Category Exclusivity): A shipment cannot contain more than one item from the same categorical tag.
- Rule C (Taboo Pairs): Certain predefined pairs of items are "taboo" and cannot be shipped together.

### 2. The Technical Approach: QUBO
This problem is a variation of the classic Knapsack Problem with multiple, complex constraints. To solve it, we turn to a quantum-inspired technique suitable for such optimization challenges:
1. **Problem Formulation**: The puzzle's objective (maximize value) and constraints (mass, category, taboo pairs) are translated into a single mathematical equation.

2. **QUBO Model**: This equation is expressed as a QUBO model. In a QUBO, we assign a binary variable (0 or 1) to each item, representing whether it's selected or not. The goal becomes finding the binary combination that minimizes a quadratic cost function, which cleverly encodes both our main objective and the penalties for breaking the rules.

3. **Simulated Annealing**: The script uses a simulated annealer (openjij.SASampler), a powerful classical algorithm that mimics the physical process of annealing metals. It is highly effective at navigating complex solution spaces to find the optimal (or near-optimal) minimum energy state of the QUBO, which corresponds to the best selection of items.

### 3. How to Run the Code
**Prerequisites**\
Ensure you have Python 3 installed, along with the following libraries:
- openjij
- numpy
  
You can install them using pip:\
'''python
pip install openjij numpy
'''

**Execution**
1. Clone this repository or download the knapsack_qubo_clean.py file.
2. Navigate to the file's directory in your terminal.
3. Run the script:\
'''python
python knapsack_qubo_clean.py'''

**4. Understanding the Output**\
The script will run the optimization and print the results, which constitute the deliverables for the puzzle:

- The identities of the chosen items: A list of the selected item indices.
- The total monetary figure: The maximized total value of the chosen set.
- The total mass value: The combined mass of the set, demonstrating that Rule A is satisfied.
- A clear demonstration of rule satisfaction: By examining the chosen items and their attributes, one can verify that Rules B and C are also satisfied.

**Example Output**\
'''python
--- QUBO Optimization Results ---
Lowest Energy: -23456.78
-----------------------------------
Selected Items: [5, 12, 23, 45, 67, 89]
Total Value: 4500
Total Weight: 998 (Max: 1000)
-----------------------------------
'''

**5. Code Structure**\
The Python script is organized into three main functions:
- generate_problem_data(): Creates a reproducible random dataset of 100 items based on the puzzle's specifications.
- build_qubo(): Translates the item data and the three rules into the final QUBO model.
- solve_and_display_results(): Feeds the QUBO to the openjij sampler and formats the final solution for display.
