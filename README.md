# ⚡ Energy Positive Metro Project: Smart EMS Integrated Dynamic Simulation 🚇🔋☀️

## Project Summary

This project is an innovative **Proof of Concept** simulation aiming to create a sustainable model where metro systems not only meet their own energy consumption but also generate their own energy, even feeding surplus energy back to the national electricity grid, thus becoming "Energy Positive." ✨ By integrating renewable energy sources (solar and wind) with a Smart Energy Management System (EMS) into the metro infrastructure, the project seeks to maximize energy efficiency and environmental sustainability.

## 🌟 Project Objectives

* To increase the energy independence of metro systems.
* To reduce fossil fuel consumption and carbon footprint. 🌱
* To demonstrate the potential of integrating renewable energy sources into large-scale infrastructure.
* To model the role of smart energy management and battery storage systems.
* To evaluate the economic and environmental feasibility of the project through simulation. 💰

## ⚙️ Core Components and Approach

The project is built upon a dynamic simulation model encompassing the following key components:

1.  **Dynamic Data Profiles:** Hourly dynamic data such as metro train traffic density, station energy consumption, solar radiation, and wind speed are read from the `dinamik_veriler.xlsx` file for realistic scenario modeling.
2.  **Renewable Energy Sources:** Solar panels ☀️ and wind turbines 🌬️ are integrated into the metro system, and their energy production is simulated based on dynamic data.
3.  **Smart Energy Management System (EMS):** As the heart of the project, the EMS is designed to manage the balance between energy generation (renewables), consumption (trains and stations), battery charging/discharging, and grid interaction (buying/selling) at optimal cost and efficiency. This system uses an optimization model (utilizing the Pulp library) to optimize energy flow.
4.  **Battery Energy Storage System:** Batteries 🔋 play a critical role in balancing the fluctuations of renewable energy, storing surplus energy, and meeting immediate system demands. Charging and discharging efficiencies, as well as minimum/maximum state-of-charge thresholds, are taken into account.
5.  **Financial and Environmental Analysis:** The simulation calculates metrics such as energy costs/revenues, total capital expenditure (CAPEX), operational and maintenance (OPEX) costs, and carbon emissions to quantitatively assess the project's economic and environmental impacts.

## 📈 Achievements and Results

The simulations conducted have demonstrated that the project's main objectives have been achieved:

* **Energy Positivity:** The simulation showed that the metro system not only met its own consumption (trains and stations) but also generated a significant energy surplus through renewable energy sources, feeding this excess back to the national grid.
* **Reduced Grid Dependency:** Thanks to the Smart EMS and battery storage, it has been proven that the metro system's energy purchase from the grid was reduced to nearly zero.
* **Economic Potential:** Due to revenues from energy sales and optimized energy management, the project was determined to have the potential for net profit during the simulation period.
* **Environmental Benefit:** By minimizing energy purchase from the grid, the carbon footprint of the metro system has been significantly reduced.

## 📊 Example Simulation Outputs (Screenshots)

Here are some example graphs generated after running the simulation:

<img width="1915" height="1002" alt="image" src="https://github.com/user-attachments/assets/3256f02a-4b9d-4399-92e5-3d44b2f8367e" />
_Graph 1: Daily Metro Energy Balance_

<img width="1919" height="1014" alt="image" src="https://github.com/user-attachments/assets/786c9e7a-6d54-4137-a309-29a50a6f5167" />
_Graph 2: Hourly Metro Energy Flow_

<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/03d8d99e-78c4-4af2-b4ae-056bc263bb80" />
_Graph 3: Hourly Battery State of Charge_

<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/12de54b7-d3c5-4043-adc9-307fbe4c4cb9" />
_Graph 4: Hourly Battery Charge/Discharge Flow_

<img width="1917" height="1014" alt="image" src="https://github.com/user-attachments/assets/7692516f-f507-4bd1-a968-cda6a69a287e" />
_Graph 5: Hourly Energy Cost/Revenue_

## 📂 Project Structure
MetroEnerjiSimulasyonu/
├── main.py                 # 🚀 Main file that starts the simulation and visualizes results

├── simulasyon_motoru.py    # 🧠 Contains the core logic for energy balance calculations and EMS optimization

├── gorsellestirme.py       # 📊 Functions for plotting simulation results into graphs

├── parametreler.py         # ⚙️ File defining all fixed parameters for the simulation

├── dinamik_veriler.xlsx    # 📈 Excel file containing hourly energy consumption and generation profiles

└── README.md               # 📄 This README file

## 🚀 How to Run?

To run the project on your system, follow these steps:

1.  **Prerequisites:**
    * Ensure Python 3.x is installed.
    * Install the necessary Python libraries. Run the following command in your terminal:
        ```bash
        pip install pandas matplotlib pulp openpyxl
        ```
        (Note: `openpyxl` might be required for `pandas` to read Excel files.)

2.  **Clone or Download the Repository:**
    * If Git is installed, clone the repository by navigating to your desired directory in the terminal and running:
        ```bash
        git clone [https://github.com/emineugurlu/MetroEnerjiSimulasyonu.git](https://github.com/emineugurlu/MetroEnerjiSimulasyonu.git)
        ```

3.  **Navigate to Project Directory:**
    * Change your current directory in the terminal to the main project directory (where the `main.py` file is located):
        ```bash
        cd MetroEnerjiSimulasyonu
        ```

4.  **Start the Simulation:**
    * Run the following command to begin the simulation:
        ```bash
        python main.py
        ```

5.  **Results:**
    * You will see the simulation progress and summary results directly in your terminal.
    * Upon completion of the simulation, various graph windows generated by `matplotlib` will automatically open. 📊

## 💡 Future Development Opportunities (Our Vision)

This project lays a strong foundation for more comprehensive and real-world applications in the future. Our potential development areas include:

* **Machine Learning-Based Forecasting:** Integration of advanced machine learning models for more accurate forecasting of energy demand and renewable energy generation. This will enable the EMS to make proactive decisions.
* **Digital Twin Integration:** Creating a virtual replica of the metro system and its energy infrastructure to conduct detailed "what-if" scenarios, optimize maintenance processes, and autonomously improve the system.
* **Energy Trading Modules:** Maximizing the project's financial revenues by evaluating surplus energy in the spot market with dynamic pricing algorithms.
* **Social & Environmental Impact Analysis:** Quantifying the tangible contributions of carbon reduction to air quality, public health, and the overall well-being of city residents, presenting it as an added value proposition to project stakeholders.

---
