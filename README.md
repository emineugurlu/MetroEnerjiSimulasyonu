# 🚇 Energy Positive Metro: Smart EMS Integrated Dynamic Simulation

> **"A transformative Proof of Concept (PoC) modeling an energy-independent metro ecosystem. Integrating dynamic renewable energy sources (Solar/Wind) with a Smart Energy Management System (EMS) to achieve net-positive grid contribution."**

![Repo Size](https://img.shields.io/github/repo-size/emineugurlu/MetroEnerjiSimulasyonu?color=yellowgreen&style=flat-square)
![Optimization](https://img.shields.io/badge/Optimization-PuLP-blue?style=flat-square)
![Analysis](https://img.shields.io/badge/Data-Pandas%20%26%20Matplotlib-blueviolet?style=flat-square)

The future of urban transportation lies in **Energy Autonomy**. This project simulates a dynamic environment where metro infrastructure transitions from an energy consumer to a green energy producer. By leveraging a **Linear Programming (LP) optimization model**, the system intelligently balances renewable generation, battery storage (BESS), and national grid interactions to minimize carbon footprint while maximizing financial returns.

---

## 🚀 Engineering Mindset

This simulation is architected as a **Digital Twin Framework**:

* **Dynamic Load Balancing:** Utilizing hourly dynamic data profiles (train density, solar radiation, wind velocity) to model realistic energy consumption/generation cycles.
* **LP-Based Optimization (PuLP):** The heart of the system is an **EMS Engine** that solves complex cost-efficiency equations to determine the optimal flow between batteries, renewables, and the grid in real-time.
* **BESS Lifecycle Modeling:** Implementing Battery Energy Storage System (BESS) logic with strict SoC (State of Charge) thresholds, charging/discharging efficiency coefficients, and immediate demand fulfillment protocols.
* **Financial & Carbon Analytics:** A dual-objective analysis layer that calculates CAPEX/OPEX metrics alongside avoided carbon emissions, proving the project's **Environmental & Economic Feasibility**.
* **Modular Architecture:** Clean separation of concerns between the Simulation Engine, Visualization Layer, and Parameter Definition files.

## 🌟 Key Results & Impact

* ⚡ **Energy Positivity:** Proven capability to meet total internal demand and export surplus energy back to the national grid.
* 📉 **Grid Independence:** Achieved near-zero dependency on external grid power during peak renewable production hours through intelligent battery orchestration.
* 🌱 **Decarbonization:** Significant reduction in carbon footprint by substituting grid-sourced electricity with localized green energy.
* 💰 **Revenue Generation:** Optimized selling cycles on the virtual spot market, turning a traditional cost center into a profit-generating asset.

## 📊 Visual Data Showcase

| Energy Balance & Flow | Battery (BESS) Management |
| :--- | :--- |
| ![Energy Balance](https://github.com/user-attachments/assets/3256f02a-4b9d-4399-92e5-3d44b2f8367e) | ![Battery SoC](https://github.com/user-attachments/assets/03d8d99e-78c4-4af2-b4ae-056bc263bb80) |
| *Hourly tracking of generation vs. demand.* | *Dynamic management of Battery State of Charge (SoC).* |
| ![Energy Flow](https://github.com/user-attachments/assets/786c9e7a-6d54-4137-a309-29a50a6f5167) | ![Financial Impact](https://github.com/user-attachments/assets/7692516f-f507-4bd1-a968-cda6a69a287e) |
| *System-wide energy distribution dynamics.* | *Cost/Revenue analysis of grid interactions.* |

---

## 🛠️ Installation & Setup Guide

To replicate this simulation environment on your local machine, follow these structured steps:

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/emineugurlu/MetroEnerjiSimulasyonu.git](https://github.com/emineugurlu/MetroEnerjiSimulasyonu.git)
cd MetroEnerjiSimulasyonu
````
### 3.Install Dependencies
Install the necessary data processing, visualization, and optimization libraries:
````bash
pip install pandas matplotlib pulp openpyxl
````
### 4.Run the Simulation
Execute the main orchestration script to start the engine and generate visual reports:
````bash
python main.py
````

📂 Project Structure
main.py: The entry point that orchestrates the simulation and triggers visualizations.

simulasyon_motoru.py: The core logic containing the PuLP optimization model and energy balance calculations.

gorsellestirme.py: Dedicated functions for generating high-fidelity Matplotlib graphs.

parametreler.py: Configuration file for battery capacities, efficiency coefficients, and pricing.

dinamik_veriler.xlsx: The dataset containing hourly consumption and generation profiles.

Developed by Emine Uğurlu - Computer Engineer. Focused on the intersection of AI, Energy, and Sustainable Infrastructure.
