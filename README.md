# Genetic Algorithm for Cryptarithmetic Problem

This project implements a genetic algorithm to solve cryptarithmetic problems, where words are used to represent equations (e.g., SEND + MORE = MONEY). Each letter is assigned a unique digit, and the goal is to find an assignment that satisfies the equation.

## Features
- **Population Generation:** Generates an initial population with 30% of high-fitness individuals.
- **Fitness Calculation:** Measures how close a solution is to satisfying the equation.
- **Selection Methods:** Supports Roulette Wheel and Tournament selection.
- **Crossover Operators:** Implements Cyclic and Partially Mapped Crossover (PMX).
- **Mutation:** Introduces diversity in the population by modifying individuals.
- **Reinsertion Strategies:** Includes ordered reinsertion and elitism.
- **Stagnation Handling:** Generates new individuals if the population stagnates.

## Requirements
This project uses **Python** and the **Poetry** package manager for dependency management.

## Setup
1. Install Poetry if not already installed:
   ```bash
   pip install poetry
   ```
2. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/esteveseverson/Genetic_Cryptarithmetic
   cd Genetic_Cryptarithmetic
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Activate the Poetry shell:
   ```bash
   poetry shell
   ```

## How to Use
1. Run the program:
   ```bash
   python cripto_aritmetica/ciclic_crossover.py
   ```
2. Enter the words representing the equation when prompted. Ensure all words use distinct letters and the total number of unique letters does not exceed 10.

## Key Functions

### 1. Population Management
- **`generate_population`:** Creates the initial population with a mix of high-fitness and placebo individuals.

### 2. Fitness Evaluation
- **`fitness`:** Computes the difference between the equation’s left and right sides.

### 3. Selection Methods
- **`roulette`:** Selects individuals probabilistically based on fitness.
- **`tournament`:** Selects the best individual from a random subset.

### 4. Genetic Operators
- **Crossover:**
  - **`ciclic_crossover`:** Implements cyclic crossover.
  - **`pmx_crossover`:** Implements PMX.
- **Mutation:**
  - **`mutate`:** Introduces diversity by modifying an individual.

### 5. Reinsertion Strategies
- **`reinsertion_ordered`:** Combines parents and offspring, selecting the best individuals.
- **`reinsertion_elitism`:** Preserves the top 20% of the current population.

### 6. Main Algorithm
- **`genetic_algorithm`:** Orchestrates the genetic algorithm’s workflow, including population generation, selection, crossover, mutation, and reinsertion.

## Example
When executed, the program prompts the user to input three words:

- First word (e.g., `SEND`)
- Second word (e.g., `MORE`)
- Result word (e.g., `MONEY`)

### Sample Output:
```
Enter the first word: SEND
Enter the second word: MORE
Enter the result word: MONEY

Solution found with 0 fitness, in generation 288
{'S': 9, 'E': 5, 'N': 6, 'D': 7, 'M': 1, 'O': 0, 'R': 8, 'Y': 2}
SEND + MORE = MONEY
9567 + 1085 = 10652
Error: 0
In generation: 288
```

## Notes
- Ensure the input words contain distinct letters.
- The algorithm will stop if a solution is found or the maximum number of generations is reached.

## Contributing
Feel free to open issues or submit pull requests to improve the project.

## License
This project is licensed under the MIT License.

