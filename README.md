# Micrograph

Micrograph is a Python toy that uses ModernGL to render 3D objects.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Micrograph requires Python 3.7 or later. You also need to install `pipenv`, a tool for managing Python virtual environments. You can install `pipenv` by running:

```bash
pip install pipenv
```

## Installation
1. Clone the repository to your local machine:
```bash
git clone https://github.com/maxim-xyz/micrograph.git
```
2. Navigate to the root directory of the project:
```bash
cd micrograph
```
3. Install the project dependencies using pipenv:
```bash
pipenv install
```
This will install all the necessary dependencies specified in the Pipfile and Pipfile.lock.

## Usage
Once the dependencies are installed, you can run the main script by executing:
```bash
pipenv run python main.py
```
### Profiling
There currently only is basic profiling available, you can enable it by passing the '--profile' argument:
```bash
pipenv run python main.py --profile
```
This will create a file named output.pstats which you can analyze with tools such as SnakeViz to visualize the profiling data.

## Have fun! Thank you.